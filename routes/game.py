from uuid import uuid4
from fastapi import APIRouter
from sqlmodel import Session, create_engine

from models.game import Game, engine

router = APIRouter()

@router.get("/games/")
def read_games():
    with Session(engine) as session:
        games = session.query(Game).all()
        return games
    
@router.get("/games/{game_id}")
def read_game(game_id: str):
    with Session(engine) as session:
        game = session.query(Game).filter(Game.id_game == game_id).first()
        return game

@router.get("/games/player/{player_id}")
def read_game_by_player(player_id: str):
    with Session(engine) as session:
        game = session.query(Game).filter(Game.id_player == player_id).first()
        return game

@router.post("/games/")
def create_game(game: Game):
    with Session(engine) as session:
        game_uid = str(uuid4())
        new_game = Game(**game.dict(), id_game=game_uid)
        print(new_game)
        session.add(new_game)
        session.commit()
        session.refresh(new_game)
        return new_game

@router.patch("/games/{game_id}")
def update_game(game_id: int, game: Game):
    with Session(engine) as session:
        game_db = session.get(Game, game_id)
        if game_db is None:
            return None
        if game.id_player is not None:
            game_db.id_player = game.id_player
        if game.id_level is not None:
            game_db.id_level = game.id_level
        if game.score is not None:
            game_db.score = game.score
        if game.status is not None:
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
