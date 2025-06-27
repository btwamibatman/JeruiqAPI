"""add bookmarks table and user relationship

Revision ID: 76b53d2a3c76
Revises: f75ff95de50e
Create Date: 2025-06-26 17:20:09.452966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '76b53d2a3c76'
down_revision: Union[str, Sequence[str], None] = 'f75ff95de50e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
