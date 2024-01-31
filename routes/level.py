from fastapi import APIRouter
from sqlmodel import Session, create_engine

from models.level import Level, engine

router = APIRouter()

@router.get("/levels/")
def read_levels():
    with Session(engine) as session:
        levels = session.query(Level).all()
        return levels

@router.post("/levels/")
def create_level(level: Level):
    with Session(engine) as session:
        session.add(level)
        session.commit()
        session.refresh(level)
        return level

@router.patch("/levels/{level_id}")
def update_level(level_id: int, level: Level):
    with Session(engine) as session:
        level_db = session.get(Level, level_id)
        if level_db is None:
            return None
        level_db.number = level.number
        level_db.number_of_alien = level.number_of_alien
        level_db.reward = level.reward
        session.add(level_db)
        session.commit()
        session.refresh(level_db)
        return level_db

@router.put("/levels/{level_id}")
def update_level(level_id: int, level: Level):
    with Session(engine) as session:
        level_db = session.get(Level, level_id)
        if level_db is None:
            return None
        level_db.number = level.number
        level_db.number_of_alien = level.number_of_alien
        level_db.reward = level.reward
        session.add(level_db)
        session.commit()
        session.refresh(level_db)
        return level_db

@router.delete("/levels/{level_id}")
def delete_level(level_id: int):
    with Session(engine) as session:
        level = session.get(Level, level_id)
        if level is None:
            return None
        session.delete(level)
        session.commit()
        return level
