"""empty message

Revision ID: fd7692a8f6d6
Revises: d653458a8d85
Create Date: 2021-07-22 12:45:59.283706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd7692a8f6d6'
down_revision = 'd653458a8d85'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_product', sa.String(), nullable=False),
    sa.Column('print', sa.String(), nullable=False),
    sa.Column('order_total', sa.Float(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders')
    # ### end Alembic commands ###
