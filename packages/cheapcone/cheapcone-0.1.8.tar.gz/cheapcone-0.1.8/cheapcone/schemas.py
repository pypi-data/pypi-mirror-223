"""Pydantic models for the PineCone API."""
from typing import List
from uuid import uuid4

from pydantic import Field

from .typedefs import CheapModel, MetaData, Query, Vector


class UpsertRequest(CheapModel):
    """Request to upsert a vector."""

    id: str = Field(default_factory=lambda: str(uuid4()))
    values: Vector = Field(...)
    metadata: MetaData = Field(...)


class Embedding(CheapModel):
    """Request to upsert a vector."""

    values: Vector = Field(...)
    metadata: MetaData = Field(...)


class QueryRequest(CheapModel):
    """Request to query for similar vectors."""

    topK: int = Field(default=10)
    filter: dict = Field(...)
    includeMetadata: bool = Field(default=True)
    vector: Vector = Field(...)


class QueryMatch(CheapModel):
    """A single match from a query."""

    id: str = Field(...)
    score: float = Field(...)
    metadata: MetaData = Field(...)


class QueryResponse(CheapModel):
    """Response to a query."""

    matches: List[QueryMatch] = Field(...)


class UpsertResponse(CheapModel):
    """Response to an upsert."""

    upsertedCount: int = Field(...)
