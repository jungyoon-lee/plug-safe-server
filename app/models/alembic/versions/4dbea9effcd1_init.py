"""init

Revision ID: 4dbea9effcd1
Revises: 
Create Date: 2019-10-01 16:46:51.402238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4dbea9effcd1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('masters', sa.Column('state', sa.Boolean))


def downgrade():
    op.drop_column('masters', 'state')
