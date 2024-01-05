"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    # Create a temporary column with a default value
    op.add_column('classes', sa.Column('temp_image_filename', sa.String(length=255), nullable=True))
    op.execute('UPDATE classes SET temp_image_filename = "default_value"')
    op.alter_column('classes', 'temp_image_filename', nullable=False, new_column_name='image_filename')

def downgrade():
    op.drop_column('classes', 'image_filename')
