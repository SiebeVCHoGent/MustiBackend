# Python ≥3.5 is required
from operator import index
import sys
from matplotlib import axis
assert sys.version_info >= (3, 5)

# Scikit-Learn ≥0.20 is required
import sklearn
assert sklearn.__version__ >= "0.20"
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

#Classifiers
from sklearn.ensemble import RandomForestClassifier

# Common imports
import numpy as np
import pandas as pd
import os
import tarfile
import cv2
import pickle

np.random.seed(42)

def target_value(val):
    if val == 'aanwezig':
        return 2
    if val == 'buiten':
        return 1
    return 0

def get_status(pred):
    if pred == [2]:
        return 'Aanwezig'
    if pred == [1]:
        return 'Op weg naar buiten'
    return "Niet aanwezig"

def load_dataframe():
    PATH = './files/images'

    if not os.path.isdir(PATH):
        raise Exception('Extracted files not found')


    # Get grayscale values from pictures
    print('Creating dataframe')
    samples = []
    sample_counter = 0
    musti = pd.DataFrame()

    for folder in os.listdir(PATH):
        if not os.path.isdir(PATH + '/' + folder):
            print(folder)
            continue

        for file in os.listdir(f'{PATH}/{folder}'):
            print(folder, file, target_value(folder))
            img = cv2.imread(f'{PATH}/{folder}/{file}', 0)
            img = cv2.normalize(img,np.zeros((640, 352)), 0, 1000)
            # add them to a dataframe
            imgd = dict()
            imgd['target'] = target_value(folder)
            c = 0
            for i in img.flatten():
                c += 1
                imgd[f'p{c}'] = i
            samples.append(imgd)
            sample_counter+=1

            if sample_counter % 200 == 0:
                print('working')
                temp_df = pd.DataFrame.from_dict(samples)
                musti = musti.append(temp_df, ignore_index=True)
                samples = []

    temp_df = pd.DataFrame.from_dict(samples)
    musti = musti.append(temp_df, ignore_index=True)
    samples = []

    print('Dataframe loaded')
    return musti


CREATE_DATAFRAME = True
def train_model():
    if CREATE_DATAFRAME:
        musti = load_dataframe()
        pickle.dump(musti, open('./model/df.pick', 'wb'))
    else:
        musti = pickle.load(open('./model/df.pick', 'rb'))

    musti.info()
    X, y = musti.drop('target', axis=1), musti['target']
    y = y.astype(np.uint8)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    pickle.dump(scaler, open('./model/scaler.pickles', 'wb'))
    X_test = scaler.transform(X_test)

    # fit model
    model = RandomForestClassifier(n_estimators= 185, max_features= 11, random_state= 42)
    print('fitting model')
    model.fit(X_train, y_train)
    print('model fitted')
    return model

def read_image(path):
    img = cv2.imread(path, 0)
    img = cv2.normalize(img, np.zeros((640, 352)), 0, 1000)

    imgd = dict()
    c = 0
    flatted = img.flatten()

    for i in flatted:
        c += 1
        imgd[f'p{c}'] = [i]

    df = pd.DataFrame.from_dict(imgd)

    # Read Scaler
    scaler = pickle.load(open('./model/scaler.pickles', 'rb'))

    df = scaler.transform(df)
    return df