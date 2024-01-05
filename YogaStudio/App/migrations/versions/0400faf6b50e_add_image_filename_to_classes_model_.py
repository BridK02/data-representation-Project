"""Add image_filename to Classes model (second attempt)

Revision ID: 0400faf6b50e
Revises: revision_id001
Create Date: 2024-01-04 21:56:19.233624

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '0400faf6b50e'
down_revision = 'revision_id001'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_filename', sa.String(length=255), nullable=True))
        batch_op.alter_column('title',
               existing_type=mysql.VARCHAR(length=250),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('classes', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=mysql.VARCHAR(length=250),
               nullable=True)
        batch_op.drop_column('image_filename')

    # ### end Alembic commands ###