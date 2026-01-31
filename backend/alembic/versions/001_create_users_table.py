"""Create users table

Revision ID: 001
Revises:
Create Date: 2026-01-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
  """마이그레이션 업그레이드"""
  op.create_table(
    'users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
  )
  op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)


def downgrade() -> None:
  """마이그레이션 다운그레이드"""
  op.drop_index(op.f('ix_users_email'), table_name='users')
  op.drop_table('users')
