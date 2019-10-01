"""add state in slaves

Revision ID: 368ccee1c117
Revises: 4dbea9effcd1
Create Date: 2019-10-01 16:53:48.820911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '368ccee1c117'
down_revision = '4dbea9effcd1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('slaves', sa.Column('state', sa.Boolean))


def downgrade():
    op.drop_column('slaves', 'state')
