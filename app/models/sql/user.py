from datetime import datetime
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.dto.user import UserDto
from app.utils.custom_types import Int64

from .base import Base, auto_int_pk
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    user_id: Mapped[auto_int_pk]
    telegram_id: Mapped[Int64] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    username: Mapped[str | None] = mapped_column(nullable=True)
    language: Mapped[str] = mapped_column(String(length=2))
    language_code: Mapped[Optional[str]] = mapped_column()
    is_superuser: Mapped[bool] = mapped_column(
        default=False, server_default='false', nullable=False
    )
    is_bot_blocked: Mapped[bool] = mapped_column(
        default=False, server_default='false', nullable=False
    )
    blocked_at: Mapped[Optional[datetime]] = mapped_column()

    def dto(self) -> UserDto:
        return UserDto.model_validate(self)
