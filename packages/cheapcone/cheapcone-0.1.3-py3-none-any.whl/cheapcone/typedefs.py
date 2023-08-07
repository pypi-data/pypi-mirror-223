from __future__ import annotations

from typing import (Any, Callable, Dict, Generic, List, Literal, Optional,
                    Tuple, Type, TypeVar, Union, cast)
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .json import dumps, loads

Vector = List[float]
Value = Union[str, int, float, bool,List[str]]
MetaData = Dict[str, Value]
Filter = Literal["$eq","$ne","$lt","$lte","$gt","$gte","$in","$nin"]
Query = Dict[Filter,Union[Value,'Query',List[Value],List['Query']]]

class CheapModel(BaseModel):
	def json(self, *args, **kwargs) -> str:
		return dumps(self.dict())

	@classmethod
	def parse(cls, s: str) -> CheapModel:
		return cls(**loads(s))

