"""add_action_function_name

Revision ID: 424fd9982066
Revises: 96907c232c78
Create Date: 2024-06-01 13:40:37.321170

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = '424fd9982066'
down_revision: Union[str, None] = '96907c232c78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('core_actions',
                  sa.Column('internal_function_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_index('ix_core_actions_action_name', table_name='core_actions')
    op.drop_column('core_actions', 'title')
    op.drop_column('core_actions', 'action_name')


def downgrade() -> None:
    op.add_column('core_actions', sa.Column('action_name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('core_actions', sa.Column('title', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_index('ix_core_actions_action_name', 'core_actions', ['action_name'], unique=False)
    op.drop_column('core_actions', 'internal_function_name')
