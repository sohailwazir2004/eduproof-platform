# parent.py - Parent Model
#
# Parent-specific model linked to User.
# Can have multiple children (students).

import uuid
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.student import Student


class Parent(Base, UUIDMixin, TimestampMixin):
    """
    Parent model with contact information.

    Linked to a User for authentication and to Students as children.
    """
    __tablename__ = "parents"

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )

    # Parent-specific fields
    occupation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    work_phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    emergency_contact: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    relationship_type: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        default="parent"
    )  # "father", "mother", "guardian"

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="parent")
    children: Mapped[List["Student"]] = relationship(
        "Student",
        back_populates="parent"
    )

    def __repr__(self) -> str:
        return f"<Parent(id={self.id})>"
