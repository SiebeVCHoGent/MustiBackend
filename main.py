import random
import os
import datetime as dt
import base64

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

CHECK_EVERY_SECONDS = 5
FILE_PATH = './files/images'
last_files = list()

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
    biggest = max(last_files, key=lambda f: f[1])

    with open(FILE_PATH + '/' + biggest[0], 'rb') as im:
        imageB64 = base64.b64encode(im.read())

    statusses = ['Aanwezig', "Niet aanwezig", "Op weg naar buiten"]

    return {"status": random.choice(statusses), 'image': imageB64}

@app.on_event('startup')
@repeat_every(seconds=CHECK_EVERY_SECONDS)
def retrain_model():
    global last_files
    def to_date(str):
        return dt.datetime.strptime(str, '%Y%m%d_%H%M%S')
    
    files = [(f, to_date(os.path.splitext(f)[0])) for f in os.listdir(FILE_PATH)]
    if files != last_files:
        last_files = files
        retrain_model()
    print(files)


def retrain_model():
    print('RETRAINING')
