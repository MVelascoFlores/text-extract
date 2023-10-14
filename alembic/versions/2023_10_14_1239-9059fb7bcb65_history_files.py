"""history files

Revision ID: 9059fb7bcb65
Revises: 956a6f049f87
Create Date: 2023-10-14 12:39:57.067753

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9059fb7bcb65'
down_revision: Union[str, None] = '956a6f049f87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'files_history',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('fecha', sa.DateTime, default=sa.func.now()),
        sa.Column('pregunta', sa.Text, nullable=False),
        sa.Column('respuesta', sa.Text, nullable=False),
        sa.Column('file_id', sa.Integer, sa.ForeignKey('files.id', ondelete="CASCADE"),  nullable=False),
    )


def downgrade() -> None:
    op.drop_table('files_history')
