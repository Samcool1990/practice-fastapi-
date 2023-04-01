"""add content column to posts table

Revision ID: 06543d86b3d7
Revises: d7236052ab09
Create Date: 2023-04-01 17:07:16.661162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06543d86b3d7'
down_revision = 'd7236052ab09'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
