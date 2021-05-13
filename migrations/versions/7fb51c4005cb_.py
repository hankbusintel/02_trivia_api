"""empty message

Revision ID: 7fb51c4005cb
Revises: 
Create Date: 2021-05-09 16:01:22.797900

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fb51c4005cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('category', 'questions', type_='foreignkey')
    #op.create_foreign_key(None, 'questions', 'categories', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass




    # ### end Alembic commands ###
