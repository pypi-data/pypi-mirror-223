import asyncio
import json
import os
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Dict, List, NamedTuple, Optional, Type
from uuid import uuid4

import openai
from cheapcone import (Embedding, Filter, MetaData, PineconeClient, Query,
                       QueryBuilder, Value)
from pydantic import Field  # pylint: disable=no-name-in-module
from tqdm import tqdm

from ..client import APIClient, APIException
from ..typedefs import F, FunctionType, Vector
from ..utils import chunker, handle_errors, setup_logging
from .schemas import List, Model

logger = setup_logging(__name__)


class Greet(FunctionType):
    """Placeholder function for greeting the user."""

    prompt: str = Field(..., description="The prompt to use for the completion.")

    async def run(self):
        return "Hello, I am a chatbot. How are you?"


class IngestRequest(NamedTuple):
    namespace: str
    texts: List[str]


@dataclass
class LLMStack:
    model: Model = field(default_factory=lambda: "gpt-3.5-turbo-16k-0613")
    base_url: str = field(default_factory=lambda: os.environ["PINECONE_API_URL"])
    api_key: str = field(default_factory=lambda: os.environ["PINECONE_API_KEY"])

    @property
    def pinecone(self) -> PineconeClient:
        return PineconeClient()

    @handle_errors
    async def upsert_vector(self, vector: Vector, metadata: MetaData):
        return await self.pinecone.upsert([Embedding(values=vector, metadata=metadata)])

    @handle_errors
    async def upsert_vectors(self, vectors: List[Vector], metadata: List[MetaData]):
        return await self.pinecone.upsert(
            embeddings=[
                Embedding(values=vector, metadata=metadata)
                for vector, metadata in zip(vectors, metadata)
            ]
        )

    @handle_errors
    async def query_vectors(self, vector: Vector, query: Query):
        response = await self.pinecone.query(vector=vector, expr=query)
        logger.info("Query response: %s", response)
        return sorted(response.matches, key=lambda x: x.score, reverse=True)

    @handle_errors
    async def upsert_messages(
        self,
        user_embedding: Vector,
        openai_embedding: Vector,
        prompt: str,
        text: str,
        namespace: str,
    ) -> int:
        """Upserts the messages to Pinecone."""
        count = 0
        res = await self.upsert_vector(
            vector=user_embedding, metadata={"text": text, "namespace": namespace}
        )
        logger.info("Upserted user embedding: %s", res)
        ress = await self.upsert_vector(
            vector=openai_embedding, metadata={"text": prompt, "namespace": namespace}
        )
        logger.info("Upserted openai embedding: %s", ress)
        return count + res.upsertedCount + ress.upsertedCount

    @handle_errors
    async def chat(self, text: str, context: str) -> str:
        """Chat completion with no functions."""
        messages = [
            {"role": "user", "content": text},
            {"role": "system", "content": context},
        ]
        logger.info("Chat messages: %s", messages)
        response = await openai.ChatCompletion.acreate(
            model=self.model, messages=messages
        )
        logger.info("Chat response: %s", response)
        assert isinstance(response, dict)
        return response["choices"][0]["message"]["content"]

    @handle_errors
    async def chat_with_memory(self, text: str, namespace: str, context: str) -> str:
        """Chat completion with similarity search retrieval from pinecone"""
        try:
            embedding = await self.create_embeddings(text)
            builder = QueryBuilder()
            query = builder("namespace") == namespace
            query_response = await self.query_vectors(embedding, query.query)
            sorted_query_response = sorted(
                query_response, key=lambda x: x.score, reverse=True
            )
            similar_text_chunks = [
                x.metadata["text"]
                for x in sorted_query_response
                if isinstance(x.metadata["text"], str)
            ]
            similar_text = "Previous Similar results:" + "\n".join(similar_text_chunks)
            messages = [
                {"role": "user", "content": text},
                {"role": "system", "content": similar_text},
                {"role": "system", "content": context},
            ]
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=messages,
            )
            chat_response = response["choices"][0]["message"]["content"]  # type: ignore
            await self.upsert_messages(
                user_embedding=embedding,
                openai_embedding=await self.create_embeddings(chat_response),
                prompt=text,
                text=chat_response,
                namespace=namespace,
            )
            assert isinstance(chat_response, str)
            return chat_response
        except Exception as exc:
            logger.exception(exc)
            raise APIException(message=str(exc)) from exc

    @handle_errors
    async def create_embeddings(self, text: str) -> Vector:
        """Creates embeddings for the given texts."""
        response = await openai.Embedding.acreate(
            model="text-embedding-ada-002",
            input=text,
        )
        return response["data"][0]["embedding"]  # type: ignore

    async def chat_stream(self, text: str) -> AsyncGenerator[str, None]:
        """Chat completion stream with no functions."""
        response = openai.ChatCompletion.acreate(
            model=self.model,
            messages=[{"role": "user", "content": text}],
            stream=True,
        )
        async for i in response:  # type: ignore
            assert isinstance(i, dict)
            delta = i["choices"][0]["delta"]
            if "content" in delta:
                yield delta["content"]

    async def chat_stream_with_memory(
        self, text: str, namespace: str = "default"
    ) -> AsyncGenerator[str, None]:
        """Chat completion stream with similarity search retrieval from pinecone"""
        try:
            embedding = await self.create_embeddings(text)
            query = QueryBuilder("namespace") == namespace
            query_response = await self.query_vectors(embedding, query)
            similar_text_chunks = [
                x.metadata["text"]
                for x in query_response
                if isinstance(x.metadata["text"], str)
            ]
            similar_text = "Previous Similar results:" + "\n".join(similar_text_chunks)
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[
                    {"role": "user", "content": text},
                    {"role": "system", "content": similar_text},
                ],
                stream=True,
            )
            assert isinstance(response, AsyncGenerator)
            async for i in response:
                assert isinstance(i, dict)
                delta = i["choices"][0]["delta"]
                if "content" in delta:
                    yield delta["content"]
        except Exception as exc:
            logger.exception(exc.__class__.__name__)
            logger.exception(exc)
            raise APIException(message=str(exc)) from exc

    @handle_errors
    async def chatgpt(
        self, text: str, context: str, namespace: str = "default", memory: bool = False
    ):
        """ChatGPT4 is a function that allows you to chat with GPT-4, with the option of using memory or functions."""
        if memory:
            return await self.chat_with_memory(
                text=text, namespace=namespace, context=context
            )
        return await self.chat(text=text, context=context)

    @handle_errors
    async def ingest_bulk(self, data: IngestRequest, chunksize: int = 32) -> int:
        """Ingest bulk data."""
        count = 0
        embeddings: List[Embedding] = await asyncio.gather(
            *[self.create_embeddings(i) for i in data.texts]
        )
        meta = []
        for i in data.texts:
            meta.append({"text": i, "namespace": data.namespace})
        for i in range(0, len(embeddings), chunksize):
            vectors = []
            for j in range(i, i + chunksize):
                if j < len(embeddings):
                    vectors.append(embeddings[j].values)
            await self.upsert_vectors(
                vectors=vectors,
                metadata=meta[i : i + chunksize],
            )
            count += len(vectors)
        return count

