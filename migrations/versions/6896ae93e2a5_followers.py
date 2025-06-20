"""followers

Revision ID: 6896ae93e2a5
Revises: 948db0aecd7b
Create Date: 2025-06-17 15:03:37.252178

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6896ae93e2a5'
down_revision = '948db0aecd7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
