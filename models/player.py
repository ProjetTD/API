from sqlmodel import Field, SQLModel, create_engine

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Player(SQLModel, table=True):
    id_player: str = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    score: int
    level: int
    ressources: int
    win: int
    lose: int

SQLModel.metadata.create_all(engine)
