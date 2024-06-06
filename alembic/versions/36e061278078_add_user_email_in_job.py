"""add_user_email_in_job

Revision ID: 36e061278078
Revises: ae882b0a58ff
Create Date: 2024-06-01 13:22:12.202304

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel
# revision identifiers, used by Alembic.
revision: str = '36e061278078'
down_revision: Union[str, None] = 'ae882b0a58ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('core_jobs', sa.Column('user_email', sqlmodel.sql.sqltypes.AutoString(), nullable=True))


def downgrade() -> None:
    op.drop_column('core_jobs', 'user_email')
