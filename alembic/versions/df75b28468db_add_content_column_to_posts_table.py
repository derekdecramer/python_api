"""add content column to posts table

Revision ID: df75b28468db
Revises: a73d673a16cf
Create Date: 2022-07-20 17:30:25.204853

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df75b28468db'
down_revision = 'a73d673a16cf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
