from __future__ import annotations

import asyncio
from asyncio import Lock
from dataclasses import dataclass, field
from os import environ
from typing import Dict, List, Optional, Type

from aiohttp import ClientSession
from aiohttp.client import ClientResponse, ClientTimeout, TCPConnector
from dotenv import load_dotenv
from multidict import CIMultiDict
from pydantic import BaseModel, Field

from .proxy import LazyProxy
from .schemas import (MetaData, Query, QueryMatch, QueryRequest, QueryResponse,
                      UpsertRequest, UpsertResponse, Vector)
from .typedefs import Filter, QueryBuilder, Value

load_dotenv()


@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class APIClient(LazyProxy[ClientSession]):
    """
    HTTP Client:
    Base class to create HTTP clients that wrap `aiohttp.ClientSession`.
    Provides Lazy Loading through proxy objects and session reuse using the singleton pattern.
    Constructor Signature:
    `base_url` (str): Base URL of the API. For example: `https://api.openai.com`. Must the an absolute URL.
    `headers` (dict): Headers that will proxide the authentication credentials, content_type, etc.
    """

    base_url: str = field(init=True, repr=True)
    headers: Dict[str, str] = field(default_factory=dict)
    _subclasses: Optional[List[Type[APIClient]]] = None
    _session_creation_lock = asyncio.Lock()
    _session: Optional[ClientSession] = None

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls._subclasses is None:
            cls._subclasses = []
        cls._subclasses.append(cls)

    @classmethod
    async def cleanup(cls):
        if hasattr(cls, "_subclasses") and cls._subclasses is not None:
            tasks = []
            for subclass in cls._subclasses:
                if subclass._session is not None:
                    tasks.append(subclass._session.close())
            await asyncio.gather(*tasks)
            cls._subclasses = None

    async def __load__(self) -> ClientSession:
        async with self._session_creation_lock:
            if self._session is None:
                self._session = ClientSession(
                    base_url=self.base_url,
                    headers=CIMultiDict(self.headers),
                    response_class=ClientResponse,
                    connector=TCPConnector(
                        keepalive_timeout=60,
                        ssl=False,
                        limit=1000,
                    ),
                    timeout=ClientTimeout(total=60),
                    connector_owner=False,
                    trust_env=False,
                    read_bufsize=2**18,
                )
        return self._session

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {self.base_url}>"


@dataclass(init=True, repr=True, unsafe_hash=False, frozen=False)
class PineconeClient(APIClient):
    """
    Cheapcone went greedy so I had to make this one.
    """

    base_url: str = field(default=environ["PINECONE_API_URL"], init=True, repr=True)
    api_key: str = field(default=environ["PINECONE_API_KEY"], init=True, repr=False)

    def __load__(self) -> ClientSession:
        return ClientSession(base_url=self.base_url, headers={"api-key": self.api_key})

    async def upsert(self, values: Vector, metadata: MetaData) -> UpsertResponse:
        async with self.__load__() as session:
            async with session.post(
                "/upsert", json=UpsertRequest(values=values, metadata=metadata).dict()
            ) as response:
                return UpsertResponse(**await response.json())

    async def query(
        self, expr: Query, vector: Vector, includeMetadata: bool = True, topK: int = 10
    ) -> QueryResponse:
        async with self.__load__() as session:
            async with session.post(
                "/vectors/query",
                json=QueryRequest(
                    topK=topK,
                    filter=expr,
                    vector=vector,
                    includeMetadata=includeMetadata,
                ).dict(),
            ) as response:
                return QueryResponse(**await response.json())
