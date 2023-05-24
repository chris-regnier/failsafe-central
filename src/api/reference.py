"""
Contains the ``reference`` API blueprint.
"""

from framework.controller import CollectionsAPIRouter

from ..models.reference import Detection, Impact, Likelihood, Severity

ReferenceRouter = CollectionsAPIRouter(
    prefix="/reference",
    tags=["reference"],
)

ReferenceRouter.add_collection(Severity)
ReferenceRouter.add_collection(Likelihood)
ReferenceRouter.add_collection(Detection)
ReferenceRouter.add_collection(Impact)
