from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Producto

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Satélite API")

class ProductoCrear(BaseModel):
    nombre: str
    precio: float
    existencia: int = 0

@app.get("/")
def root():
    return {"mensaje": "API ERP Satélite funcionando"}

@app.get("/salud")
def salud():
    return {"estado": "ok", "base_datos": "erp_demo"}

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.post("/productos", status_code=201)
def crear_producto(producto: ProductoCrear, db: Session = Depends(get_db)):
    nuevo = Producto(**producto.model_dump())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
