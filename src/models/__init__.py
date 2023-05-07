from datetime import datetime
from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel


class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime
    updated_at: datetime = None
    deleted_at: datetime = None

    class Config:
        orm_mode = True


class BaseDescriptorModel(BaseModel):
    name: str
    description: Optional[str] = None


class TeamModel(BaseDescriptorModel, table=True):
    pass


class ProjectModel(BaseDescriptorModel, table=True):
    pass


class UserModel(BaseModel, table=True):
    name: str
    email: str
    last_login: datetime = None
    is_admin: bool = False

    class Config:
        orm_mode = True


class RoleModel(BaseDescriptorModel, table=True):
    short_name: Optional[str] = None
    external_roles: Optional[str] = None


class LinkUserToTeamModel(BaseModel, table=True):
    user_id: int = Field(default=None, foreign_key="users.id")
    team_id: int = Field(default=None, foreign_key="teams.id")
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")


class LinkProjectToTeamModel(BaseModel, table=True):
    project_id: int = Field(default=None, foreign_key="projects.id")
    team_id: int = Field(default=None, foreign_key="teams.id")


class FailureModel(BaseDescriptorModel, table=True):
    pass


class CauseModel(BaseDescriptorModel, table=True):
    pass


class EffectModel(BaseDescriptorModel, table=True):
    pass


class BaseRankModel(BaseModel):
    name: str
    description: str
    value: int
    example: str

    class Config:
        orm_mode = True


class SeverityModel(BaseRankModel, table=True):
    pass


class LikelihoodModel(BaseRankModel, table=True):
    pass


class DetectionModel(BaseRankModel, table=True):
    pass


class ImpactModel(BaseRankModel, table=True):
    pass
