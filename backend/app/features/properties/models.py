"""Property feature models."""

import uuid
from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Numeric, String, Text, Uuid, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.features.zones.models import Neighborhood


class PropertyType(StrEnum):
    """Property type."""

    HOUSE = "house"  # Casa
    APARTMENT = "apartment"  # Apartamento
    ROOM = "room"  # Habitación
    LAND = "land"  # Terreno
    COMMERCIAL = "commercial"  # Local comercial
    OTHER = "other"  # Otro


class ListingType(StrEnum):
    """Whether the property is offered for sale or for rent."""

    SALE = "sale"  # Venta
    RENTAL = "rental"  # Alquiler


class PropertyStatus(StrEnum):
    """Listing status."""

    AVAILABLE = "available"  # Disponible
    RESERVED = "reserved"  # Reservado
    SOLD = "sold"  # Vendido (sale only)
    RENTED = "rented"  # Alquilado (rental only)
    INACTIVE = "inactive"  # Inactivo


class GasType(StrEnum):
    """Gas supply system."""

    PIPED = "piped"  # Gas de la calle (por tubería)
    CYLINDER = "cylinder"  # Gas por balita
    NONE = "none"  # Sin gas


class Currency(StrEnum):
    """Price currency. Averages must be computed per currency."""

    USD = "USD"
    CUP = "CUP"
    EUR = "EUR"


def _enum_column(enum_cls: type[StrEnum]) -> SAEnum:
    # Stored as VARCHAR with the enum *values* so new members don't need a DB migration
    return SAEnum(
        enum_cls,
        native_enum=False,
        length=20,
        values_callable=lambda e: [member.value for member in e],
        validate_strings=True,
    )


class Property(Base):
    """Property (Inmueble) listed for sale or rent."""

    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    property_type: Mapped[PropertyType] = mapped_column(
        _enum_column(PropertyType), index=True, nullable=False
    )
    listing_type: Mapped[ListingType] = mapped_column(
        _enum_column(ListingType), index=True, nullable=False
    )
    status: Mapped[PropertyStatus] = mapped_column(
        _enum_column(PropertyStatus),
        index=True,
        default=PropertyStatus.AVAILABLE,
        nullable=False,
    )
    price: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[Currency] = mapped_column(
        _enum_column(Currency), default=Currency.USD, nullable=False
    )
    area_m2: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    bedrooms: Mapped[int | None] = mapped_column(nullable=True)
    bathrooms: Mapped[int | None] = mapped_column(nullable=True)
    gas_type: Mapped[GasType] = mapped_column(_enum_column(GasType), nullable=False)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    neighborhood_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("neighborhoods.id", ondelete="RESTRICT"),
        index=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    neighborhood: Mapped[Neighborhood] = relationship()

    def __repr__(self) -> str:
        return f"<Property(id={self.id}, title='{self.title}')>"
