from pathlib import Path, PurePosixPath
from shutil import copytree
from tempfile import mkdtemp

from .app_extension import _APP_EXTENSIONS_DIRECTORY

_BRANDING_EXTENSION_NAME = "@atoti/branding-extension"

_SOURCE_EXTENSION_DIRECTORY = _APP_EXTENSIONS_DIRECTORY / PurePosixPath(
    _BRANDING_EXTENSION_NAME
)

_TITLE_PLACEHOLDER = "APPLICATION_NAME_PLACEHOLDER"


def create_branding_extension(*, title: str) -> dict[str, Path]:
    path = Path(mkdtemp(prefix="atoti-branding-extension-"))
    copytree(_SOURCE_EXTENSION_DIRECTORY, path, dirs_exist_ok=True)
    chunk_path = next(path.glob("**/*.chunk.js"))
    chunk_source = chunk_path.read_text(encoding="utf8")
    assert _TITLE_PLACEHOLDER in chunk_source
    chunk_source = chunk_source.replace(_TITLE_PLACEHOLDER, title)
    chunk_path.write_text(chunk_source, encoding="utf8")
    return {_BRANDING_EXTENSION_NAME: path}
