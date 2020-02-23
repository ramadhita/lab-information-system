"""notelp

Revision ID: 14ec12f1e1c8
Revises: c42d72b6832a
Create Date: 2020-01-13 17:25:27.267374

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '14ec12f1e1c8'
down_revision = 'c42d72b6832a'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pasien',sa.Column('notelp',sa.String,index=True))

def downgrade():
    op.drop_column('pasien','notelp')
