import subprocess

# command = "ffmpeg -i /Users/nilansh/Desktop/file2.wav -ab 160k -ac 2 -ar 44100 -vn audio_converted.wav"

command = "ffmpeg -i /Users/nilansh/Desktop/file2.wav audio_converted.wav"


subprocess.call(command, shell=True)
