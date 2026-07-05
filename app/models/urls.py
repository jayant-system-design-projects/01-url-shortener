from sqlalchemy import Index, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4
from datetime import datetime, timezone
from app.database import Base


from datetime import datetime, timezone
from sqlalchemy import DateTime


class TimeDateMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class URLS(TimeDateMixin, Base):
    __tablename__ = "urls"
    __table_args__ = (
        Index("idx_shortcode", "short_code", unique=True),
        {"schema": "my_url_shortener"},
    )
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    short_code: Mapped[str] = mapped_column(String(50), nullable=False)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
