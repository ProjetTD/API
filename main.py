from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, Session, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///../RVA_bdd.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Player(Base):
    __tablename__ = "player"
    id_player = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    score = Column(Integer)
    level = Column(Integer)
    ressources = Column(Integer)

    games = relationship("Game", back_populates="player")

class Robot(Base):
    __tablename__ = "robot"
    id_robot = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    cost = Column(Integer)
    power = Column(Integer)
    reload_time = Column(Integer)

class AlienGame(Base):
    __tablename__ = "alien_game"
    id_game = Column(Integer, ForeignKey("game.id_game"), primary_key=True, index=True)
    id_alien = Column(Integer, ForeignKey("alien.id_alien"), primary_key=True, index=True)
    pos_x = Column(Integer)
    pos_y = Column(Integer)

class RobotGame(Base):
    __tablename__ = "robot_game"
    id_game = Column(Integer, ForeignKey("game.id_game"), primary_key=True, index=True)
    id_robot = Column(Integer, ForeignKey("robot.id_robot"), primary_key=True, index=True)
    pos_x = Column(Integer)
    pos_y = Column(Integer)

class Alien(Base):
    __tablename__ = "alien"
    id_alien = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    power = Column(Integer)
    speed = Column(Integer)
    health = Column(Integer)
    drop = Column(Integer)

class Game(Base):
    __tablename__ = "game"
    id_game = Column(Integer, primary_key=True, index=True)
    id_player = Column(Integer, ForeignKey("player.id_player"))
    id_level = Column(Integer, ForeignKey("level.id_level"))
    score = Column(Integer)
    status = Column(String, index=True)

    player = relationship("Player", back_populates="games")
    level = relationship("Level", back_populates="games")

class Level(Base):
    __tablename__ = "level"
    id_level = Column(Integer, primary_key=True, index=True)
    number = Column(Integer)
    number_of_alien = Column(Integer)
    reward = Column(Integer)

    games = relationship("Game", back_populates="level")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_all_players(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Player).offset(skip).limit(limit).all()

# def get_all_robots(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Robot).offset(skip).limit(limit).all()

# def get_all_aliens(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Alien).offset(skip).limit(limit).all()

# def get_all_games(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Game).offset(skip).limit(limit).all()

# def get_all_levels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(Level).offset(skip).limit(limit).all()

# def get_all_robots_in_game(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return db.query(RobotGame).offset(skip).limit(limit).all()

# @app.get("/")
# def default():
#     return {'name': 'rva', 'version': '1.0.0', 'environement': 'production'}

# @app.get("/players/")
# async def read_all_players(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_all_players(skip=skip, limit=limit, db=db)

@app.post("/players/")
async def create_player(player: Player, db: Session = Depends(get_db)) -> Player:
    db.add(player)
    db.commit()
    db.refresh(player)
    return player

# @app.put("/players/{player_id}")
# async def update_player(player_id: int, updated_player: Player, db: Session = Depends(get_db)):
#     existing_player = db.query(Player).filter(Player.id_player == player_id).first()
#     if existing_player:
#         for key, value in updated_player.dict().items():
#             setattr(existing_player, key, value)
#         db.commit()
#         db.refresh(existing_player)
#         return existing_player
#     raise HTTPException(status_code=404, detail="Player not found")

# @app.delete("/players/{player_id}")
# async def delete_player(player_id: int, db: Session = Depends(get_db)):
#     player = db.query(Player).filter(Player.id_player == player_id).first()
#     if player:
#         db.delete(player)
#         db.commit()
#         return {"message": "Player deleted successfully"}
#     raise HTTPException(status_code=404, detail="Player not found")

# @app.get("/robots/")
# async def read_all_robots(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_all_robots(skip=skip, limit=limit, db=db)

# @app.post("/robots/")
# async def create_robot(robot: Robot, db: Session = Depends(get_db)):
#     db.add(robot)
#     db.commit()
#     db.refresh(robot)
#     return robot

# @app.put("/robots/{robot_id}")
# async def update_robot(robot_id: int, updated_robot: Robot, db: Session = Depends(get_db)):
#     existing_robot = db.query(Robot).filter(Robot.id_robot == robot_id).first()
#     if existing_robot:
#         for key, value in updated_robot.dict().items():
#             setattr(existing_robot, key, value)
#         db.commit()
#         db.refresh(existing_robot)
#         return existing_robot
#     raise HTTPException(status_code=404, detail="Robot not found")

# @app.delete("/robots/{robot_id}")
# async def delete_robot(robot_id: int, db: Session = Depends(get_db)):
#     robot = db.query(Robot).filter(Robot.id_robot == robot_id).first()
#     if robot:
#         db.delete(robot)
#         db.commit()
#         return {"message": "Robot deleted successfully"}
#     raise HTTPException(status_code=404, detail="Robot not found")

