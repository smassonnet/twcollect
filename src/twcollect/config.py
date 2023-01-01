import pathlib
from typing import Dict, Type, TypeVar

import yaml
from pydantic import BaseModel

_T = TypeVar("_T", bound=BaseModel)


class CredentialsModel(BaseModel):

    __root__: Dict[str, str]


def parse_file_from_pydantic_model(path: pathlib.Path, model: Type[_T]) -> _T:
    with path.open() as cf:
        return model.parse_obj(yaml.safe_load(cf))


def parse_credentials_file(credentials_path: pathlib.Path) -> CredentialsModel:
    return parse_file_from_pydantic_model(credentials_path, CredentialsModel)
