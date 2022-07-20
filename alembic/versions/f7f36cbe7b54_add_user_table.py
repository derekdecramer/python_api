"""Add user table

Revision ID: f7f36cbe7b54
Revises: df75b28468db
Create Date: 2022-07-20 17:35:23.355028

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f7f36cbe7b54'
down_revision = 'df75b28468db'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
    )
    
    pass


def downgrade():
    op.drop_table("users")
    pass
