from datetime import datetime
from typing import Optional
from pydantic import Field
from sqlmodel import Relationship, SQLModel


class BaseModel(SQLModel):
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class BaseDescriptorModel(BaseModel):
    name: str
    description: Optional[str] = None


class Team(BaseDescriptorModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class Project(BaseDescriptorModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class User(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    name: str
    email: str
    last_login: datetime = None
    is_admin: bool = False

    class Config:
        orm_mode = True


class Role(BaseDescriptorModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    short_name: Optional[str] = None
    external_roles: Optional[str] = None


class UserTeamLink(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    team_id: int = Field(default=None, foreign_key="teams.id")
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")


class ProjectTeamLink(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    project_id: int = Field(default=None, foreign_key="projects.id")
    team_id: int = Field(default=None, foreign_key="teams.id")


class Failure(BaseDescriptorModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class Cause(BaseDescriptorModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class Effect(BaseDescriptorModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class BaseRankModel(BaseModel):
    name: str
    description: str
    value: int
    example: str

    class Config:
        orm_mode = True


class Severity(BaseRankModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class Likelihood(BaseRankModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class Detection(BaseRankModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)


class Impact(BaseRankModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
