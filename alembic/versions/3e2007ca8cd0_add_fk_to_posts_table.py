"""add fk to posts table

Revision ID: 3e2007ca8cd0
Revises: ec2ce169b7dd
Create Date: 2023-08-03 23:40:38.428190

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3e2007ca8cd0'
down_revision = 'ec2ce169b7dd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'],
                          remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
