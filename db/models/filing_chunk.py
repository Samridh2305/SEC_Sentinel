from datetime import date

from sqlalchemy import Date, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from pgvector.sqlalchemy import Vector

from db.database import Base


class FilingChunk(Base):

    __tablename__ = "filing_chunks"
    __table_args__ = (
        UniqueConstraint(
            "accession_number",
            "section",
            "chunk_index",
            name="uq_filing_chunks_accession_section_index",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    ticker: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    form_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    filing_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    accession_number: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    section: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    chunk_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=False
    )