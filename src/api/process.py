"""
Contains the ``process`` API blueprint.
"""

from framework.controller import CollectionsAPIRouter

from ..models.process import Cause, Effect, Failure

ProcessRouter = CollectionsAPIRouter(
    prefix="/process",
    tags=["process"],
)

ProcessRouter.add_collection(Failure)
ProcessRouter.add_collection(Cause)
ProcessRouter.add_collection(Effect)
