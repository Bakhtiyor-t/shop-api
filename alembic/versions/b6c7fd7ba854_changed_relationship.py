"""changed relationship

Revision ID: b6c7fd7ba854
Revises: 4e7b7f8ba1c6
Create Date: 2021-11-29 04:29:58.971911

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6c7fd7ba854'
down_revision = '4e7b7f8ba1c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('debtors_user_id_fkey', 'debtors', type_='foreignkey')
    op.create_foreign_key(None, 'debtors', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('firms_user_id_fkey', 'firms', type_='foreignkey')
    op.create_foreign_key(None, 'firms', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('invoices_firm_id_fkey', 'invoices', type_='foreignkey')
    op.drop_constraint('invoices_user_id_fkey', 'invoices', type_='foreignkey')
    op.create_foreign_key(None, 'invoices', 'firms', ['firm_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'invoices', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'invoices', type_='foreignkey')
    op.drop_constraint(None, 'invoices', type_='foreignkey')
    op.create_foreign_key('invoices_user_id_fkey', 'invoices', 'users', ['user_id'], ['id'])
    op.create_foreign_key('invoices_firm_id_fkey', 'invoices', 'firms', ['firm_id'], ['id'])
    op.drop_constraint(None, 'firms', type_='foreignkey')
    op.create_foreign_key('firms_user_id_fkey', 'firms', 'users', ['user_id'], ['id'])
    op.drop_constraint(None, 'debtors', type_='foreignkey')
    op.create_foreign_key('debtors_user_id_fkey', 'debtors', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###
