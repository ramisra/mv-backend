"""add_user_token_migration

Revision ID: ae882b0a58ff
Revises: ec37f55d6ff5
Create Date: 2024-06-01 11:12:56.564844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'ae882b0a58ff'
down_revision: Union[str, None] = 'ec37f55d6ff5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('core_users', sa.Column('user_token', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('core_users', 'user_token')
