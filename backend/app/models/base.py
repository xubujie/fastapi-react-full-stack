from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Base(SQLModel):
    """Base model for all database models"""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
