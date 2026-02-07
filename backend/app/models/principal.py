# principal.py - Principal/Admin Model
#
# Administrative user with school-wide access.

import uuid
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import date

from app.core.database import Base
from app.models.base import UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.school import School


class Principal(Base, UUIDMixin, TimestampMixin):
    """
    Principal model with administrative information.

    Linked to a User for authentication and to a School for management.
    """
    __tablename__ = "principals"

    # Foreign keys
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    school_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("schools.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Principal-specific fields
    employee_id: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True
    )
    qualification: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    date_of_joining: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    years_of_experience: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="principal")
    school: Mapped[Optional["School"]] = relationship("School", back_populates="principals")

    def __repr__(self) -> str:
        return f"<Principal(id={self.id}, employee_id={self.employee_id})>"
