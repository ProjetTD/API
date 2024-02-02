from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
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

@router.get("/players/{uid}")
def read_player(uid: str):
    with Session(engine) as session:
        player = session.query(Player).filter(Player.uid == uid).first()
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return player
    
@router.get("/players/name/{name}")
def read_player_by_name(name: str):
    with Session(engine) as session:
        player = session.query(Player).filter(Player.name == name).first()
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return player

@router.post("/players/")
def create_player(player: Player):
    with Session(engine) as session:
        existing_player = session.query(Player).filter(Player.name == player.name).first()
        if existing_player:
            raise HTTPException(status_code=400, detail={"detail": "Player with this name already exists", "code": "PLAYER_ALREADY_EXISTS" })
        player_uid = str(uuid4())
        new_player = Player(**player.dict(), uid=player_uid)
        session.add(new_player)
        session.commit()
        session.refresh(new_player)

        return new_player

@router.patch("/players/{player_id}")
def update_player(player_id: int, player: Player):
    with Session(engine) as session:
        player_db = session.get(Player, player_id)
        if player_db is None:
            return None
        if player.name is not None:
            player_db.name = player.name
        if player.score is not None:
            player_db.score = player.score
        if player.level is not None:
            player_db.level = player.level
        if player.ressources is not None:
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
