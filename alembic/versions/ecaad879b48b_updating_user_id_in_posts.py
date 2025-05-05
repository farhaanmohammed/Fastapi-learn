"""updating user_id in posts

Revision ID: ecaad879b48b
Revises: ee12e2b9d49c
Create Date: 2025-05-02 15:08:23.269921

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecaad879b48b'
down_revision: Union[str, None] = 'ee12e2b9d49c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('post', 'user_id',
                    existing_type=sa.INTEGER(),
                    nullable=True
                    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
