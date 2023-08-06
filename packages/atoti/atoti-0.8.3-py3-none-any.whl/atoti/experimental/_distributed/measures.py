from collections.abc import Iterable, Mapping
from typing import Optional

from atoti_core import MeasureIdentifier
from atoti_query import QueryMeasure

from ..._java_api import JavaApi
from ..._local_measures import LocalMeasures


class DistributedMeasures(LocalMeasures[QueryMeasure]):
    def __init__(self, *, cube_name: str, java_api: JavaApi) -> None:
        super().__init__(java_api=java_api)

        self._cube_name = cube_name

    def _get_underlying(self) -> dict[str, QueryMeasure]:
        """Fetch the measures from the JVM each time they are needed."""
        measures = self._java_api.get_measures(self._cube_name)
        return {
            identifier.measure_name: QueryMeasure(
                identifier,
                description=measure.description,
                folder=measure.folder,
                formatter=measure.formatter,
                visible=measure.visible,
            )
            for identifier, measure in measures.items()
        }

    def __getitem__(self, key: str, /) -> QueryMeasure:
        identifier = MeasureIdentifier(key)
        measure = self._java_api.get_measure(identifier, cube_name=self._cube_name)
        return QueryMeasure(
            identifier,
            formatter=measure.formatter,
            folder=measure.folder,
            description=measure.description,
            visible=measure.visible,
        )

    def _update(
        self,
        other: Mapping[str, QueryMeasure],  # noqa: ARG002
        /,
    ) -> None:
        raise AssertionError("Distributed cube measures cannot be changed.")

    def _delete_keys(
        self,
        keys: Optional[Iterable[str]] = None,  # noqa: ARG002
        /,
    ) -> None:
        raise AssertionError("Distributed cube measures cannot be changed.")
