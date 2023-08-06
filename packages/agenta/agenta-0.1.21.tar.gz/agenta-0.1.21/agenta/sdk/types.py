import json
from typing import Any, Dict, List

from pydantic import BaseModel, Extra


class InFile:
    def __init__(self, file_name: str, file_path: str):
        self.file_name = file_name
        self.file_path = file_path


class TextParam(str):
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update({"x-parameter": "text"})


class FloatParam(float):
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update({"x-parameter": "float"})




class MultipleChoiceParam(str):
    def __new__(cls, choices: list = [], default: str = None):
        
        if default is None and choices:
            # if a default value is not provided,
            # uset the first value in the choices list
            default = choices[0]
        
        if default is None and not choices:
            # raise error if no default value or choices is provided
            raise ValueError(
                "You must provide either a default value or choices"
            )
            
        instance = super().__new__(cls, default)
        instance.choices = choices
        return instance

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]):
        field_schema.update(
            {
                "x-parameter": "choice",
                "type": "string",
                "enum": [],
            }
        )


class Context(BaseModel):
    class Config:
        extra = Extra.allow

    def to_json(self):
        return self.json()

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(**data)
