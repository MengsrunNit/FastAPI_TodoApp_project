"""add phone number to the users Column

Revision ID: cff1cbd2c233
Revises: 
Create Date: 2024-08-17 22:24:44.166536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cff1cbd2c233'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    #op.add_column('users', sa.Column('phone_number', sa.String(), nullable = True))
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))




def downgrade() -> None:
    op.drop_column('users', 'phone_number')
