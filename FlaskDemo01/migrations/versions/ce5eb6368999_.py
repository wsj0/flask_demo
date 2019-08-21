"""empty message

Revision ID: ce5eb6368999
Revises: 2afe8a03814d
Create Date: 2019-08-07 19:23:52.228318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce5eb6368999'
down_revision = '2afe8a03814d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teacher', sa.Column('course_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'teacher', 'course', ['course_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teacher', type_='foreignkey')
    op.drop_column('teacher', 'course_id')
    # ### end Alembic commands ###
