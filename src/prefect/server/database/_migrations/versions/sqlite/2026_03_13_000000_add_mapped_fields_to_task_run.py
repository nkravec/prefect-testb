"""Add mapped and map_index columns to task_run table

Revision ID: c2d3e4f5a6b9
Revises: 4dfa692e02a7
Create Date: 2026-03-13 00:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "c2d3e4f5a6b9"
down_revision = "4dfa692e02a7"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "task_run",
        sa.Column(
            "mapped",
            sa.Boolean(),
            server_default="false",
            nullable=False,
        ),
    )
    op.add_column(
        "task_run",
        sa.Column(
            "map_index",
            sa.Integer(),
            server_default="-1",
            nullable=False,
        ),
    )


def downgrade():
    op.drop_column("task_run", "map_index")
    op.drop_column("task_run", "mapped")
