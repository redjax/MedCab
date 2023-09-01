"""Set terpenes to optional on ProductModel

Revision ID: 3a2455683aa2
Revises: f0940b4419c2
Create Date: 2023-09-01 01:21:36.956431

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a2455683aa2'
down_revision: Union[str, None] = 'f0940b4419c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
