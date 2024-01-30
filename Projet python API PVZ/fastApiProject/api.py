from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


class Player(SQLModel, table=True):
    id_player: int = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    score: int
    level: int
    ressources: int
    
SQLModel.metadata.create_all(engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/players/")
def create_player(player: Player):
    with Session(engine) as session:
        session.add(player)
        session.commit()
        session.refresh(player)
        return player

@app.get("/players/")
def read_players():
    with Session(engine) as session:
        players = session.query(Player).all()
        return players