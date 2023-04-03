"""empty message

Revision ID: ab8f093a0880
Revises: 09f4861cbacf
Create Date: 2023-04-02 17:42:54.082094

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ab8f093a0880"
down_revision = "09f4861cbacf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("User", schema=None) as batch_op:
        batch_op.drop_column("gender")
        batch_op.drop_column("name")

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("User", schema=None) as batch_op:
        batch_op.add_column(sa.Column("name", sa.VARCHAR(length=10), nullable=False))
        batch_op.add_column(sa.Column("gender", sa.VARCHAR(length=2), nullable=False))

    # ### end Alembic commands ###
