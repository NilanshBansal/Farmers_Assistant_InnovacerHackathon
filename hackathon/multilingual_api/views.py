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
import requests
import pandas as pd
import io

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import subprocess
from django.http import JsonResponse

# Create your views here.
# speech to text function


def stt(blob, lang_code='en-US'):
    import os

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/nilansh/Downloads/Speech-to-text-Api-10b0792c0795.json"

    # Imports the Google Cloud client library
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe

    audio = types.RecognitionAudio(content=blob)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=lang_code)
    # sample_rate_hertz=8000)

    # config = types.RecognitionConfig(
    # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    # sample_rate_hertz=16000,
    # language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    for result in response.results:
        return result.alternatives[0].transcript


def predict_lang(text):

    # json_file = open('model_org.json', 'r')
    json_file = open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'model_org.json'), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    # model.load_weights("model_org.h5")
    model.load_weights(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'model_org.h5'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy', metrics=['accuracy'])
    # vectorizer = pickle.load(open('vectorizer_original.pkl', 'rb'))
    vectorizer = pickle.load(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'vectorizer_original.pkl'), 'rb'))

    # scaler = pickle.load(open('scaler_original.pkl', 'rb'))
    scaler = pickle.load(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'scaler_original.pkl'), 'rb'))

    # pca = pickle.load(open('pca_original.pkl', 'rb'))
    pca = pickle.load(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'pca_original.pkl'), 'rb'))

    # int2label = pickle.load(open('int2label_org.pkl', 'rb'))
    int2label = pickle.load(open(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'int2label_org.pkl'), 'rb'))

    text = np.array([text])
    y_pred_single = model.predict(pca.transform(
        scaler.transform(vectorizer.transform(text).toarray())))
    y_pred_single_val = np.argmax(y_pred_single, axis=1)
    return int2label[y_pred_single_val[0]]


def map_g_code(model_code):
    map_code = pd.read_csv(os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'languages.txt'), sep=",")
    g_code = map_code[map_code["model_code"] == model_code]["g_code"].item()
    return g_code


def translate_input(text):
    translator = Translator()
    response = translator.translate(text)
    return response.text


def translate_iniatial(text, g_code):
    translator = Translator()
    response = translator.translate(text, dest=g_code)
    return response.text


@csrf_exempt
def text(request):
    import numpy as np
    from keras.models import model_from_json
    import pickle
    from googletrans import Translator
    import sys
    import os
    import io
    import pandas as pd

    if request.method == 'POST':
        if request.POST['content_type'] == 'speech':
            lang_code = request.POST['lang_code']
            data = request.FILES.get('file')
            path = default_storage.save(
                'file2.wav', ContentFile(data.read()))
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
            print(tmp_file)
            # command = "ffmpeg -i /Users/nilansh/Desktop/file2.wav -ab 160k -ac 2 -ar 44100 -vn audio_converted.wav"

            command = "ffmpeg -i " + tmp_file + " audio_converted.wav -y"

            subprocess.call(command, shell=True)
            # f = open("audio_converted.wav", "r")

            file_name = 'audio_converted.wav'

            # Loads the audio into memory
            with io.open(file_name, 'rb') as audio_file:
                content = audio_file.read()

            transcript = stt(content, lang_code=lang_code)
            if transcript is not None:
                print("TRANSCRIPT: ", transcript)
            else:
                print("TRANSCRIPT IS NONE:")
                return JsonResponse({"text_response":"Voice not detected!"})
            # f.write(request.FILES.get('file'))
            # print(f.read())
            # f.close()

            model_code = predict_lang(transcript)
            # translated input
            bot_input = translate_input(transcript)
            # bot_input = bot_input.lower()
            # bot_input = bot_input.replace('rodent', 'rodents')
            # bot_input = bot_input.replace('pomegrenate', 'pomegrenate')
            # bot output

            url = "http://4faff15e.ngrok.io/main/" + bot_input
            output = requests.get(url)
            bot_output = output.text
            # get g_code
            g_code = map_g_code(model_code)
            # translated initial input
            translate_init = translate_iniatial(bot_output, g_code)
            response = {
                "text_response": translate_init
            }
            return JsonResponse(response)

        elif request.POST['content_type'] == 'text':

            input_text = request.POST['text_input']
            print(input_text)
            # model code
            model_code = predict_lang(input_text)
            # translated input
            bot_input = translate_input(input_text)
            # bot_input = bot_input.lower()
            # bot_input = bot_input.replace('rodent', 'rodents')
            # bot_input = bot_input.replace('pomegrenate', 'pomegrenate')
            # bot output

            url = "http://4faff15e.ngrok.io/main/" + bot_input
            output = requests.get(url)
            bot_output = output.text
            # get g_code
            g_code = map_g_code(model_code)
            # translated initial input
            translate_init = translate_iniatial(bot_output, g_code)
            response = {
                "model_code": model_code,
                "text_response": translate_init
            }
            return JsonResponse(response)
