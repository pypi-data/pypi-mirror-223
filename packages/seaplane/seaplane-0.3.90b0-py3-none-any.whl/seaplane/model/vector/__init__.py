from enum import Enum
from typing import Any, Dict, List, NamedTuple, Optional
import uuid


class Vector(NamedTuple):

    vector: List[float]
    id: str = str(uuid.uuid4())
    metadata: Optional[Dict[Any, Any]] = None


Vectors = List[Vector]


class Distance(Enum):
    COSINE = "cosine"
    DOT = "dot"
    EUCLID = "euclid"

    def __str__(self) -> str:
        return str(self.value)
