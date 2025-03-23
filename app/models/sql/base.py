from datetime import datetime
from typing import Annotated
import uuid

from sqlalchemy import BigInteger, DateTime, Integer, SmallInteger, text
from sqlalchemy.orm import DeclarativeBase, mapped_column, registry
from sqlalchemy.dialects.postgresql import UUID

from app.utils.custom_types import Int16, Int32, Int64

auto_uuid_pk = Annotated[uuid.UUID, mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    default=uuid.uuid4,
    server_default=text("gen_random_uuid()")
)]
auto_int_pk = Annotated[Int64, mapped_column(primary_key=True, autoincrement=True)]


class Base(DeclarativeBase):
    registry = registry(
        type_annotation_map={
            Int16: SmallInteger,
            Int32: Integer,
            Int64: BigInteger,
            datetime: DateTime(timezone=True),
        }
    )
