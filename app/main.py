from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, teams, matches

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="GameMatch API",
    description="Backend per la gestione di team e partite multiplayer",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(teams.router)
app.include_router(matches.router)


@app.get("/")
def root():
    return {"message": "Benvenuto in GameMatch API 🎮"}
