"""Type definitions for CheapCone."""
from __future__ import annotations

from typing import Dict, List, Literal, Union

from pydantic import BaseModel  # pylint: disable=no-name-in-module

from .json import dumps, loads

Vector = List[float]
Value = str | int | float | bool | List[str]
MetaData = Dict[str, Value]
Filter = Literal["$eq", "$ne", "$lt", "$lte", "$gt", "$gte", "$in", "$nin"]
AndOr = Literal["$and", "$or"]
Query = Union[
    Dict[str, Union[Value, "Query", List[Value], List["Query"]]],
    Dict[AndOr, List[Dict[str, Union[Value, "Query", List[Value], List["Query"]]]]],
]


class CheapModel(BaseModel):
    """Cheap model that allow cheap serialization and deserialization."""

   

    def json(self, *args, **kwargs) -> str:
        """Serialize the model to JSON."""
        return dumps(self.dict())


    def dict(self, *args, **kwargs) -> Dict:
        """Serialize the model to a dictionary."""
        return loads(super().json(*args, **kwargs))

class QueryBuilder:
    """Query builder for Pinecone Query API with MongoDB-like syntax."""

    def __init__(self, field: str = None, query: Query = None):  # type: ignore
        self.field = field
        self.query = query if query else {}

    def __repr__(self) -> str:
        return f"{self.query}"

    def __call__(self, field_name: str) -> QueryBuilder:
        return QueryBuilder(field_name)

    def __and__(self, other: QueryBuilder) -> QueryBuilder:
        return QueryBuilder(query={"$and": [self.query, other.query]})

    def __or__(self, other: QueryBuilder) -> QueryBuilder:
        return QueryBuilder(query={"$or": [self.query, other.query]})

    def __eq__(self, value: Value) -> QueryBuilder:
        return QueryBuilder(query={self.field: {"$eq": value}})

    def __ne__(self, value: Value) -> QueryBuilder:
        return QueryBuilder(query={self.field: {"$ne": value}})

    def __lt__(self, value: Value) -> QueryBuilder:
        return QueryBuilder(query={self.field: {"$lt": value}})

    def __le__(self, value: Value) -> QueryBuilder:
        return QueryBuilder(query={self.field: {"$lte": value}})

    def __gt__(self, value: Value) -> QueryBuilder:
        return QueryBuilder(query={self.field: {"$gt": value}})

    def __ge__(self, value: Value) -> QueryBuilder:
        return QueryBuilder(query={self.field: {"$gte": value}})

    def in_(self, values: List[Value]) -> QueryBuilder:
        """MongoDB-like syntax for $in operator."""
        return QueryBuilder(query={self.field: {"$in": values}})

    def nin_(self, values: List[Value]) -> QueryBuilder:
        """MongoDB-like syntax for $nin operator."""
        return QueryBuilder(query={self.field: {"$nin": values}})
