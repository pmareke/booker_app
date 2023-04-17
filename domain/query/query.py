from dataclasses import dataclass
from uuid import UUID


@dataclass
class Query:
    query_id: UUID
