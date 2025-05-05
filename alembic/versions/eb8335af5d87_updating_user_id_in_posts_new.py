"""updating user_id in posts new

Revision ID: eb8335af5d87
Revises: ecaad879b48b
Create Date: 2025-05-02 15:20:45.953588

"""
from typing import Sequence, Union
from loguru import logger
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb8335af5d87'
down_revision: Union[str, None] = 'ecaad879b48b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    try:
        op.alter_column('posts', 'user_id',
                        existing_type=sa.INTEGER(),
                        nullable=False
                        )
    except Exception as e:
        logger.info(f"error:{e}")


def downgrade() -> None:
    """Downgrade schema."""
    pass
