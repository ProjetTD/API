from sqlmodel import Field, SQLModel, create_engine

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Game(SQLModel, table=True):
    id_game: int = Field(primary_key=True, index=True)
    id_player: int
    id_level: int
    score: int
    status: str

SQLModel.metadata.create_all(engine)
