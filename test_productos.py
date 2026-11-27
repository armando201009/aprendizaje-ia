from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from main import app, get_db
from models import Base

SQLALCHEMY_DATABASE_URL = "sqlite://"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def token():
    r = client.post("/login", data={"username": "admin", "password": "admin123"})
    assert r.status_code == 200
    return r.json()["access_token"]

def test_listar_productos():
    r = client.get("/productos")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_crear_producto_devuelve_id():
    r = client.post(
        "/productos",
        json={"nombre": "Tubo PVC", "precio": 150, "existencia": 10},
        headers={"Authorization": f"Bearer {token()}"},
    )
    assert r.status_code == 201
    assert "id" in r.json()

def test_crear_sin_token_da_401():
    r = client.post(
        "/productos",
        json={"nombre": "Tubo PVC", "precio": 150, "existencia": 10},
    )
    assert r.status_code == 401


def test_get_producto_inexistente_da_404():
    r = client.get("/productos/999")
    assert r.status_code == 404
    assert r.json() == {"detail": "Producto no encontrado"}

def test_actualizar_producto():
    creado = client.post(
        "/productos",
        json={"nombre": "Cemento", "precio": 285, "existencia": 5},
        headers={"Authorization": f"Bearer {token()}"},
    )
    assert creado.status_code == 201
    pid = creado.json()["id"]
    r = client.put(
        f"/productos/{pid}",
        json={"nombre": "Cemento", "precio": 300, "existencia": 5},
        headers={"Authorization": f"Bearer {token()}"},
    )
    assert r.status_code == 200
    assert r.json()["precio"] == 300

def test_eliminar_producto():
    creado = client.post(
        "/productos",
        json={"nombre": "Arena", "precio": 100, "existencia": 20},
        headers={"Authorization": f"Bearer {token()}"},
    )
    pid = creado.json()["id"]
    r = client.delete(
        f"/productos/{pid}",
        headers={"Authorization": f"Bearer {token()}"},
    )
    assert r.status_code == 204
    r2 = client.get(f"/productos/{pid}")
    assert r2.status_code == 404

def test_login_contrasena_mal_da_401():
    r = client.post("/login", data={"username": "admin", "password": "mala"})
    assert r.status_code == 401