async def parse_openai_response(  # pylint: disable=dangerous-default-value
    response: dict,
    functions: List[
        Type[F]
    ] = FunctionType._subclasses,  # pylint: disable=protected-access
) -> Any:
    """Parse the response from OpenAI and return the result."""
    choice = response["choices"][0]["message"]
    if "function_call" in choice:
        function_call_ = choice["function_call"]
        name = function_call_["name"]
        arguments = function_call_["arguments"]
        for i in functions:
            if i.__name__ == name:
                result = await i.run(i(**json.loads(arguments)))
                break
        else:
            raise ValueError(f"Function {name} not found")
        return result
    return choice["content"]


@handle_errors
async def function_call(  # pylint: disable=dangerous-default-value
    text: str,
    context: Optional[str] = None,
    model: Model = "gpt-3.5-turbo-16k-0613",
    functions: List[
        Type[F]
    ] = FunctionType._subclasses,  # pylint: disable=protected-access
) -> Any:
    """
    Function to call a OpenAI function with given text and context.

    Arguments:
    text -- Input text for the function
    context -- Optional context for the function
    model -- Model to be used. Defaults to "gpt-4-0613"
    functions -- List of function types. Defaults to all subclasses of FunctionType.
    """
    if context is not None:
        messages = [
            {"role": "user", "content": text},
            {"role": "system", "content": context},
        ]
    else:
        messages = [{"role": "user", "content": text}]
    response = await openai.ChatCompletion.acreate(
        model=model, messages=messages, functions=[i.openaischema for i in functions]
    )
    return await parse_openai_response(response, functions=functions)  # type: ignore
