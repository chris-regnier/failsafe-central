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


TeamModel = type("TeamModel", (BaseDescriptorModel,), dict(__tablename__="teams"))
ProjectModel = type(
    "ProjectModel", (BaseDescriptorModel,), dict(__tablename__="projects")
)


class UserModel(BaseModel):
    name: str
    email: str
    last_login: datetime = None
    is_admin: bool = False

    class Config:
        orm_mode = True


class RoleModel(BaseDescriptorModel):
    short_name: Optional[str] = None
    external_roles: Optional[str] = None


class LinkUserToTeamModel(BaseModel):
    user_id: int = Field(default=None, foreign_key="users.id")
    team_id: int = Field(default=None, foreign_key="teams.id")
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")


class LinkProjectToTeamModel(BaseModel):
    project_id: int = Field(default=None, foreign_key="projects.id")
    team_id: int = Field(default=None, foreign_key="teams.id")


FailureModel = type(
    "FailureModel", (BaseDescriptorModel,), dict(__tablename__="failures")
)
CauseModel = type("CauseModel", (BaseDescriptorModel,), dict(__tablename__="causes"))
EffectModel = type("EffectModel", (BaseDescriptorModel,), dict(__tablename__="effects"))


class BaseRankModel(BaseModel):
    name: str
    description: str
    value: int
    example: str

    class Config:
        orm_mode = True


SeverityModel = type(
    "SeverityModel", (BaseRankModel,), dict(__tablename__="severities")
)
LikelihoodModel = type(
    "LikelihoodModel", (BaseRankModel,), dict(__tablename__="likelihoods")
)
DetectionModel = type(
    "DetectionModel", (BaseRankModel,), dict(__tablename__="detections")
)
ImpactModel = type("ImpactModel", (BaseRankModel,), dict(__tablename__="impacts"))
