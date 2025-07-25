"""Add sentiment and embedding columns to articles

Revision ID: 54076d64706b
Revises: 122a0cf874ce
Create Date: 2025-07-19 17:50:27.029298

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '54076d64706b'
down_revision: Union[str, Sequence[str], None] = '122a0cf874ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('articles', sa.Column('sentiment', sa.String(), nullable=True))
    op.add_column('articles', sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=384), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('articles', 'embedding')
    op.drop_column('articles', 'sentiment')
    # ### end Alembic commands ###
