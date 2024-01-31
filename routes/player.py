from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, create_engine

from models.player import Player, engine

router = APIRouter()

@router.get("/")
def default():
    return {'name': 'rva', 'version': '1.0.0', 'environment': 'production'}

@router.get("/players/")
def read_players():
    with Session(engine) as session:
        players = session.query(Player).all()
        return players

@router.post("/players/")
def create_player(player: Player):
    with Session(engine) as session:
        session.add(player)
        session.commit()
        session.refresh(player)
        return player

@router.patch("/players/{player_id}")
def update_player(player_id: int, player: Player):
    with Session(engine) as session:
        player_db = session.get(Player, player_id)
        if player_db is None:
            return None
        player_db.name = player.name
        player_db.score = player.score
        player_db.level = player.level
        player_db.ressources = player.ressources
        session.add(player_db)
        session.commit()
        session.refresh(player_db)
        return player_db

@router.put("/players/{player_id}")
def update_player(player_id: int, player: Player):
    with Session(engine) as session:
        player_db = session.get(Player, player_id)
        if player_db is None:
            return None
        player_db.name = player.name
        player_db.score = player.score
        player_db.level = player.level
        player_db.ressources = player.ressources
        session.add(player_db)
        session.commit()
        session.refresh(player_db)
        return player_db

@router.delete("/players/{player_id}")
def delete_player(player_id: int):
    with Session(engine) as session:
        player = session.get(Player, player_id)
        if player is None:
            return None
        session.delete(player)
        session.commit()
        return player
