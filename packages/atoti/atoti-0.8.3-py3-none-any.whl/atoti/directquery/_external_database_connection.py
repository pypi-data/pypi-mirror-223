from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Generic, TypeVar

from .._external_table_identifier import ExternalTableIdentifier
from .._java_api import JavaApi
from ..directquery import ExternalTables
from ..type import DataType
from ._external_table import ExternalTable, ExternalTableT_co


class ExternalDatabaseConnection(Generic[ExternalTableT_co], ABC):
    def __init__(self, *, database_key: str, java_api: JavaApi) -> None:
        super().__init__()

        self._database_key = database_key
        self._java_api = java_api

    @property
    def tables(self) -> ExternalTables[ExternalTableT_co]:
        """Tables of the external database."""
        table_descriptions = self._java_api.get_external_tables(self._database_key)
        return ExternalTables(
            _tables=table_descriptions,
            _database_key=self._database_key,
            _create_table=lambda identifier: self._discover_and_create_table(
                identifier
            ),
        )

    @abstractmethod
    def _create_table(
        self,
        identifier: ExternalTableIdentifier,
        /,
        *,
        types: Mapping[str, DataType],
    ) -> ExternalTableT_co:
        ...

    def _discover_and_create_table(
        self,
        identifier: ExternalTableIdentifier,
    ) -> ExternalTableT_co:
        columns = self._java_api.get_external_table_schema(
            self._database_key, identifier=identifier
        )
        return self._create_table(identifier, types=columns)


ExternalDatabaseConnectionT = TypeVar(
    "ExternalDatabaseConnectionT",
    bound=ExternalDatabaseConnection[ExternalTable],
)
