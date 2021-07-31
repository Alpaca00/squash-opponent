"""empty message

Revision ID: 07931d3c0569
Revises: 9f3017e13d27
Create Date: 2021-07-30 18:24:48.998291

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07931d3c0569'
down_revision = '9f3017e13d27'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('roles_users',
    sa.Column('user_account_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_account_id'], ['users_accounts.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('role')
    # ### end Alembic commands ###