from datetime import datetime
from typing import Optional
from pydantic import create_model
from sqlmodel import Field, SQLModel
from sqlmodel.main import SQLModelMetaclass

from inflection import tableize

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
        field_annotations_dict = {
            field: (cls.__fields__[field].type_, cls.__fields__[field].default)
            for field in dict.keys(cls.__fields__)
            if field not in cls._INPUT_MODEL_EXCLUDED_FIELDS
        }

        # need to create a new class to avoid metaclass conflicts and allow input
        # models to be used in FastAPI endpoints
        return create_model(
            f"{cls.__name__}Input",
            __config__=cls.Config,
            **field_annotations_dict,
        )


class BaseDescriptorModel(BaseModel):
    name: str
    description: Optional[str] = None


class Team(BaseDescriptorModel, table=True):
    pass


class Project(BaseDescriptorModel, table=True):
    pass


class User(BaseModel, table=True):
    name: str
    email: str
    last_login: datetime = None
    is_admin: bool = False


class Role(BaseDescriptorModel, table=True):
    short_name: Optional[str] = None
    external_roles: Optional[str] = None


class UserTeamLink(BaseModel, table=True):
    user_id: int = Field(default=None, foreign_key="users.id")
    team_id: int = Field(default=None, foreign_key="teams.id")
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")


class ProjectTeamLink(BaseModel, table=True):
    project_id: int = Field(default=None, foreign_key="projects.id")
    team_id: int = Field(default=None, foreign_key="teams.id")


class Failure(BaseDescriptorModel, table=True):
    pass


class Cause(BaseDescriptorModel, table=True):
    pass


class Effect(BaseDescriptorModel, table=True):
    pass


class BaseRankModel(BaseModel):
    name: str
    description: str
    value: int
    example: str


class Severity(BaseRankModel, table=True):
    pass


class Likelihood(BaseRankModel, table=True):
    pass


class Detection(BaseRankModel, table=True):
    pass


class Impact(BaseRankModel, table=True):
    pass
