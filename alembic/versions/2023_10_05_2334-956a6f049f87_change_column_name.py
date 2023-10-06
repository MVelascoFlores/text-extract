"""change column name

Revision ID: 956a6f049f87
Revises: e55391915ed4
Create Date: 2023-10-05 23:34:29.891404

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '956a6f049f87'
down_revision: Union[str, None] = 'e55391915ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        'files',
        'files_name',
        new_column_name='file_name'
    )


def downgrade() -> None:
    op.alter_column(
        'files',
        'file_name',
        new_column_name='files_name'
    )

