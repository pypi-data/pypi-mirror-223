"""JSON serialization and deserialization for Pinecone."""
from datetime import datetime
from json import JSONDecoder, JSONEncoder
from typing import Any, NamedTuple
from uuid import UUID

from pydantic import BaseModel  # pylint: disable=no-name-in-module
from typing_extensions import override


class PineconeEncoder(JSONEncoder):
    """Serialize UUID, datetime, NamedTuple, and Pydantic models."""

    def default(self, obj: Any) -> Any:
        """Serialize UUID, datetime, NamedTuple, and Pydantic models."""
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
    """Deserialize UUID, datetime, NamedTuple, and Pydantic models."""

    def __init__(self, *args, **kwargs):
        """Deserialize UUID, datetime, NamedTuple, and Pydantic models."""
        kwargs["object_hook"] = self.object_hook
        super().__init__(*args, **kwargs)

    @override
    def object_hook(self, obj: Any) -> Any:
        """Deserialize UUID, datetime, NamedTuple, and Pydantic models."""
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
        """Deserialize NamedTuple."""
        cls = NamedTuple(obj["type"], obj["fields"])
        return cls(*obj["values"])

    def pydantic_hook(self, obj: Any) -> Any:
        """Deserialize Pydantic models."""
        cls = getattr(__import__(obj["type"]), obj["type"])
        return cls(**obj["data"])


def dumps(obj: Any) -> str:
    """Serialize UUID, datetime, NamedTuple, and Pydantic models."""
    return PineconeEncoder().encode(obj)


def loads(s: str) -> Any:
    """Deserialize UUID, datetime, NamedTuple, and Pydantic models."""
    return PineconeDecoder().decode(s)
