"""Add version column to flow table

Revision ID: b1c2d3e4f5a7
Revises: 4dfa692e02a7
Create Date: 2026-03-12 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b1c2d3e4f5a7"
down_revision = "4dfa692e02a7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "flow",
        sa.Column(
            "version",
            sa.Integer(),
            server_default="1",
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("flow", "version")
