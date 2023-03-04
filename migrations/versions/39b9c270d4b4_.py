"""empty message

Revision ID: 39b9c270d4b4
Revises: 
Create Date: 2023-03-04 20:48:43.607470

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "39b9c270d4b4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "User",
        sa.Column("email", sa.String(length=80), nullable=True),
        sa.Column("username", sa.String(length=10), nullable=True),
        sa.Column("first_name", sa.String(length=4), nullable=True),
        sa.Column("last_name", sa.String(length=4), nullable=True),
        sa.Column("gender", sa.Enum("남자", "여자"), nullable=True),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("password", sa.String(length=120), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=True),
        sa.Column("updated_on", sa.DateTime(), nullable=True),
        sa.Column("uuid", sa.String(length=36), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("User")
    # ### end Alembic commands ###
