# from .multilingual import *
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from keras.models import model_from_json
import pickle
from googletrans import Translator
import sys
import os
from django.http import JsonResponse
# Create your views here.


def predict_lang(text):

    # json_file = open('model_org.json', 'r')
    json_file = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'model_org.json'),'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    # model.load_weights("model_org.h5")
    model.load_weights(os.path.join(os.path.dirname(os.path.realpath(__file__)),'model_org.h5'))
    model.compile(optimizer= 'adam', loss='categorical_crossentropy', metrics = ['accuracy'])
    # vectorizer = pickle.load(open('vectorizer_original.pkl', 'rb'))
    vectorizer = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'vectorizer_original.pkl'),'rb'))

    # scaler = pickle.load(open('scaler_original.pkl', 'rb'))
    scaler = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'scaler_original.pkl'),'rb'))

    # pca = pickle.load(open('pca_original.pkl', 'rb'))
    pca = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'pca_original.pkl'),'rb'))
    
    # int2label = pickle.load(open('int2label_org.pkl', 'rb'))
    int2label = pickle.load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'int2label_org.pkl'),'rb'))
    
    text = np.array([text])
    y_pred_single = model.predict(pca.transform(scaler.transform(vectorizer.transform(text).toarray())))
    y_pred_single_val = np.argmax(y_pred_single, axis=1)
    return int2label[y_pred_single_val[0]]


@csrf_exempt
def text(request):
	if request.method == 'POST':
		input_text = request.POST['text_input']
		#model code
		model_code = predict_lang(input_text)
		
		#translated input
		translateinput = translate_input(input_text)
		#translated initial input
		translateiniatial = translate_iniatial()
		response = {
		"text_response":translateiniatial
		}

		return JsonResponse(response)

