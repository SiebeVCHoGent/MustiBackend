import random

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/', response_class=HTMLResponse)
def get_home():
    with open('./files/index.html', 'r') as f:
        html = f.read()
    return html


@app.get("/musti")
def get_musti():
    statusses = ['Aanwezig', "Niet aanwezig", "Op weg naar buiten"]

    return {"status": random.choice(statusses)}

@app.get("/model/retrain")
def retrain_model():
    return 'retrained'