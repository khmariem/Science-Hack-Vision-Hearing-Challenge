from pydub import AudioSegment
from pydub.playback import play
import os
import numpy as np

f='wav\\Hackathon\\Background'
files = np.array([f+'\\' + i for i in os.listdir(f) if i[-3:]=='mp3' or i[-3:]='wav'])
mix = [1,2]

sounds = np.array([AudioSegment.from_file(i, format=i[-3:]) for i in files[mix]])

t = sounds[0].overlay(sounds[1])
for s in sounds[1:]:
    t = t.overlay(s)
play(t)