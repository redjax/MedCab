"""Add decimal precision to floats

Revision ID: 2d035dfc33da
Revises: e1c833ab705a
Create Date: 2023-08-31 00:46:42.677917

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d035dfc33da'
down_revision: Union[str, None] = 'e1c833ab705a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
