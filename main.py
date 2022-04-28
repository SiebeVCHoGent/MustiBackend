from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import random

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


@app.get("/musti")
def read_root():
    statusses = ['Aanwezig', "Niet aanwezig", "Op weg naar buiten"]

    return {"status": random.choice(statusses)}
