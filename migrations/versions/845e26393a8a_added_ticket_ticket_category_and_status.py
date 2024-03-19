"""Added Ticket, Ticket Category and Status

Revision ID: 845e26393a8a
Revises: 27c70d44ff35
Create Date: 2024-03-18 23:25:09.211373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '845e26393a8a'
down_revision = '27c70d44ff35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket_status',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ticket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender', sa.Integer(), nullable=False),
    sa.Column('receiver', sa.Integer(), nullable=False),
    sa.Column('status_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('subject', sa.String(length=120), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('attachment', sa.String(length=512), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('previous_ticket', sa.Integer(), nullable=True),
    sa.Column('next_ticket', sa.Integer(), nullable=True),
    sa.Column('confirm_code', sa.Integer(), nullable=False),
    sa.Column('no_reply', sa.Boolean(), nullable=True),
    sa.Column('read_only', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['ticket_category.id'], ),
    sa.ForeignKeyConstraint(['next_ticket'], ['ticket.id'], ),
    sa.ForeignKeyConstraint(['previous_ticket'], ['ticket.id'], ),
    sa.ForeignKeyConstraint(['receiver'], ['user.id'], ),
    sa.ForeignKeyConstraint(['sender'], ['user.id'], ),
    sa.ForeignKeyConstraint(['status_id'], ['ticket_status.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('confirm_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ticket')
    op.drop_table('ticket_status')
    op.drop_table('ticket_category')
    # ### end Alembic commands ###
