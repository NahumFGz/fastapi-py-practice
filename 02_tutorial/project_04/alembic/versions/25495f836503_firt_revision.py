"""firt revision

Revision ID: 25495f836503
Revises:
Create Date: 2025-04-21 01:36:38.605983

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "25495f836503"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # La primera vez a mano
    op.add_column("users", sa.Column("new_column_one", sa.String(), nullable=True))

    # pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
