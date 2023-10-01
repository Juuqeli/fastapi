"""add columns to posts table

Revision ID: 4aff272674a3
Revises: 3e2007ca8cd0
Create Date: 2023-08-03 23:50:58.586321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4aff272674a3'
down_revision = '3e2007ca8cd0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
