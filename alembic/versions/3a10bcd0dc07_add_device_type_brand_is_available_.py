"""add device_type brand is_available status fields

Revision ID: 3a10bcd0dc07
Revises: 5a3d726a2b89
Create Date: 2026-06-25 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '3a10bcd0dc07'
down_revision: Union[str, Sequence[str], None] = '5a3d726a2b89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('devices', sa.Column('device_type', sa.String(), nullable=True, server_default='laptop'))
    op.add_column('devices', sa.Column('brand', sa.String(), nullable=True))
    op.add_column('devices', sa.Column('is_available', sa.Boolean(), nullable=True, server_default='1'))
    op.add_column('devices', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('loans', sa.Column('status', sa.String(), nullable=True, server_default='active'))
    op.add_column('loans', sa.Column('created_at', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('loans', 'created_at')
    op.drop_column('loans', 'status')
    op.drop_column('devices', 'created_at')
    op.drop_column('devices', 'is_available')
    op.drop_column('devices', 'brand')
    op.drop_column('devices', 'device_type')