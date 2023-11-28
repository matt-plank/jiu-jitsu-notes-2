from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]

    groups: Mapped[list["PositionGroup"]] = relationship(back_populates="user")
    positions: Mapped[list["Position"]] = relationship(back_populates="user")
    techniques: Mapped[list["Technique"]] = relationship(back_populates="user")


class PositionGroup(Base):
    __tablename__ = "position_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="groups")

    name: Mapped[str]
    description: Mapped[str]

    positions: Mapped[list["Position"]] = relationship(back_populates="group")


class Position(Base):
    __tablename__ = "positions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="positions")

    name: Mapped[str]
    description: Mapped[str]
    submission: Mapped[bool] = mapped_column(default=False)

    group_id: Mapped[int | None] = mapped_column(ForeignKey("position_groups.id"))
    group: Mapped[PositionGroup | None] = relationship(back_populates="positions")

    techniques_from: Mapped[list["Technique"]] = relationship(
        back_populates="from_position",
        foreign_keys="Technique.from_position_id",
    )

    techniques_to: Mapped[list["Technique"]] = relationship(
        back_populates="to_position",
        foreign_keys="Technique.to_position_id",
    )


class Technique(Base):
    __tablename__ = "techniques"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="techniques")

    name: Mapped[str]
    description: Mapped[str]

    from_position_id: Mapped[int | None] = mapped_column(ForeignKey("positions.id"))
    from_position: Mapped[Position | None] = relationship(
        back_populates="techniques_from",
        foreign_keys=[from_position_id],
    )

    to_position_id: Mapped[int | None] = mapped_column(ForeignKey("positions.id"))
    to_position: Mapped[Position | None] = relationship(
        back_populates="techniques_to",
        foreign_keys=[to_position_id],
    )
