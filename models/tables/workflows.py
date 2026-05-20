from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, DateTime, Float, Integer, String, Text, ForeignKey
from typing import Optional
from datetime import datetime

from database.database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), default="test", index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    details: Mapped[list["WorkflowDetails"]] = relationship(
        "WorkflowDetails",
        back_populates="workflow",
        cascade="all, delete-orphan"
    )


class WorkflowDetails(Base):
    __tablename__ = "workflow_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workflow_id: Mapped[int] = mapped_column(Integer,ForeignKey("workflows.id"),index=True, nullable=False)
    version: Mapped[str] = mapped_column(String(10), primary_key=True, nullable=False)
    data: Mapped[dict] = mapped_column(JSON, nullable=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    agents:Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    task_sequence : Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    run_logs : Mapped[dict] = mapped_column(JSON, nullable=True, default=dict)


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by: Mapped[str] = mapped_column(String(255), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    workflow: Mapped["Workflow"] = relationship(
        "Workflow",
        back_populates="details"
    )
