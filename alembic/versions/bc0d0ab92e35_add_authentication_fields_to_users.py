"""add authentication fields to users

Revision ID: bc0d0ab92e35
Revises: 3a10bcd0dc07
Create Date: 2026-06-26 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'bc0d0ab92e35'
down_revision: Union[str, Sequence[str], None] = '3a10bcd0dc07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass