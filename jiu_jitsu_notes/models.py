from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


class PositionGroup(Base):
    __tablename__ = "position_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]

    positions: Mapped[list["Position"]] = relationship(back_populates="group")


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]
    submission: Mapped[bool]

    group_id: Mapped[int] = mapped_column(ForeignKey("position_groups.id"))
    group: Mapped[PositionGroup] = relationship(back_populates="positions")

    techniques_from: Mapped[list["Technique"]] = relationship(
        back_populates="from_position"
    )

    techniques_to: Mapped[list["Technique"]] = relationship(
        back_populates="to_position"
    )


class Technique(Base):
    __tablename__ = "techniques"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    description: Mapped[str]

    from_position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    from_position: Mapped[Position] = relationship(back_populates="techniques_from")

    to_position_id: Mapped[int] = mapped_column(ForeignKey("positions.id"))
    to_position: Mapped[Position] = relationship(back_populates="techniques_to")
