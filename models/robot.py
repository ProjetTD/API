from sqlmodel import Field, SQLModel, create_engine

sqlite_file_name = "database.sqlite3"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

class Robot(SQLModel, table=True):
    id_robot: int = Field(primary_key=True, index=True)
    name: str = Field(index=True)
    cost: int
    power: int
    reload_time: float
    health: int

SQLModel.metadata.create_all(engine)
