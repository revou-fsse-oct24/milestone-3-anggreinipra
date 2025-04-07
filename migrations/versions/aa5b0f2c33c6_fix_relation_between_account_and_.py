"""fix relation between account and transaction

Revision ID: aa5b0f2c33c6
Revises: 5f15ddaf3a0f
Create Date: 2025-04-07 09:59:32.204214

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa5b0f2c33c6'
down_revision: Union[str, None] = '5f15ddaf3a0f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'accounts', ['account_number'])
    op.create_unique_constraint(None, 'users', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'accounts', type_='unique')
    # ### end Alembic commands ###
