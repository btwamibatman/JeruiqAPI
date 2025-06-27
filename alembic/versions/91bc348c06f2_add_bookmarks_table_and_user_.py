"""add bookmarks table and user relationship

Revision ID: 91bc348c06f2
Revises: 76b53d2a3c76
Create Date: 2025-06-26 17:39:47.648457

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91bc348c06f2'
down_revision: Union[str, Sequence[str], None] = '76b53d2a3c76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
