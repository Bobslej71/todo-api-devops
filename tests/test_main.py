"""
Testy jednostkowe dla TODO List API
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app, todos_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """Resetuj bazę danych przed każdym testem"""
    todos_db.clear()
    import app.main
    app.main.next_id = 1
    yield

def test_read_root():
    """Test endpointu głównego"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "TODO List API"

def test_health_check():
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_empty_todos():
    """Test pobierania pustej listy zadań"""
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    """Test tworzenia nowego zadania"""
    todo_data = {
        "title": "Test zadanie",
        "description": "Opis testowego zadania",
        "completed": False
    }
    response = client.post("/todos", json=todo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["id"] == 1
    assert "created_at" in data

def test_get_todo():
    """Test pobierania konkretnego zadania"""
    # Najpierw utwórz zadanie
    todo_data = {"title": "Test zadanie", "completed": False}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Pobierz zadanie
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == todo_data["title"]

def test_get_nonexistent_todo():
    """Test pobierania nieistniejącego zadania"""
    response = client.get("/todos/999")
    assert response.status_code == 404

def test_update_todo():
    """Test aktualizacji zadania"""
    # Utwórz zadanie
    todo_data = {"title": "Stare zadanie", "completed": False}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Zaktualizuj zadanie
    updated_data = {"title": "Nowe zadanie", "completed": True}
    response = client.put(f"/todos/{todo_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Nowe zadanie"
    assert response.json()["completed"] is True

def test_delete_todo():
    """Test usuwania zadania"""
    # Utwórz zadanie
    todo_data = {"title": "Zadanie do usunięcia", "completed": False}
    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    # Usuń zadanie
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200

    # Sprawdź czy zostało usunięte
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404

def test_multiple_todos():
    """Test tworzenia i pobierania wielu zadań"""
    # Utwórz kilka zadań
    for i in range(3):
        client.post("/todos", json={"title": f"Zadanie {i+1}", "completed": False})

    # Pobierz wszystkie
    response = client.get("/todos")
    assert response.status_code == 200
    assert len(response.json()) == 3
