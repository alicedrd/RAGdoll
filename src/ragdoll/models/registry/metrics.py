from datetime import datetime
from sqlalchemy import DateTime, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from .decl_base import AppDeclarativeBase

class ReqMetricReport(AppDeclarativeBase):
    __tablename__ = "metrics_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    context_precision: Mapped[float] = mapped_column(Float, nullable=False)
    context_recall: Mapped[float] = mapped_column(Float, nullable=False)
    faithfulness: Mapped[float] = mapped_column(Float, nullable=False)
    answer_relevancy: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

