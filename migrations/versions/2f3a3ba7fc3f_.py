"""empty message

Revision ID: 2f3a3ba7fc3f
Revises: 
Create Date: 2023-03-05 10:24:17.014571

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2f3a3ba7fc3f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "User",
        sa.Column("email", sa.String(length=80), nullable=False),
        sa.Column("username", sa.String(length=10), nullable=False),
        sa.Column("first_name", sa.String(length=4), nullable=False),
        sa.Column("last_name", sa.String(length=4), nullable=False),
        sa.Column("gender", sa.Enum("남자", "여자"), nullable=False),
        sa.Column("phone_number", sa.String(length=20), nullable=False),
        sa.Column("password", sa.String(length=120), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created_on", sa.DateTime(), nullable=False),
        sa.Column("updated_on", sa.DateTime(), nullable=False),
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("phone_number"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("User")
    # ### end Alembic commands ###
