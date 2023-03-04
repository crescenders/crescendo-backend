"""empty message

Revision ID: 6efcf0e1f84a
Revises: 
Create Date: 2023-03-04 18:46:28.504261

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "6efcf0e1f84a"
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
        sa.Column("uuid", sa.String(length=36), nullable=False),
        sa.PrimaryKeyConstraint("id", "uuid"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("User")
    # ### end Alembic commands ###
