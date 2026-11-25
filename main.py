from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, Producto

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Satélite API")

@app.get("/")
def root():
    return {"mensaje": "API ERP Satélite funcionando"}

@app.get("/salud")
def salud():
    return {"estado": "ok", "base_datos": "erp_demo"}

@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()
