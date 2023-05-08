from datetime import datetime
from typing import Optional
from fastapi import APIRouter
from sqlmodel import Session

from src.models import Detection, Impact, Likelihood, Severity
from .. import engine

ReferenceRouter = APIRouter()


__REFERENCE_MODELS__ = {
    Severity.__tablename__: Severity,
    Likelihood.__tablename__: Likelihood,
    Detection.__tablename__: Detection,
    Impact.__tablename__: Impact,
}


@ReferenceRouter.get("/{severities}")
async def get_severities(name: Optional[str] = None):
    with Session(engine) as session:
        query = session.query(Severity)
        if name:
            query = query.filter(Severity.name == name)
        severities = query.all()
        return severities


@ReferenceRouter.get("/severities/{severity_id}")
async def get_severity(severity_id: int):
    with Session(engine) as session:
        severity = session.get(Severity, severity_id)
        return severity


@ReferenceRouter.post("/severities")
async def create_severity(severity: Severity):
    with Session(engine) as session:
        session.add(severity)
        session.commit()
        session.refresh(severity)
        return severity


@ReferenceRouter.put("/severities/{severity_id}")
async def update_severity(severity_id: int, severity: Severity):
    with Session(engine) as session:
        existing_severity = session.get(Severity, severity_id)
        if existing_severity:
            session.update(severity)
            session.commit()
            session.refresh(severity)
            return severity
        raise ValueError(f"Severity with id {severity_id} not found")


@ReferenceRouter.delete("/severities/{severity_id}")
async def delete_severity(severity_id: int):
    with Session(engine) as session:
        severity = session.get(Severity, severity_id)
        if severity:
            severity.deleted_at = datetime.utcnow()
            session.update(severity)
            session.commit()
            return {"message": "Severity soft deleted"}
        raise ValueError(f"Severity with id {severity_id} not found")
