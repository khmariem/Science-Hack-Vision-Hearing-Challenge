from pydub import AudioSegment
from pydub.playback import play
import os
import numpy as np

# f='wav\\Hackathon\\Background'
# files = np.array([f+'\\' + i for i in os.listdir(f) if i[-3:]=='mp3' or i[-3:]=='wav'])

# mix = [1,2]
# files = [
#     'wav\Synth-RundFunk2.wav',
#     'wav\bensound-hey.mp3'
# ]
# files = [f + '\\' + i for i in files]
# sounds = np.array([AudioSegment.from_file(i, format=i[-3:]) for i in files])
# f = 'filename'
s2= AudioSegment.from_file(r'wav\Hackathon\Single\Drum_Dumpf.wav', format='wav')
s1 = AudioSegment.from_file(r'wav\Hackathon\Background\All the things you love.wav', format='wav')
# t = sounds[0].overlay(sounds[1])
# for s in sounds[1:]:
#     t = t.overlay(s)

t = s1.overlay(s2)
play(t)