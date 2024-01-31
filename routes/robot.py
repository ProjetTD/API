from fastapi import APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, create_engine

from models.robot import Robot, engine

router = APIRouter()

@router.get("/robots/")
def read_robots():
    with Session(engine) as session:
        robots = session.query(Robot).all()
        return robots

@router.post("/robots/")
def create_robot(robot: Robot):
    with Session(engine) as session:
        session.add(robot)
        session.commit()
        session.refresh(robot)
        return robot

@router.patch("/robots/{robot_id}")
def update_robot(robot_id: int, robot: Robot):
    with Session(engine) as session:
        robot_db = session.get(Robot, robot_id)
        if robot_db is None:
            return None
        robot_db.name = robot.name
        robot_db.cost = robot.cost
        robot_db.power = robot.power
        robot_db.reload_time = robot.reload_time
        session.add(robot_db)
        session.commit()
        session.refresh(robot_db)
        return robot_db

@router.put("/robots/{robot_id}")
def update_robot(robot_id: int, robot: Robot):
    with Session(engine) as session:
        robot_db = session.get(Robot, robot_id)
        if robot_db is None:
            return None
        robot_db.name = robot.name
        robot_db.cost = robot.cost
        robot_db.power = robot.power
        robot_db.reload_time = robot.reload_time
        session.add(robot_db)
        session.commit()
        session.refresh(robot_db)
        return robot_db

@router.delete("/robots/{robot_id}")
def delete_robot(robot_id: int):
    with Session(engine) as session:
        robot = session.get(Robot, robot_id)
        if robot is None:
            return None
        session.delete(robot)
        session.robot()
        return robot
