from alembic import op
import sqlalchemy as sa

# ID миграции
revision = "20240206123456"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Создаём таблицу пользователей"""
    op.create_table(
        "users",
        sa.Column("user_id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=True),
        sa.Column("role", sa.String(), default="user"),  # Роль хранится как строка
    )

def downgrade():
    """Удаляем таблицу пользователей"""
    op.drop_table("users")
