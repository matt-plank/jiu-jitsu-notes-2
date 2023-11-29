import os
import uuid
from datetime import datetime
from typing import Optional

from passlib import hash
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Position, PositionGroup, Technique, Token, User

DATABASE_URI: str = os.environ.get("DATABASE_URI", "sqlite:///jiu_jitsu_notes.db")

engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def group_by_id(session: Session, user: User, group_id: int) -> PositionGroup | None:
    return session.query(PositionGroup).filter_by(id=group_id, user=user).first()


def all_groups_for_user(session: Session, user: User) -> list[PositionGroup]:
    return session.query(PositionGroup).filter_by(user=user).all()


def create_group(session: Session, user: User, name: str, description: str) -> PositionGroup:
    group = PositionGroup(
        name=name,
        description=description,
        user=user,
    )

    session.add(group)
    session.commit()

    return group


def update_group(session: Session, group: PositionGroup, name: Optional[str], description: Optional[str]) -> PositionGroup:
    if name is not None:
        group.name = name

    if description is not None:
        group.description = description

    session.commit()

    return group


def position_by_id(session: Session, user: User, position_id: int) -> Position | None:
    return session.query(Position).filter_by(id=position_id, user=user).first()


def all_positions_for_user(session: Session, user: User) -> list[Position]:
    return session.query(Position).filter_by(user=user).all()


def create_position_in_group(session: Session, user: User, group: PositionGroup, **position_args) -> Position:
    position = Position(
        user=user,
        group=group,
        **position_args,
    )

    session.add(position)
    session.commit()

    return position


def technique_by_id(session: Session, user: User, technique_id: int) -> Technique | None:
    return session.query(Technique).filter_by(id=technique_id, user=user).first()


def create_technique(
    session: Session,
    user: User,
    name: str,
    description: str,
    from_position_id: int,
    to_position_id: Optional[int],
) -> Technique:
    technique = Technique(
        name=name,
        description=description,
        from_position_id=from_position_id,
        to_position_id=to_position_id,
        user=user,
    )

    session.add(technique)
    session.commit()

    return technique


def user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter_by(email=email).first()


def user_by_username(session: Session, username: str) -> User | None:
    return session.query(User).filter_by(username=username).first()


def create_user(session: Session, username: str, email: str, password: str) -> User | None:
    user = User(
        username=username,
        email=email,
        password_hash=hash.bcrypt.hash(password),
    )

    session.add(user)
    session.commit()

    return user


def token_from_string(session: Session, token: str) -> Token | None:
    return session.query(Token).filter_by(token=token).first()


def create_token_for_user(session: Session, user: User) -> Token:
    token = Token(
        token=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
    )

    session.add(token)

    user.token = token

    session.commit()

    return token


def delete_token_for_user(session: Session, user: User) -> None:
    session.delete(user.token)
    session.commit()
