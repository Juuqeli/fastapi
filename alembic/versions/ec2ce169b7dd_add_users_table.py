"""add users table

Revision ID: ec2ce169b7dd
Revises: 7019bb45d8b9
Create Date: 2023-08-03 23:31:27.262931

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec2ce169b7dd'
down_revision = '7019bb45d8b9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
