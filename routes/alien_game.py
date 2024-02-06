from fastapi import APIRouter
from sqlmodel import Session, create_engine

from models.alien_game import AlienGame, engine

router = APIRouter()

@router.get("/alien_games/")
def read_alien_games():
    with Session(engine) as session:
        alien_games = session.query(AlienGame).all()
        return alien_games
    
@router.get("/alien_games/{game_id}/{alien_id}")
def read_alien_game(game_id: int, alien_id: int):
    with Session(engine) as session:
        alien_game = session.get(AlienGame, (game_id, alien_id))
        if alien_game is None:
            return None
        return alien_game

@router.post("/alien_games/")
def create_alien_game(alien_game: AlienGame):
    with Session(engine) as session:
        session.add(alien_game)
        session.commit()
        session.refresh(alien_game)
        return alien_game

@router.patch("/alien_games/{game_id}/{alien_id}")
def update_alien_game(game_id: int, alien_id: int, alien_game: AlienGame):
    with Session(engine) as session:
        alien_game_db = session.get(AlienGame, (game_id, alien_id))
        if alien_game_db is None:
            return None
        if alien_game.pos_x is not None:
            alien_game_db.pos_x = alien_game.pos_x
        if alien_game.pos_y is not None:
            alien_game_db.pos_y = alien_game.pos_y
        session.add(alien_game_db)
        session.commit()
        session.refresh(alien_game_db)
        return alien_game_db

@router.put("/alien_games/{game_id}/{alien_id}")
def update_alien_game(game_id: int, alien_id: int, alien_game: AlienGame):
    with Session(engine) as session:
        alien_game_db = session.get(AlienGame, (game_id, alien_id))
        if alien_game_db is None:
            return None
        alien_game_db.pos_x = alien_game.pos_x
        alien_game_db.pos_y = alien_game.pos_y
        session.add(alien_game_db)
        session.commit()
        session.refresh(alien_game_db)
        return alien_game_db

@router.delete("/alien_games/{game_id}/{alien_id}")
def delete_alien_game(game_id: int, alien_id: int):
    with Session(engine) as session:
        alien_game = session.get(AlienGame, (game_id, alien_id))
        if alien_game is None:
            return None
        session.delete(alien_game)
        session.commit()
        return alien_game
