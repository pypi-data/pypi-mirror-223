from datetime import datetime
from json import JSONDecoder, JSONEncoder
from typing import Any, NamedTuple
from uuid import UUID

from pydantic import BaseModel


class PineconeEncoder(JSONEncoder):
    def default(self, obj: Any) -> Any:
        if isinstance(obj, UUID):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.astimezone().isoformat()
        elif isinstance(obj, NamedTuple):
            return obj._asdict()
        elif isinstance(obj, BaseModel):
            return obj.dict()
        else:
            return super().default(obj)


class PineconeDecoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        kwargs["object_hook"] = self.object_hook
        super().__init__(*args, **kwargs)

    def object_hook(self, obj: Any) -> Any:
        if "uuid" in obj:
            return UUID(obj["uuid"])
        elif "datetime" in obj:
            return datetime.fromisoformat(obj["datetime"])
        elif "type" in obj and "fields" in obj:
            return self.named_tuple_hook(obj)
        elif "type" in obj and "data" in obj:
            return self.pydantic_hook(obj)
        else:
            return obj

    def named_tuple_hook(self, obj: Any) -> Any:
        cls = NamedTuple(obj["type"], obj["fields"])
        return cls(*obj["values"])

    def pydantic_hook(self, obj: Any) -> Any:
        cls = getattr(__import__(obj["type"]), obj["type"])
        return cls(**obj["data"])


def dumps(obj: Any) -> str:
    return PineconeEncoder().encode(obj)


def loads(s: str) -> Any:
    return PineconeDecoder().decode(s)
