from datetime import datetime
from typing import Optional

from inflection import tableize
from pydantic import create_model
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelMetaclass

BASE_INPUT_EXCLUDED_FIELDS = ("id", "deleted_at", "updated_at", "created_at")
BASE_OUTPUT_EXCLUDED_FIELDS = ("deleted_at",)


class BaseSQLModelMetaclass(SQLModelMetaclass):
    def __new__(mcls, name, bases, namespace, **kwargs):
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        if not hasattr(cls, "Config"):
            cls.Config = type("Config", (), {})
        if not hasattr(cls.Config, "exclude"):
            cls.Config.exclude = []
        for field in BASE_OUTPUT_EXCLUDED_FIELDS:
            if field not in cls.Config.exclude:
                cls.Config.exclude.append(field)
        cls.__exclude_fields__ = set(cls.Config.exclude)
        cls.__tablename__ = tableize(cls.__name__)
        return cls


class BaseModel(SQLModel, metaclass=BaseSQLModelMetaclass):
    _INPUT_MODEL_EXCLUDED_FIELDS = BASE_INPUT_EXCLUDED_FIELDS

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    created_at: datetime = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)
    deleted_at: Optional[datetime] = Field(default=None)

    @classmethod
    def input_model(cls):
        if not hasattr(cls, "_input_model"):
            field_annotations_dict = {
                field: (cls.__fields__[field].type_, cls.__fields__[field].default)
                for field in dict.keys(cls.__fields__)
                if field not in cls._INPUT_MODEL_EXCLUDED_FIELDS
            }

            # need to create a new class to avoid metaclass conflicts and allow input
            # models to be used in FastAPI endpoints
            cls._input_model = create_model(
                f"{cls.__name__}Input",
                __config__=cls.Config,
                **field_annotations_dict,
            )
        return cls._input_model


class BaseDescriptorModel(BaseModel):
    name: str
    description: Optional[str] = None
