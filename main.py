import random
import os
import re
import datetime as dt
import base64
import pickle

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from xgboost import train

from model.train import train_model, read_image, get_status

CHECK_EVERY_SECONDS = 60
FILE_PATH = './files/images'
MODEL_SAVE_PATH = './model/model.pickles'
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
    try:
        # get most recent picture
        biggest = max(last_files, key=lambda f: f[1])
        
        with open(biggest[0], 'rb') as im:
            imageB64 = base64.b64encode(im.read())

        # read model
        model = pickle.load(open(MODEL_SAVE_PATH, 'rb'))
        
        if model:
            pred = model.predict(read_image(biggest[0]))
            status = get_status(pred)
        else:
            status = 'Model niet geladen'

        test = None
        statusses = ['Aanwezig', "Niet aanwezig", "Op weg naar buiten"]
    except Exception as e:
        print(e)
        status = 'Model niet geladen'
        imageB64 = ''

    return {"status": status, 'image': imageB64}

@app.on_event('startup')
@repeat_every(seconds=CHECK_EVERY_SECONDS)
def retrain_model():
    global last_files
    def to_date(date_str):
        return dt.datetime.strptime(date_str, '%Y%m%d_%H%M%S')
    
    files = []
    reg = re.compile('[\d]{8}_[\d]{6}.jpg$')
    for dir in list(os.walk(FILE_PATH)):
        files.extend([dir[0] + '/' + f for f in dir[2] if reg.match(os.path.basename(f))])

    files = [(f, to_date(os.path.splitext(os.path.basename(f))[0]))  for f in files]

    if files != last_files:
        last_files = files
        retrain_model()


def retrain_model():
    # model = train_model()
    # pickle.dump(model, open(MODEL_SAVE_PATH, 'wb'))
    print('Model retrained')
