"""empty message

Revision ID: 2e9368d958e4
Revises: 66d092ce9a5a
Create Date: 2021-08-05 23:05:44.432622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e9368d958e4'
down_revision = '66d092ce9a5a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gallery', sa.Column('data', sa.LargeBinary(), nullable=True))
    op.alter_column('gallery', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint('gallery_link_key', 'gallery', type_='unique')
    op.drop_column('gallery', 'link')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('gallery', sa.Column('link', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.create_unique_constraint('gallery_link_key', 'gallery', ['link'])
    op.alter_column('gallery', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.drop_column('gallery', 'data')
    # ### end Alembic commands ###