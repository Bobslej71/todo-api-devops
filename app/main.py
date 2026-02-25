"""
TODO List API - Główny plik aplikacji
"""
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(
    title="TODO List API",
    description="Prosta aplikacja do zarządzania zadaniami",
    version="1.0.0"
)

# Model danych
class TodoItem(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: Optional[datetime] = None

# Prosta baza danych w pamięci
todos_db: List[TodoItem] = []
next_id = 1

@app.get("/")
def read_root():
    """Przekierowanie na dokumentację API"""
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
    """Pobierz wszystkie zadania"""
    return todos_db

@app.get("/todos/{todo_id}", response_model=TodoItem)
def get_todo(todo_id: int):
    """Pobierz konkretne zadanie"""
    for todo in todos_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Zadanie nie zostało znalezione")

@app.post("/todos", response_model=TodoItem, status_code=201)
def create_todo(todo: TodoItem):
    """Utwórz nowe zadanie"""
    global next_id
    todo.id = next_id
    todo.created_at = datetime.now()
    next_id += 1
    todos_db.append(todo)
    return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, updated_todo: TodoItem):
    """Zaktualizuj zadanie"""
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            updated_todo.id = todo_id
            updated_todo.created_at = todo.created_at
            todos_db[index] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Zadanie nie zostało znalezione")

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Usuń zadanie"""
    for index, todo in enumerate(todos_db):
        if todo.id == todo_id:
            todos_db.pop(index)
            return {"message": "Zadanie zostało usunięte"}
    raise HTTPException(status_code=404, detail="Zadanie nie zostało znalezione")
