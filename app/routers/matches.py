from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app import crud
from schemas import MatchCreate, MatchRead

router = APIRouter(prefix="/matches", tags=["matches"])


@router.post("/", response_model=MatchRead, status_code=status.HTTP_201_CREATED)
def create_match(match: MatchCreate, db: Session = Depends(get_db)):
    if match.team1_id == match.team2_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="team1 and team2 must be different",
        )
    if crud.get_game(db, game_id=match.game_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game not found")
    if crud.get_team(db, team_id=match.team1_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team 1 not found")
    if crud.get_team(db, team_id=match.team2_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team 2 not found")
    return crud.create_match(db=db, match=match)


@router.get("/", response_model=List[MatchRead])
def list_matches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_matches(db, skip=skip, limit=limit)


@router.get("/{match_id}", response_model=MatchRead)
def get_match(match_id: int, db: Session = Depends(get_db)):
    db_match = crud.get_match(db, match_id=match_id)
    if db_match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Match not found")
    return db_match
