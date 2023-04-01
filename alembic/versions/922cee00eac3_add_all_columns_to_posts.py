"""add all columns to posts

Revision ID: 922cee00eac3
Revises: 0e76012aac5f
Create Date: 2023-04-01 17:27:02.953656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '922cee00eac3'
down_revision = '0e76012aac5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default="TRUE"),
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))),) # type: ignore
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
