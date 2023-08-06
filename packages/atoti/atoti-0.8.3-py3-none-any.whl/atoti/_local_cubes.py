from collections.abc import Iterable, Mapping
from typing import Any, Optional, Protocol, TypeVar, cast

from atoti_core import BaseCubes, DelegateMutableMapping

from ._local_cube import LocalCube

_LocalCube_co = TypeVar(
    "_LocalCube_co", bound="LocalCube[Any, Any, Any]", covariant=True
)


class _DeleteCube(Protocol):
    def __call__(self, cube_name: str, /) -> None:
        ...


class _GetCube(Protocol[_LocalCube_co]):
    def __call__(self, cube_name: str, /) -> _LocalCube_co:
        ...


class _GetCubes(Protocol[_LocalCube_co]):
    def __call__(self) -> Mapping[str, _LocalCube_co]:
        ...


class LocalCubes(  # type: ignore[type-var]
    DelegateMutableMapping[
        str,
        _LocalCube_co,  # pyright: ignore[reportGeneralTypeIssues]
    ],
    BaseCubes[_LocalCube_co],
):
    def __init__(
        self,
        *,
        delete_cube: _DeleteCube,
        get_cube: _GetCube[_LocalCube_co],
        get_cubes: _GetCubes[_LocalCube_co],
    ) -> None:
        super().__init__()

        self._delete_cube = delete_cube
        self._get_cube = get_cube
        self._get_cubes = get_cubes

    def _update(
        self,
        other: Mapping[str, _LocalCube_co],  # noqa: ARG002
        /,
    ) -> None:
        raise AssertionError("Use `Session.create_cube()` to create a cube.")

    def __getitem__(self, key: str, /) -> _LocalCube_co:
        return self._get_cube(key)

    def _get_underlying(self) -> dict[str, _LocalCube_co]:
        return cast(dict[str, _LocalCube_co], self._get_cubes())

    def _delete_keys(self, keys: Optional[Iterable[str]] = None, /) -> None:
        keys = self._default_to_all_keys(keys)
        for key in keys:
            self._delete_cube(key)
