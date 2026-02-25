# TODO List API - Projekt DevOps

Prosty REST API do zarządzania listą zadań, zbudowany z użyciem FastAPI, Docker i GitHub Actions.

## Funkcjonalności

- Tworzenie nowych zadań (POST)
- Pobieranie listy wszystkich zadań (GET)
- Pobieranie szczegółów zadania (GET)
- Aktualizacja zadania (PUT)
- Usuwanie zadania (DELETE)
- Health check endpoint
- Automatyczna dokumentacja API (Swagger UI)

## Technologie

- **Python 3.11** - język programowania
- **FastAPI** - framework do budowania API
- **Uvicorn** - serwer ASGI
- **Pytest** - framework do testowania
- **Ruff** - linter dla kodu Python
- **Docker** - konteneryzacja aplikacji
- **GitHub Actions** - CI/CD pipeline

## Struktura projektu

```
todo-api-devops/
├── app/
│   └── main.py
├── tests/
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

