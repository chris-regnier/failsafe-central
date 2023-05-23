"""
Contains the ``process`` API blueprint.
"""

from ..models.process import Cause, Effect, Failure
from . import CollectionsAPIRouter

ProcessRouter = CollectionsAPIRouter(
    prefix="/process",
    tags=["process"],
)

ProcessRouter.add_collection(Failure)
ProcessRouter.add_collection(Cause)
ProcessRouter.add_collection(Effect)
