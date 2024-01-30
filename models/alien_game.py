from sqlmodel import Field, SQLModel, create_engine

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class AlienGame(SQLModel, table=True):
    id_game: int = Field(primary_key=True, index=True)
    id_alien: int = Field(primary_key=True, index=True)
    pos_x: int
    pos_y: int

SQLModel.metadata.create_all(engine)
