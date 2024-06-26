"""initial_migration

Revision ID: ec37f55d6ff5
Revises: 
Create Date: 2024-05-31 14:12:50.356330

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ec37f55d6ff5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('core_actions',
                    sa.Column('action_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('tags', sa.JSON(), nullable=True),
                    sa.Column('input_parameters', sa.JSON(), nullable=True),
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('visibility', sa.Enum('public', 'private', name='visibility'), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_core_actions_action_name'), 'core_actions', ['action_name'], unique=False)
    op.create_table('core_users',
                    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('organization_id', sa.UUID(), nullable=True),
                    sa.Column('picture', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('nickname', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('email_verified', sa.Boolean(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_core_users_email'), 'core_users', ['email'], unique=True)
    op.create_index(op.f('ix_core_users_name'), 'core_users', ['name'], unique=True)
    op.create_table('core_jobs',
                    sa.Column('action_id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('user_id', sqlmodel.sql.sqltypes.GUID(), nullable=True),
                    sa.Column('inputs', sa.JSON(), nullable=True),
                    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
                    sa.Column('id', sqlmodel.sql.sqltypes.GUID(), nullable=False),
                    sa.Column('internal_id', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
                    sa.Column('output', sa.JSON(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), nullable=False),
                    sa.ForeignKeyConstraint(['action_id'], ['core_actions.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['core_users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_core_jobs_action_id'), 'core_jobs', ['action_id'], unique=False)
    op.create_index(op.f('ix_core_jobs_internal_id'), 'core_jobs', ['internal_id'], unique=False)
    op.create_index(op.f('ix_core_jobs_user_id'), 'core_jobs', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_core_jobs_user_id'), table_name='core_jobs')
    op.drop_index(op.f('ix_core_jobs_internal_id'), table_name='core_jobs')
    op.drop_index(op.f('ix_core_jobs_action_id'), table_name='core_jobs')
    op.drop_table('core_jobs')
    op.drop_index(op.f('ix_core_users_name'), table_name='core_users')
    op.drop_index(op.f('ix_core_users_email'), table_name='core_users')
    op.drop_table('core_users')
    op.drop_index(op.f('ix_core_actions_action_name'), table_name='core_actions')
    op.drop_table('core_actions')
