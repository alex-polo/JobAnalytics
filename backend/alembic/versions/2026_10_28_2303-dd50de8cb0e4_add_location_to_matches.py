"""add location to matches

Revision ID: dd50de8cb0e4
Revises: ebfd05808cb4
Create Date: 2026-10-28 23:03:31.344777

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "dd50de8cb0e4"
down_revision: str | Sequence[str] | None = "ebfd05808cb4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Создаём enum-тип вручную
    op.execute(
        "CREATE TYPE location_item_enum AS ENUM "
        "('remote', 'office', 'gibrid')"
    )

    # 2. Добавляем колонку с server_default, чтобы NOT NULL прошёл на старых строках
    location_enum = postgresql.ENUM(
        'remote', 'office', 'gibrid',
        name='location_item_enum',
        create_type=False,   # тип уже создан выше
    )
    op.add_column(
        "resume_match_results",
        sa.Column(
            "location",
            location_enum,
            nullable=False,
            server_default="remote",
        ),
    )

    # 3. Убираем server_default — новые строки должны задавать location явно
    op.alter_column("resume_match_results", "location", server_default=None)

    # 4. Индекс и удаление старой колонки
    op.create_index(
        op.f("ix_resume_match_results_location"),
        "resume_match_results",
        ["location"],
        unique=False,
    )
    op.drop_column("resume_match_results", "is_remote")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "resume_match_results",
        sa.Column(
            "is_remote",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_index(
        op.f("ix_resume_match_results_location"),
        table_name="resume_match_results",
    )
    op.drop_column("resume_match_results", "location")
    op.execute("DROP TYPE location_item_enum")