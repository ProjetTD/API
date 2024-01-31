from fastapi import APIRouter
from sqlmodel import Session, create_engine

from models.game import Game, engine

router = APIRouter()

@router.get("/games/")
def read_games():
    with Session(engine) as session:
        games = session.query(Game).all()
        return games

@router.post("/games/")
def create_game(game: Game):
    with Session(engine) as session:
        session.add(game)
        session.commit()
        session.refresh(game)
        return game

@router.patch("/games/{game_id}")
def update_game(game_id: int, game: Game):
    with Session(engine) as session:
        game_db = session.get(Game, game_id)
        if game_db is None:
            return None
        game_db.id_player = game.id_player
        game_db.id_level = game.id_level
        game_db.score = game.score
        game_db.status = game.status
        session.add(game_db)
        session.commit()
        session.refresh(game_db)
        return game_db

@router.put("/games/{game_id}")
def update_game(game_id: int, game: Game):
    with Session(engine) as session:
        game_db = session.get(Game, game_id)
        if game_db is None:
            return None
        game_db.id_player = game.id_player
        game_db.id_level = game.id_level
        game_db.score = game.score
        game_db.status = game.status
        session.add(game_db)
        session.commit()
        session.refresh(game_db)
        return game_db

@router.delete("/games/{game_id}")
def delete_game(game_id: int):
    with Session(engine) as session:
        game = session.get(Game, game_id)
        if game is None:
            return None
        session.delete(game)
        session.commit()
        return game
