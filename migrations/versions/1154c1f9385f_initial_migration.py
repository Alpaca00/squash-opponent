"""Initial migration.

Revision ID: 1154c1f9385f
Revises: 
Create Date: 2021-12-10 16:54:23.239373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1154c1f9385f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('queues_opponents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('queue_name', sa.String(length=50), nullable=True),
    sa.Column('queue_email', sa.String(length=50), nullable=True),
    sa.Column('queue_phone', sa.String(length=50), nullable=True),
    sa.Column('queue_category', sa.String(length=50), nullable=True),
    sa.Column('queue_city', sa.String(length=50), nullable=True),
    sa.Column('queue_district', sa.String(length=50), nullable=True),
    sa.Column('queue_date', sa.String(length=50), nullable=True),
    sa.Column('queue_accept', sa.Boolean(), nullable=True),
    sa.Column('queue_message', sa.Text(), nullable=True),
    sa.Column('queue_offer_opponent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['queue_offer_opponent_id'], ['offers_opponents.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users_accounts', sa.Column('count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users_accounts', 'count')
    op.drop_table('queues_opponents')
    # ### end Alembic commands ###