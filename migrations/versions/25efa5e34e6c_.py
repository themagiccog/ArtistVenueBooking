"""empty message

Revision ID: 25efa5e34e6c
Revises: 
Create Date: 2020-10-19 17:17:30.999864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25efa5e34e6c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('artist',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('seeking', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venue',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('address', sa.String(length=120), nullable=True),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.Column('phone', sa.String(length=120), nullable=True),
    sa.Column('seeking', sa.Boolean(), nullable=True),
    sa.Column('seeking_description', sa.String(length=500), nullable=True),
    sa.Column('image_link', sa.String(length=500), nullable=True),
    sa.Column('facebook_link', sa.String(length=120), nullable=True),
    sa.Column('website', sa.String(length=500), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aristgenre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.Enum('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental', 'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae', 'Rock n Roll', 'Soul', 'Other', name='genre'), nullable=True),
    sa.Column('artist_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('show',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['artist.id'], ),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('venuegenre',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genre', sa.Enum('Alternative', 'Blues', 'Classical', 'Country', 'Electronic', 'Folk', 'Funk', 'Hip-Hop', 'Heavy Metal', 'Instrumental', 'Jazz', 'Musical Theatre', 'Pop', 'Punk', 'R&B', 'Reggae', 'Rock n Roll', 'Soul', 'Other', name='genre'), nullable=True),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['venue_id'], ['venue.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venuegenre')
    op.drop_table('show')
    op.drop_table('aristgenre')
    op.drop_table('venue')
    op.drop_table('artist')
    # ### end Alembic commands ###
