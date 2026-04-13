from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    id: int


class GameBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    genre: Optional[str] = Field(default=None, max_length=30)


class GameCreate(GameBase):
    pass


class GameRead(GameBase):
    id: int


class TeamBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=40)


class TeamCreate(TeamBase):
    creator_id: int
    member_ids: List[int] = Field(default_factory=list)


class TeamRead(TeamBase):
    id: int
    creator_id: int
    members: List[UserRead] = Field(default_factory=list)


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


class TeamMembershipBase(BaseModel):
    user_id: int
    team_id: int


class TeamMembershipCreate(TeamMembershipBase):
    pass


class TeamMembershipRead(TeamMembershipBase):
    id: int
