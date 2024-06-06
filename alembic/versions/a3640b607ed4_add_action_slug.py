"""add_action_slug

Revision ID: a3640b607ed4
Revises: 36e061278078
Create Date: 2024-06-01 13:33:11.459735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'a3640b607ed4'
down_revision: Union[str, None] = '36e061278078'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('core_actions', sa.Column('slug', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column('core_actions', sa.Column('short_description', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.alter_column('core_actions', 'description',
                    existing_type=sa.VARCHAR(),
                    nullable=True)
    op.execute("UPDATE core_actions SET short_description = ''")  # Set default value for existing rows
    op.alter_column('core_actions', 'short_description', nullable=False)  # Make the column NOT NULL
    op.create_index(op.f('ix_core_actions_slug'), 'core_actions', ['slug'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_core_actions_slug'), table_name='core_actions')
    op.alter_column('core_actions', 'description',
                    existing_type=sa.VARCHAR(),
                    nullable=False)
    op.drop_column('core_actions', 'short_description')
    op.drop_column('core_actions', 'slug')
