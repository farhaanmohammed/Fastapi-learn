"""making nullable fields

Revision ID: e452717422b1
Revises: a01815fcc1f0
Create Date: 2025-04-29 22:29:42.795812

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "e452717422b1"
down_revision: Union[str, None] = "a01815fcc1f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
