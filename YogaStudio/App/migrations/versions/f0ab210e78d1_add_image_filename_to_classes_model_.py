"""Add image_filename to Classes model (third attempt)

Revision ID: f0ab210e78d1
Revises: 0400faf6b50e
Create Date: 2024-01-04 22:19:14.512034

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f0ab210e78d1'
down_revision = '0400faf6b50e'
branch_labels = None
depends_on = None

def upgrade():
    # Set a default value for existing rows
    op.execute("UPDATE classes SET image_filename = 'default_value' WHERE image_filename IS NULL")

    # Modify the column to be NOT NULL
    op.alter_column('classes', 'image_filename', existing_type=sa.String(length=255), nullable=False)

def downgrade():
    # Revert the NOT NULL constraint
    op.alter_column('classes', 'image_filename', existing_type=sa.String(length=255), nullable=True)


    # ### end Alembic commands ###
