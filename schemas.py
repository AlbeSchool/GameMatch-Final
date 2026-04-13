from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ─── User ────────────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: int

    model_config = {"from_attributes": True}


# ─── Game ────────────────────────────────────────────────────────────────────

class GameBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    genre: Optional[str] = None


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: int

    model_config = {"from_attributes": True}


# ─── Team ────────────────────────────────────────────────────────────────────

class TeamBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)


class TeamCreate(TeamBase):
    creator_id: int


class TeamRead(TeamBase):
    id: int
    creator_id: int
    members: List[UserRead] = []

    model_config = {"from_attributes": True}


# ─── TeamMembership (bridge table N:M User ↔ Team) ───────────────────────────

class TeamMembershipBase(BaseModel):
    user_id: int
    team_id: int


class TeamMembershipCreate(TeamMembershipBase):
    pass


class TeamMembershipRead(TeamMembershipBase):
    id: int
    user: Optional[UserRead] = None

    model_config = {"from_attributes": True}


# ─── Match ───────────────────────────────────────────────────────────────────

class MatchBase(BaseModel):
    scheduled_at: datetime


class MatchCreate(MatchBase):
    game_id: int
    team1_id: int
    team2_id: int


class MatchRead(MatchBase):
    id: int
    game_id: int
    team1_id: int
    team2_id: int
    game: Optional[GameRead] = None
    team1: Optional[TeamRead] = None
    team2: Optional[TeamRead] = None

    model_config = {"from_attributes": True}
