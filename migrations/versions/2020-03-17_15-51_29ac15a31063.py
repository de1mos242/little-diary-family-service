"""add uuid to family and member

Revision ID: 29ac15a31063
Revises: d8e0aed930c7
Create Date: 2020-03-17 15:51:08.126814+00:00

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '29ac15a31063'
down_revision = 'd8e0aed930c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('family', sa.Column('family_uuid', postgresql.UUID(), nullable=False))
    op.create_unique_constraint(None, 'family', ['family_uuid'])
    op.add_column('family_member', sa.Column('member_uuid', postgresql.UUID(), nullable=False))
    op.drop_constraint('family_member_user_uuid_key', 'family_member', type_='unique')
    op.create_unique_constraint(None, 'family_member', ['member_uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'family_member', type_='unique')
    op.create_unique_constraint('family_member_user_uuid_key', 'family_member', ['user_uuid'])
    op.drop_column('family_member', 'member_uuid')
    op.drop_constraint(None, 'family', type_='unique')
    op.drop_column('family', 'family_uuid')
    # ### end Alembic commands ###
