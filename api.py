from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.alien import router as alien_router
from routes.robot import router as robot_router
from routes.game import router as game_router
from routes.player import router as player_router
from routes.robot_game import router as robot_game_router
from routes.alien_game import router as alien_game_router
from routes.level import router as level_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alien_router)
app.include_router(robot_router)
app.include_router(game_router)
app.include_router(player_router)
app.include_router(robot_game_router)
app.include_router(alien_game_router)
app.include_router(level_router)
