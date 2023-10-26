"""Add ForeignKey to TerpeneModel

Revision ID: 37720c6c0276
Revises: 2d035dfc33da
Create Date: 2023-08-31 00:49:03.906578

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37720c6c0276'
down_revision: Union[str, None] = '2d035dfc33da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
