from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

CLIENTES = {
    "1001": {"nombre": "Ana Torres", "saldo": 85000, "vence": "2026-10-20", "estado": "pendiente"},
    "1002": {"nombre": "Carlos Ruiz", "saldo": 0, "vence": "2026-10-15", "estado": "al día"},
    "1003": {"nombre": "Marta Gómez", "saldo": 142000, "vence": "2026-10-05", "estado": "vencida"},
}
RESUMENES = []

class Consulta(BaseModel):
    documento: str

class Resumen(BaseModel):
    cliente: str
    intencion: str
    pasos_intentados: str
    motivo_escalamiento: str
    sentimiento: str

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/consultar_saldo")
def consultar_saldo(c: Consulta):
    cli = CLIENTES.get(c.documento[-4:])
    if not cli:
        return {"encontrado": False}
    return {"encontrado": True, **cli}

@app.post("/generar_resumen")
def generar_resumen(r: Resumen):
    texto = (f"Cliente: {r.cliente}. Motivo: {r.intencion}. "
             f"Ya se intentó: {r.pasos_intentados}. "
             f"Se escala porque: {r.motivo_escalamiento}. Ánimo: {r.sentimiento}.")
    RESUMENES.append({"hora": datetime.now().isoformat(), "resumen": texto})
    return {"resumen": texto}

@app.get("/resumenes")
def resumenes():
    return RESUMENES
