import enum
import typing
import importlib.resources

from hat import json


conf_schema_id: str = 'dtviz://main.yaml#'

with importlib.resources.path(__package__, 'json_schema_repo.json') as _path:
    json_schema_repo: json.SchemaRepository = json.SchemaRepository(
        json.json_schema_repo,
        json.SchemaRepository.from_json(_path))


class ProjectType(enum.Enum):
    PYPROJECT_TOML = 'pyproject.toml'
    PACKAGE_JSON = 'package.json'


class Project(typing.NamedTuple):
    type: ProjectType
    name: str
    version: str | None
    refs: typing.List['ProjectRef']


class ProjectRef(typing.NamedTuple):
    project: str
    version: str | None
    dev: bool
