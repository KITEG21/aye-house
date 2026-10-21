"""Add zones (provinces, municipalities, neighborhoods) and properties

Revision ID: add_zones_and_properties
Revises: initial_migration
Create Date: 2026-10-19 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'add_zones_and_properties'
down_revision: Union[str, None] = 'initial_migration'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        'provinces',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        *_timestamps(),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )

    op.create_table(
        'municipalities',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('province_id', sa.Uuid(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(['province_id'], ['provinces.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('province_id', 'name', name='uq_municipalities_province_id_name'),
    )
    op.create_index(op.f('ix_municipalities_province_id'), 'municipalities', ['province_id'])

    op.create_table(
        'neighborhoods',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('municipality_id', sa.Uuid(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(['municipality_id'], ['municipalities.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('municipality_id', 'name', name='uq_neighborhoods_municipality_id_name'),
    )
    op.create_index(op.f('ix_neighborhoods_municipality_id'), 'neighborhoods', ['municipality_id'])

    # Enum columns are stored as VARCHAR(20) (native_enum=False in the model)
    op.create_table(
        'properties',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('property_type', sa.String(length=20), nullable=False),
        sa.Column('listing_type', sa.String(length=20), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('price', sa.Numeric(precision=14, scale=2), nullable=False),
        sa.Column('currency', sa.String(length=20), nullable=False),
        sa.Column('area_m2', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('bedrooms', sa.Integer(), nullable=True),
        sa.Column('bathrooms', sa.Integer(), nullable=True),
        sa.Column('gas_type', sa.String(length=20), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('neighborhood_id', sa.Uuid(), nullable=False),
        *_timestamps(),
        sa.ForeignKeyConstraint(['neighborhood_id'], ['neighborhoods.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_properties_property_type'), 'properties', ['property_type'])
    op.create_index(op.f('ix_properties_listing_type'), 'properties', ['listing_type'])
    op.create_index(op.f('ix_properties_status'), 'properties', ['status'])
    op.create_index(op.f('ix_properties_neighborhood_id'), 'properties', ['neighborhood_id'])


def downgrade() -> None:
    op.drop_index(op.f('ix_properties_neighborhood_id'), table_name='properties')
    op.drop_index(op.f('ix_properties_status'), table_name='properties')
    op.drop_index(op.f('ix_properties_listing_type'), table_name='properties')
    op.drop_index(op.f('ix_properties_property_type'), table_name='properties')
    op.drop_table('properties')
    op.drop_index(op.f('ix_neighborhoods_municipality_id'), table_name='neighborhoods')
    op.drop_table('neighborhoods')
    op.drop_index(op.f('ix_municipalities_province_id'), table_name='municipalities')
    op.drop_table('municipalities')
    op.drop_table('provinces')
