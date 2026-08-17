"""create ingestion jobs

Revision ID: c4d9e8f7a012
Revises: b9a4e7c3d121
Create Date: 2026-08-17
"""

import sqlalchemy as sa
from alembic import op


revision = "c4d9e8f7a012"
down_revision = "b9a4e7c3d121"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ingestion_jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("ticker", sa.String(length=10), nullable=False),
        sa.Column("form_type", sa.String(length=10), nullable=False),
        sa.Column("requested_filing_date", sa.String(length=10), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("accession_number", sa.String(length=30), nullable=True),
        sa.Column("chunks_created", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ingestion_jobs_status", "ingestion_jobs", ["status"])


def downgrade() -> None:
    op.drop_index("ix_ingestion_jobs_status", table_name="ingestion_jobs")
    op.drop_table("ingestion_jobs")
