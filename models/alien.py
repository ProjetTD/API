from sqlmodel import Field, SQLModel, create_engine

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Alien(SQLModel, table=True):
    id_alien: int = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    power: int
    speed: int
    health: int
    drop: int

SQLModel.metadata.create_all(engine)
