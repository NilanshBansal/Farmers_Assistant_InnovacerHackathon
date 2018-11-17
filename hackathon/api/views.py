from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
import io

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.conf import settings
import subprocess
from django.http import JsonResponse


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


@csrf_exempt
def postout(request):

	data = request.FILES.get('file')
	path = default_storage.save('file2.wav', ContentFile(data.read()))
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

	transcript = stt(content)
	print("TRANSCRIPT: ",transcript)

	# f.write(request.FILES.get('file'))
	# print(f.read())
	# f.close()

	print("------------------------------------------------------------------------------------")
	return JsonResponse({"transcript":transcript})



# if __name__ == '__main__':
#     file_name = 'audio_converted.wav'

#     # Loads the audio into memory
#     with io.open(file_name, 'rb') as audio_file:
#         content = audio_file.read()

#     transcript = stt(content)
#     print("TRANSCRIPT: ",transcript)
#     df = []

#     with io.open('transcript3_new1.txt', 'w') as text_file:
#         text_file.write(transcript)







# Create your views here.

# @csrf_exempt
# def speechtotext(request):
# 	r = sr.Recognizer()

# 	with sr.Microphone() as source:
# 	print('Say Something:')
# 	audio = r.listen(source)
# 	print ('Done!')

# 	text = r.recognize_google(audio, language = request.POST['text_input'])

# 	print (text)

# 	print (r.recognize_google(audio))

# 	response = {
# 	"text" : text
# 	}
# 	return JsonResponse(response)
