# -*- coding: utf-8 -*-
import numpy as np
from keras.models import model_from_json
import pickle
from googletrans import Translator
import sys

sys.path.append('./multilingual_api/')

def predict_lang(text):

    json_file = open('model_org.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights("model_org.h5")
    model.compile(optimizer= 'adam', loss='categorical_crossentropy', metrics = ['accuracy'])
    vectorizer = pickle.load(open('vectorizer_original.pkl', 'rb'))
    scaler = pickle.load(open('scaler_original.pkl', 'rb'))
    pca = pickle.load(open('pca_original.pkl', 'rb'))
    int2label = pickle.load(open('int2label_org.pkl', 'rb'))
    text = np.array([text])
    y_pred_single = model.predict(pca.transform(scaler.transform(vectorizer.transform(text).toarray())))
    y_pred_single_val = np.argmax(y_pred_single, axis=1)
    return int2label[y_pred_single_val[0]]

def translate_input(text):
    translator = Translator()
    response = translator.translate(text)
    return response.text

def translate_iniatial(text, g_code):
    translator = Translator()
    response = translator.translate(text, dest=g_code)
    return response.text