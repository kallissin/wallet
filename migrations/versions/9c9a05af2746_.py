"""empty message

Revision ID: 9c9a05af2746
Revises: 
Create Date: 2022-06-23 17:51:53.298302

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c9a05af2746'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=150), nullable=False),
    sa.Column('discount', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('category_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('customers',
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('cpf', sa.Unicode(length=11), nullable=False),
    sa.Column('name', sa.Unicode(length=150), nullable=False),
    sa.PrimaryKeyConstraint('customer_id'),
    sa.UniqueConstraint('cpf')
    )
    op.create_table('users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=150), nullable=False),
    sa.Column('email', sa.Unicode(length=255), nullable=False),
    sa.Column('username', sa.Unicode(length=100), nullable=False),
    sa.Column('password_hash', sa.Unicode(length=255), nullable=False),
    sa.Column('role', sa.Unicode(length=100), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('sold_at', sa.DateTime(), nullable=False),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('cashback_id', sa.Integer(), nullable=True),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=150), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
    sa.PrimaryKeyConstraint('product_id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('orders_products',
    sa.Column('register_id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=True),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('qty', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['orders.order_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.product_id'], ),
    sa.PrimaryKeyConstraint('register_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('orders_products')
    op.drop_table('products')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('customers')
    op.drop_table('categories')
    # ### end Alembic commands ###
