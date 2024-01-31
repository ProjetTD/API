from fastapi import APIRouter, Depends
from sqlmodel import Session, create_engine

from models.alien import Alien, engine

router = APIRouter()

@router.get("/aliens/")
def read_aliens():
    with Session(engine) as session:
        aliens = session.query(Alien).all()
        return aliens

@router.post("/aliens/")
def create_alien(alien: Alien):
    with Session(engine) as session:
        session.add(alien)
        session.commit()
        session.refresh(alien)
        return alien

@router.patch("/aliens/{alien_id}")
def update_alien(alien_id: int, alien: Alien):
    with Session(engine) as session:
        alien_db = session.get(Alien, alien_id)
        if alien_db is None:
            return None
        if alien.name is not None:
            alien_db.name = alien.name
        if alien.power is not None:
            alien_db.power = alien.power
        if alien.speed is not None:
            alien_db.speed = alien.speed
        if alien.health is not None:
            alien_db.health = alien.health
        if alien.drop is not None:
            alien_db.drop = alien.drop
        
        session.add(alien_db)
        session.commit()
        session.refresh(alien_db)
        return alien_db

@router.put("/aliens/{alien_id}")
def update_alien(alien_id: int, alien: Alien):
    with Session(engine) as session:
        alien_db = session.get(Alien, alien_id)
        if alien_db is None:
            return None
        alien_db.name = alien.name
        alien_db.power = alien.power
        alien_db.speed = alien.speed
        alien_db.health = alien.health
        alien_db.drop = alien.drop
        session.add(alien_db)
        session.commit()
        session.refresh(alien_db)
        return alien_db

@router.delete("/aliens/{alien_id}")
def delete_alien(alien_id: int):
    with Session(engine) as session:
        alien = session.get(Alien, alien_id)
        if alien is None:
            return None
        session.delete(alien)
        session.commit()
        return alien
