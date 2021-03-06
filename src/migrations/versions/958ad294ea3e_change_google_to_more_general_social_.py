"""Change 'google' to more general 'social' naming

Revision ID: 958ad294ea3e
Revises: d4e23d6e7ddb
Create Date: 2022-07-10 03:52:50.007547

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '958ad294ea3e'
down_revision = 'd4e23d6e7ddb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'social_users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('social_id', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
        sa.UniqueConstraint('social_id'),
    )
    op.drop_table('google_users')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'google_users',
        sa.Column('id', postgresql.UUID(), autoincrement=False, nullable=False),
        sa.Column('user_id', postgresql.UUID(), autoincrement=False, nullable=True),
        sa.Column('google_id', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='google_users_user_id_fkey'),
        sa.PrimaryKeyConstraint('id', name='google_users_pkey'),
        sa.UniqueConstraint('google_id', name='google_users_google_id_key'),
    )
    op.drop_table('social_users')
    # ### end Alembic commands ###
