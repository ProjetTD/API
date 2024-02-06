from fastapi import APIRouter
from sqlmodel import Session, create_engine

from models.robot_game import RobotGame, engine

router = APIRouter()

@router.get("/robot_games/")
def read_robot_games():
    with Session(engine) as session:
        robot_games = session.query(RobotGame).all()
        return robot_games
    
@router.get("/robot_games/{game_id}/{robot_id}")
def read_robot_game(game_id: int, robot_id: int):
    with Session(engine) as session:
        robot_game = session.get(RobotGame, (game_id, robot_id))
        if robot_game is None:
            return None
        return robot_game

@router.post("/robot_games/")
def create_robot_game(robot_game: RobotGame):
    with Session(engine) as session:
        session.add(robot_game)
        session.commit()
        session.refresh(robot_game)
        return robot_game

@router.patch("/robot_games/{game_id}/{robot_id}")
def update_robot_game(game_id: int, robot_id: int, robot_game: RobotGame):
    with Session(engine) as session:
        robot_game_db = session.get(RobotGame, (game_id, robot_id))
        if robot_game_db is None:
            return None
        if robot_game.pos_x is not None:
            robot_game_db.pos_x = robot_game.pos_x
        if robot_game.pos_y is not None:
            robot_game_db.pos_y = robot_game.pos_y

        session.add(robot_game_db)
        session.commit()
        session.refresh(robot_game_db)
        return robot_game_db

@router.put("/robot_games/{game_id}/{robot_id}")
def update_robot_game(game_id: int, robot_id: int, robot_game: RobotGame):
    with Session(engine) as session:
        robot_game_db = session.get(RobotGame, (game_id, robot_id))
        if robot_game_db is None:
            return None
        robot_game_db.pos_x = robot_game.pos_x
        robot_game_db.pos_y = robot_game.pos_y
        session.add(robot_game_db)
        session.commit()
        session.refresh(robot_game_db)
        return robot_game_db

@router.delete("/robot_games/{game_id}/{robot_id}")
def delete_robot_game(game_id: int, robot_id: int):
    with Session(engine) as session:
        robot_game = session.get(RobotGame, (game_id, robot_id))
        if robot_game is None:
            return None
        session.delete(robot_game)
        session.commit()
        return robot_game
