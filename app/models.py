from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    UniqueConstraint,
)
from sqlalchemy.orm import backref, relationship
from app.database import Base, db_context

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


character_episode = Table(
    "character_episode",
    Base.metadata,
    Column("character_id", Integer, ForeignKey("character.id")),
    Column("episode_id", Integer, ForeignKey("episode.id")),
)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    password = Column(String(255))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    comments = relationship("Comment", backref="user", lazy="dynamic")
    role_id = Column(Integer, ForeignKey("role.id"), nullable=True)

    def __repr__(self):
        return "<User {}>".format(self.name)

    def set_password(self, password):
        self.password = pwd_context.hash(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)


class Character(Base):
    __tablename__ = "character"
    id = Column(Integer, primary_key=True)
    name = Column(
        String(255)
    )  # not possible to make it unique because characters can share the same name, example : Beth Smith
    status = Column(String(255))
    species = Column(String(255))
    type = Column(String(255))
    gender = Column(String(255))
    comments = relationship("Comment", backref="character", lazy="dynamic")

    def __repr__(self):
        return "<Character {} {}>".format(self.id, self.name)


class Episode(Base):
    __tablename__ = "episode"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    air_date = Column(DateTime)
    episode = Column(Integer)
    season = Column(Integer)
    __table_args__ = (
        UniqueConstraint("episode", "season", name="unique_episode_season"),
    )
    characters = relationship(
        "Character",
        secondary=character_episode,
        backref=backref("episodes", lazy="dynamic"),
        lazy="dynamic",
    )
    comments = relationship("Comment", backref="episode", lazy="dynamic")

    def __repr__(self):
        return "<Episode {} S{}E{}>".format(self.name, self.season, self.episode)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("character.id"), nullable=True)
    episode_id = Column(Integer, ForeignKey("episode.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    body = Column(String(255))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    updated_at = Column(DateTime, index=True, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("NOT(character_id IS NULL AND episode_id IS NULL)"),
    )

    def __repr__(self):
        return "<Comment {}>".format(self.id)


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    users = relationship("User", backref="role", lazy="dynamic")
