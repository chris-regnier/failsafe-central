from datetime import datetime
from typing import Optional
from sqlmodel import Field

from .base import BaseModel, BaseDescriptorModel


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
