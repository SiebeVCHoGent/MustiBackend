from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/musti")
def read_root():
    return {"Hello": "World"}
