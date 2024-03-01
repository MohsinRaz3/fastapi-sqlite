from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

#create models
class BaseTodo(SQLModel):
    task: str
    is_complete: Optional[bool] = False


class Todo(BaseTodo, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class CreateTodo(BaseTodo):
    pass

class ReadTodo(BaseTodo):
    id: int    

class UpdateTodo(BaseTodo):
    task: Optional[str] = None
    is_complete: Optional[bool] = False


#create sqlite db
sqlite_filename = 'database.db'
sqlite_path = f"sqlite:///{sqlite_filename}"

#create engine
engine = create_engine(sqlite_path, echo=True)
