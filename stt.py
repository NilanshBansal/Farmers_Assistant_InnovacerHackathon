import io


def stt(blob, lang_code = 'en-US'):
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
        #sample_rate_hertz=8000)

    # config = types.RecognitionConfig(
    # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    # sample_rate_hertz=16000,
    # language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)
    for result in response.results:
        return result.alternatives[0].transcript


if __name__ == '__main__':
    file_name = 'audio_converted.wav'

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()

    transcript = stt(content)
    print("TRANSCRIPT: ",transcript)
    df = []

    with io.open('transcript3_new1.txt', 'w') as text_file:
        text_file.write(transcript)
