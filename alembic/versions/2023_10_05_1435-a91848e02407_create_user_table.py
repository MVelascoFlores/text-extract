"""create user table

Revision ID: a91848e02407
Revises: 
Create Date: 2023-10-05 14:35:19.878225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a91848e02407'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('hashed_password', sa.String(150), nullable=False),
        sa.Column('is_active', sa.Boolean, default=True),
    )


def downgrade() -> None:
    op.drop_table('users')
