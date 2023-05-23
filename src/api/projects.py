"""
Contains the ``projects`` API blueprint.
"""

from ..models.projects import Project, Role, Team, User
from . import CollectionsAPIRouter

ProjectsRouter = CollectionsAPIRouter(
    prefix="/projects",
    tags=["projects"],
)

ProjectsRouter.add_collection(User)
ProjectsRouter.add_collection(Team)
ProjectsRouter.add_collection(Project)
ProjectsRouter.add_collection(Role)
