from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import JSON, DateTime, Float, Integer, String, Text
from typing import Optional

from database.database import Base

class Agents(Base):
    __tablename__ = "agents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)