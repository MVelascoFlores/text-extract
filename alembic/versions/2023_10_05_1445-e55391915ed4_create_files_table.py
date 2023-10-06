"""Create files table

Revision ID: e55391915ed4
Revises: a91848e02407
Create Date: 2023-10-05 14:45:42.292678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e55391915ed4'
down_revision: Union[str, None] = 'a91848e02407'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'files',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('files_name', sa.String(150), nullable=False),
        sa.Column('index_path', sa.String(150), nullable=False),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('files')
