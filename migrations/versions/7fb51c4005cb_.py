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
    op.drop_table('order_items')
    op.drop_table('todos')
    op.drop_table('order')
    op.drop_table('product')
    op.drop_table('todo_list')
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_constraint('category', 'questions', type_='foreignkey')
    op.create_foreign_key(None, 'questions', 'categories', ['category'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'questions', type_='foreignkey')
    op.create_foreign_key('category', 'questions', 'categories', ['category'], ['id'], onupdate='CASCADE', ondelete='SET NULL')
    op.alter_column('questions', 'category',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.create_table('todo_list',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('todo_list_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='todo_list_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('product',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('product_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='product_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('order',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('order_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='order_pkey'),
    postgresql_ignore_search_path=False
    )
    op.create_table('todos',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('completed', sa.BOOLEAN(), autoincrement=False, nullable=False),
    sa.Column('list_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['list_id'], ['todo_list.id'], name='todos_list_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='todos_pkey')
    )
    op.create_table('order_items',
    sa.Column('order_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], name='order_items_order_id_fkey'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], name='order_items_product_id_fkey'),
    sa.PrimaryKeyConstraint('order_id', 'product_id', name='order_items_pkey')
    )
    # ### end Alembic commands ###
