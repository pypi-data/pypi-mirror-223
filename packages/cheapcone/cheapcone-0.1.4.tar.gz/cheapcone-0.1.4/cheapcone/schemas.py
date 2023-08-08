from typing import List
from uuid import uuid4

from pydantic import Field

from .typedefs import CheapModel, MetaData, Query, Vector


class UpsertRequest(CheapModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    values: Vector = Field(...)
    metadata: MetaData = Field(...)


class QueryRequest(CheapModel):
    topK: int = Field(default=10)
    filter: Query = Field(...)
    includeMetadata: bool = Field(default=True)
    vector: Vector = Field(...)


class QueryMatch(CheapModel):
    id: str = Field(...)
    score: float = Field(...)
    metadata: MetaData = Field(...)


class QueryResponse(CheapModel):
    matches: List[QueryMatch] = Field(...)


class UpsertResponse(CheapModel):
    upsertedCount: int = Field(...)
