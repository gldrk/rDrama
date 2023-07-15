"""remove holes

Revision ID: 6b6c1b21a487
Revises: 8b97d5de5050
Create Date: 2023-03-30 05:36:17.697225+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b6c1b21a487'
down_revision = '8b97d5de5050'
branch_labels = None
depends_on = None


def upgrade():
	# ### commands auto generated by Alembic - please adjust! (adjusted -@TLSM) ###

	op.drop_index('fki_exile_exiler_fkey', table_name='exiles')
	op.drop_index('fki_exile_sub_fkey', table_name='exiles')
	op.drop_table('exiles')

	op.drop_index('fki_mod_sub_fkey', table_name='mods')
	op.drop_table('mods')

	op.drop_index('fki_sub_blocks_sub_fkey', table_name='sub_blocks')
	op.drop_table('sub_blocks')

	op.drop_constraint('sub_fkey', 'submissions', type_='foreignkey')
	op.drop_column('submissions', 'sub')
	op.drop_column('users', 'subs_created')

	op.drop_index('subs_idx', table_name='subs')
	op.drop_table('subs')

	op.execute("DELETE FROM modactions WHERE kind = 'move_hole'")


def downgrade():
	# ### commands auto generated by Alembic - please adjust! (adjusted -@TLSM) ###
	op.create_table('subs',
	sa.Column('name', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
	sa.Column('sidebar', sa.VARCHAR(length=500), autoincrement=False, nullable=True),
	sa.Column('sidebar_html', sa.VARCHAR(length=1000), autoincrement=False, nullable=True),
	sa.Column('sidebarurl', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
	sa.Column('bannerurl', sa.VARCHAR(length=60), autoincrement=False, nullable=True),
	sa.Column('css', sa.VARCHAR(length=4000), autoincrement=False, nullable=True),
	sa.PrimaryKeyConstraint('name', name='subs_pkey'),
	postgresql_ignore_search_path=False
	)
	op.create_index('subs_idx', 'subs', ['name'], unique=False)

	op.add_column('users', sa.Column('subs_created', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=False))
	op.add_column('submissions', sa.Column('sub', sa.VARCHAR(length=20), autoincrement=False, nullable=True))
	op.create_foreign_key('sub_fkey', 'submissions', 'subs', ['sub'], ['name'])

	op.create_table('sub_blocks',
	sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
	sa.Column('sub', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
	sa.ForeignKeyConstraint(['sub'], ['subs.name'], name='sub_blocks_sub_fkey'),
	sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='sub_blocks_user_fkey'),
	sa.PrimaryKeyConstraint('user_id', 'sub', name='sub_blocks_pkey')
	)
	op.create_index('fki_sub_blocks_sub_fkey', 'sub_blocks', ['sub'], unique=False)

	op.create_table('mods',
	sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
	sa.Column('sub', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
	sa.Column('created_utc', sa.INTEGER(), autoincrement=False, nullable=False),
	sa.ForeignKeyConstraint(['sub'], ['subs.name'], name='mod_sub_fkey'),
	sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='user_mod_fkey'),
	sa.PrimaryKeyConstraint('user_id', 'sub', name='mods_pkey')
	)
	op.create_index('fki_mod_sub_fkey', 'mods', ['sub'], unique=False)

	op.create_table('exiles',
	sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
	sa.Column('sub', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
	sa.Column('exiler_id', sa.INTEGER(), autoincrement=False, nullable=False),
	sa.ForeignKeyConstraint(['exiler_id'], ['users.id'], name='exile_exiler_fkey'),
	sa.ForeignKeyConstraint(['sub'], ['subs.name'], name='exile_sub_fkey'),
	sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='exile_user_fkey'),
	sa.PrimaryKeyConstraint('user_id', 'sub', name='exiles_pkey')
	)
	op.create_index('fki_exile_sub_fkey', 'exiles', ['sub'], unique=False)
	op.create_index('fki_exile_exiler_fkey', 'exiles', ['exiler_id'], unique=False)
