"""Zone feature models.

Zones are hierarchical: Province (Provincia/Ciudad) > Municipality (Municipio)
> Neighborhood (Reparto). Properties reference a neighborhood, so statistics can
be aggregated at any of the three levels.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Province(Base):
    """Province (Provincia/Ciudad)."""

    __tablename__ = "provinces"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
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

    municipalities: Mapped[list["Municipality"]] = relationship(back_populates="province")

    def __repr__(self) -> str:
        return f"<Province(id={self.id}, name='{self.name}')>"


class Municipality(Base):
    """Municipality (Municipio)."""

    __tablename__ = "municipalities"
    __table_args__ = (
        UniqueConstraint("province_id", "name", name="uq_municipalities_province_id_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    province_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("provinces.id", ondelete="RESTRICT"),
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

    province: Mapped[Province] = relationship(back_populates="municipalities")
    neighborhoods: Mapped[list["Neighborhood"]] = relationship(back_populates="municipality")

    def __repr__(self) -> str:
        return f"<Municipality(id={self.id}, name='{self.name}')>"


class Neighborhood(Base):
    """Neighborhood (Reparto)."""

    __tablename__ = "neighborhoods"
    __table_args__ = (
        UniqueConstraint("municipality_id", "name", name="uq_neighborhoods_municipality_id_name"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    municipality_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("municipalities.id", ondelete="RESTRICT"),
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

    municipality: Mapped[Municipality] = relationship(back_populates="neighborhoods")

    def __repr__(self) -> str:
        return f"<Neighborhood(id={self.id}, name='{self.name}')>"
