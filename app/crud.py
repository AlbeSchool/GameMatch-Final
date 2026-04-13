from sqlalchemy.orm import Session
from app import models
from schemas import UserCreate, GameCreate, TeamCreate, MatchCreate, TeamMembershipCreate
from app.utils.security import hash_password


# ─── User ────────────────────────────────────────────────────────────────────

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ─── Game ────────────────────────────────────────────────────────────────────

def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_games(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Game).offset(skip).limit(limit).all()


def create_game(db: Session, game: GameCreate):
    db_game = models.Game(name=game.name, genre=game.genre)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


# ─── Team ────────────────────────────────────────────────────────────────────

def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: TeamCreate):
    db_team = models.Team(name=team.name, creator_id=team.creator_id)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


# ─── TeamMembership ──────────────────────────────────────────────────────────

def create_team_membership(db: Session, membership: TeamMembershipCreate):
    db_membership = models.TeamMembership(
        user_id=membership.user_id, team_id=membership.team_id
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership


def get_team_memberships(db: Session, team_id: int):
    return (
        db.query(models.TeamMembership)
        .filter(models.TeamMembership.team_id == team_id)
        .all()
    )


# ─── Match ───────────────────────────────────────────────────────────────────

def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()


def create_match(db: Session, match: MatchCreate):
    db_match = models.Match(
        scheduled_at=match.scheduled_at,
        game_id=match.game_id,
        team1_id=match.team1_id,
        team2_id=match.team2_id,
    )
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match
