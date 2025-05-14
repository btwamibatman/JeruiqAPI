"""Add name and phone_number to users table

Revision ID: 14d99f0a3a4e
Revises: 0f3e3a0e2235
Create Date: 2025-05-14 16:32:27.076696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '14d99f0a3a4e'
down_revision: Union[str, None] = '0f3e3a0e2235'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
