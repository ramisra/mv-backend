"""add_action_name

Revision ID: 96907c232c78
Revises: a3640b607ed4
Create Date: 2024-06-01 13:38:26.158060

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel
# revision identifiers, used by Alembic.
revision: str = '96907c232c78'
down_revision: Union[str, None] = 'a3640b607ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('core_actions', sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('core_actions', 'name')
