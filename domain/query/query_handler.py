from abc import ABC, abstractmethod

from domain.query.query import Query
from domain.query.query_response import QueryResponse


class QueryHandler(ABC):
    @abstractmethod
    def process(self, query: Query) -> QueryResponse:
        pass
