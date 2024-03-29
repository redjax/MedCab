"""${commit_msg}

Revision ID: 370b44b6f787
Revises: f1a558f8eda0
Create Date: 2023-12-10 22:18:33.437868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '370b44b6f787'
down_revision: Union[str, None] = 'f1a558f8eda0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('favorite', sa.Boolean(), nullable=False, server_default=False))
    op.drop_index('ix_product_family', table_name='product')
    op.drop_index('ix_product_form', table_name='product')
    op.drop_index('ix_product_id', table_name='product')
    op.drop_index('ix_product_strain', table_name='product')
    op.drop_table('product')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.CHAR(length=32), nullable=False),
    sa.Column('strain', sa.VARCHAR(), nullable=False),
    sa.Column('family', sa.VARCHAR(), nullable=False),
    sa.Column('form', sa.VARCHAR(), nullable=False),
    sa.Column('total_thc', sa.NUMERIC(precision=3), nullable=True),
    sa.Column('total_cbd', sa.NUMERIC(precision=3), nullable=True),
    sa.Column('weight', sa.NUMERIC(precision=3), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_product_strain', 'product', ['strain'], unique=False)
    op.create_index('ix_product_id', 'product', ['id'], unique=False)
    op.create_index('ix_product_form', 'product', ['form'], unique=False)
    op.create_index('ix_product_family', 'product', ['family'], unique=False)
    # ### end Alembic commands ###
