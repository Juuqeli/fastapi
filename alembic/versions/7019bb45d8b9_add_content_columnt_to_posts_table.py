"""add  content columnt to posts table

Revision ID: 7019bb45d8b9
Revises: 6f2d11685257
Create Date: 2023-08-03 23:20:21.744500

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7019bb45d8b9'
down_revision = '6f2d11685257'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
