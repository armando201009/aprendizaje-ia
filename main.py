from fastapi import FastAPI

app = FastAPI(title="ERP Satélite API")

@app.get("/")
def root():
    return {"mensaje": "API ERP Satélite funcionando"}

@app.get("/salud")
def salud():
    return {"estado": "ok", "base_datos": "erp_demo"}
