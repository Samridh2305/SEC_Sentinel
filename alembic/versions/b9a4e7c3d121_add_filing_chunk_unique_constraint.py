"""add unique filing chunk identity

Revision ID: b9a4e7c3d121
Revises: f71eee62be47
Create Date: 2026-08-17
"""

from alembic import op


revision = "b9a4e7c3d121"
down_revision = "f71eee62be47"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Preserve the oldest row for each chunk identity so existing duplicate
    # ingestion runs do not prevent the uniqueness constraint from being added.
    op.execute(
        """
        DELETE FROM filing_chunks AS duplicate
        USING filing_chunks AS original
        WHERE duplicate.id > original.id
          AND duplicate.accession_number = original.accession_number
          AND duplicate.section = original.section
          AND duplicate.chunk_index = original.chunk_index
        """
    )
    op.create_unique_constraint(
        "uq_filing_chunks_accession_section_index",
        "filing_chunks",
        ["accession_number", "section", "chunk_index"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_filing_chunks_accession_section_index",
        "filing_chunks",
        type_="unique",
    )
