from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    teams_created = relationship("Team", back_populates="creator")
    memberships = relationship("TeamMembership", back_populates="user")


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    genre = Column(String(100), nullable=True)

    matches = relationship("Match", back_populates="game")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("User", back_populates="teams_created")
    memberships = relationship("TeamMembership", back_populates="team")
    matches_as_team1 = relationship(
        "Match", foreign_keys="Match.team1_id", back_populates="team1"
    )
    matches_as_team2 = relationship(
        "Match", foreign_keys="Match.team2_id", back_populates="team2"
    )

    @property
    def members(self):
        return [m.user for m in self.memberships if m.user is not None]


class TeamMembership(Base):
    __tablename__ = "team_memberships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    user = relationship("User", back_populates="memberships")
    team = relationship("Team", back_populates="memberships")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    scheduled_at = Column(DateTime, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    team1_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    team2_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    game = relationship("Game", back_populates="matches")
    team1 = relationship(
        "Team", foreign_keys=[team1_id], back_populates="matches_as_team1"
    )
    team2 = relationship(
        "Team", foreign_keys=[team2_id], back_populates="matches_as_team2"
    )
