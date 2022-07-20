"""add last few columns to post table

Revision ID: 851c254fc875
Revises: e428a582b58d
Create Date: 2022-07-20 17:58:34.531271

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '851c254fc875'
down_revision = 'e428a582b58d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column("posts", sa.Column("created_at", sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text("NOW()")),)
    
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
