from datetime import datetime
from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class AppDeclarativeBase(DeclarativeBase):
    pass

class DocRecord(AppDeclarativeBase):
    __tablename__ = "documents"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    doc_name: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    size_in_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