# @app.get("/aliens/")
# async def read_all_aliens(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_all_aliens(skip=skip, limit=limit, db=db)

# @app.post("/aliens/")
# async def create_alien(alien: Alien, db: Session = Depends(get_db)):
#     db.add(alien)
#     db.commit()
#     db.refresh(alien)
#     return alien

# @app.put("/aliens/{alien_id}")
# async def update_alien(alien_id: int, updated_alien: Alien, db: Session = Depends(get_db)):
#     existing_alien = db.query(Alien).filter(Alien.id_alien == alien_id).first()
#     if existing_alien:
#         for key, value in updated_alien.dict().items():
#             setattr(existing_alien, key, value)
#         db.commit()
#         db.refresh(existing_alien)
#         return existing_alien
#     raise HTTPException(status_code=404, detail="Alien not found")

# @app.delete("/aliens/{alien_id}")
# async def delete_alien(alien_id: int, db: Session = Depends(get_db)):
#     alien = db.query(Alien).filter(Alien.id_alien == alien_id).first()
#     if alien:
#         db.delete(alien)
#         db.commit()
#         return {"message": "Alien deleted successfully"}
#     raise HTTPException(status_code=404, detail="Alien not found")

# @app.get("/games/")
# async def read_all_games(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_all_games(skip=skip, limit=limit, db=db)

# @app.post("/games/")
# async def create_game(game: Game, db: Session = Depends(get_db)):
#     db.add(game)
#     db.commit()
#     db.refresh(game)
#     return game

# @app.put("/games/{game_id}")
# async def update_game(game_id: int, updated_game: Game, db: Session = Depends(get_db)):
#     existing_game = db.query(Game).filter(Game.id_game == game_id).first()
#     if existing_game:
#         for key, value in updated_game.dict().items():
#             setattr(existing_game, key, value)
#         db.commit()
#         db.refresh(existing_game)
#         return existing_game
#     raise HTTPException(status_code=404, detail="Game not found")

# @app.delete("/games/{game_id}")
# async def delete_game(game_id: int, db: Session = Depends(get_db)):
#     game = db.query(Game).filter(Game.id_game == game_id).first()
#     if game:
#         db.delete(game)
#         db.commit()
#         return {"message": "Game deleted successfully"}
#     raise HTTPException(status_code=404, detail="Game not found")

# @app.get("/levels/")
# async def read_all_levels(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_all_levels(skip=skip, limit=limit, db=db)

# @app.post("/levels/")
# async def create_level(level: Level, db: Session = Depends(get_db)):
#     db.add(level)
#     db.commit()
#     db.refresh(level)
#     return level

# @app.put("/levels/{level_id}")
# async def update_level(level_id: int, updated_level: Level, db: Session = Depends(get_db)):
#     existing_level = db.query(Level).filter(Level.id_level == level_id).first()
#     if existing_level:
#         for key, value in updated_level.dict().items():
#             setattr(existing_level, key, value)
#         db.commit()
#         db.refresh(existing_level)
#         return existing_level
#     raise HTTPException(status_code=404, detail="Level not found")

# @app.delete("/levels/{level_id}")
# async def delete_level(level_id: int, db: Session = Depends(get_db)):
#     level = db.query(Level).filter(Level.id_level == level_id).first()
#     if level:
#         db.delete(level)
#         db.commit()
#         return {"message": "Level deleted successfully"}
#     raise HTTPException(status_code=404, detail="Level not found")

# @app.get("/robots_in_game/")
# async def read_all_robots_in_game(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return get_all_robots_in_game(skip=skip, limit=limit, db=db)

# @app.post("/robots_in_game/")
# async def create_robot_in_game(robot_game: RobotGame, db: Session = Depends(get_db)):
#     db.add(robot_game)
#     db.commit()
#     db.refresh(robot_game)
#     return robot_game

# @app.put("/robots_in_game/{robot_game_id}")
# async def update_robot_in_game(robot_game_id: int, updated_robot_game: RobotGame, db: Session = Depends(get_db)):
#     existing_robot_game = db.query(RobotGame).filter(RobotGame.id_game == robot_game_id).first()
#     if existing_robot_game:
#         for key, value in updated_robot_game.dict().items():
#             setattr(existing_robot_game, key, value)
#         db.commit()
#         db.refresh(existing_robot_game)
#         return existing_robot_game
#     raise HTTPException(status_code=404, detail="Robot in game not found")

# @app.delete("/robots_in_game/{robot_game_id}")
# async def delete_robot_in_game(robot_game_id: int, db: Session = Depends(get_db)):
#     robot_game = db.query(RobotGame).filter(RobotGame.id_game == robot_game_id).first()
#     if robot_game:
#         db.delete(robot_game)
#         db.commit()
#         return {"message": "Robot in game deleted successfully"}
#     raise HTTPException(status_code=404, detail="Robot in game not found")