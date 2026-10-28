# The web server (FastAPI). It lists what the frontend can ask for.
# Run:  python main.py     then open  http://127.0.0.1:8000
from pathlib import Path

import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import database
from ai import ask_ai
from analysis import analyse
from fake_data import make_reading
from settings import PUMPS

app = FastAPI()

# Let the frontend call the API from another site (e.g. Cloudflare Pages).
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")                                           # for Render's health check
def health():
    return {"status": "ok"}


def analyse_pump(pump):
    """Read the readings from Supabase and analyse them."""
    if pump not in PUMPS:
        raise HTTPException(404, "Pump not found")

    first = database.get_oldest(pump, 200)                     # the healthy pump
    latest = list(reversed(database.get_newest(pump, 200)))    # oldest -> newest
    if len(latest) == 0:
        raise HTTPException(400, "No readings for this pump. Add one on the Manage page.")

    result = analyse(pd.DataFrame(first), pd.DataFrame(latest))
    result["pump"] = pump
    result["service"] = PUMPS[pump]["service"]
    return result


# ---------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------
@app.get("/api/pumps")
def list_pumps():
    return [{"name": name, "service": info["service"]} for name, info in PUMPS.items()]


@app.get("/api/analysis/{pump}")
def get_analysis(pump: str):
    return analyse_pump(pump)


@app.get("/api/insight/{pump}")
def get_insight(pump: str):
    result = analyse_pump(pump)
    return {"text": ask_ai(pump, result["service"], result)}


@app.post("/api/simulate/{pump}")
def simulate(pump: str):
    """Live update: add one new fake reading."""
    hour = database.count_readings(pump)
    database.add_reading(make_reading(pump, hour))
    return {"ok": True}


# ---------------------------------------------------------------
# MANAGE PAGE: Create, Read, Update, Delete (CRUD)
# ---------------------------------------------------------------
class Values(BaseModel):                  # the 4 numbers of a reading
    vibration: float
    bearing_temp: float
    discharge_pressure: float
    flow: float


class NewReading(Values):                 # a new reading also needs the pump name
    pump: str


@app.get("/api/readings")                                     # READ
def read_readings(pump: str):
    return database.get_newest(pump, 15)


@app.post("/api/readings")                                    # CREATE
def create_reading(item: NewReading):
    database.add_reading(item.model_dump())
    return {"ok": True}


@app.put("/api/readings/{reading_id}")                        # UPDATE
def update_reading(reading_id: int, values: Values):
    database.update_reading(reading_id, values.model_dump())
    return {"ok": True}


@app.delete("/api/readings/{reading_id}")                     # DELETE
def delete_reading(reading_id: int):
    database.delete_reading(reading_id)
    return {"ok": True}


# ---------------------------------------------------------------
# Show the frontend folder as the website (keep this at the END)
# ---------------------------------------------------------------
frontend_folder = Path(__file__).parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_folder, html=True))

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
