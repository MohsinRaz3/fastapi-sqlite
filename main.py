from sqlmodel import SQLModel, Session, select
from fastapi import FastAPI, HTTPException, Depends 
from model import Todo, ReadTodo, CreateTodo, engine
from typing import List


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="todo app",
    description="an todo application",
    docs_url="/docs",
    version="v1"
)

@app.on_event("startup")
async def startup_event():
    create_db_and_table()

@app.get("/")
async def home_todo():
    return "home page"

@app.get("/todos", response_model=List[ReadTodo])
async def all_todos( session:Session = Depends(get_session))-> List[ReadTodo]:
    todos = session.exec(select(Todo)).all( )
    return todos

@app.get("/todos/{todo_id}", response_model=ReadTodo)
async def get_single_todo(todo_id:int, session: Session= Depends(get_session))->ReadTodo:
    todo = session.get(Todo,todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="todo not found")
    return todo

@app.post("/todos/", response_model=ReadTodo)
async def create_todos(todo:CreateTodo, session: Session = Depends(get_session)):
    new_todo = Todo.model_validate(todo)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo

@app.patch("/todos/{todo_id}", response_model=ReadTodo)
async def update_todo(todo_id: int, todo: Todo, session: Session = Depends(get_session)):
    todo_item = session.get(Todo, todo_id)
    if not todo_item:
        raise HTTPException(status_code=404, detail="no todo found")
    
    todo_data = todo.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(todo_item, key, value)

        session.add(todo_item)
        session.commit()
        session.refresh(todo_item)
        return todo_item



@app.delete("/todos/{todo_id}")
async def delete_todos(todo_id: int, session: Session = Depends(get_session)):
    delete_todo = session.get(Todo, todo_id)
    if not delete_todo:
        raise HTTPException(status_code=404, detail="not todo found")
    
    session.delete(delete_todo)
    session.commit()
    return {"OK": True}

