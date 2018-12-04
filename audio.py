from pydub import AudioSegment
import os
import numpy as np
import random
import subprocess
from tempfile import NamedTemporaryFile
import string

tempfiles = []
processes = []

def _play_with_ffplay(seg,f):
    seg.export(f, "wav")
    return subprocess.Popen(['ffplay', "-nodisp", "-autoexit", "-hide_banner", f])

def giverd():
    t = [random.gauss(0.5,0.5) for i in range(1000)]
    s= sum(t)
    return [i/s for i in t]

def givewavs(folder):
    return [os.path.join(dp, f) for dp, dn, fn in os.walk(folder) for f in 
                                        fn if 
                                        f[-3:]=='mp3' or 
                                        f[-3:]=='wav']

MUSIC_FOLDERS = ['wav']
BEAT_FOLDERS=[r'Adrien Fertier_Lo-fi Rock/Loop']
SINGLE_FOLDERS = [r'Adrien Fertier_Lo-fi Rock/Single Hit']
SINGLE_NUM = 4

allsamples = []
for folder in MUSIC_FOLDERS:
    allsamples = allsamples + givewavs(folder)
    
beats = []
for folder in BEAT_FOLDERS:
    beats = beats + givewavs(folder)
beats = np.array(beats)

singles = []
for folder in SINGLE_FOLDERS:
    singles = singles + givewavs(folder)
singles = np.array(singles)

print(str(len(beats)) + 'beats')
print(str(len(singles)) + 'singles')
print(str(len(allsamples)) + 'samples')

# USE THIS - vector, class
def mix(arr,cl):
    print("cl: " + str(cl))
    print("arr: " + str(arr))
    beat = AudioSegment.from_file(beats[cl])
    #single_i = np.argpartition(singles, -SINGLE_NUM)[-SINGLE_NUM:]
    single_i = [int(i * 135 / 1000) for i in np.argpartition(arr[0], -SINGLE_NUM)[-SINGLE_NUM:]]
    single_as = [AudioSegment.from_file(i) for i in singles[single_i[:-1]]]

    t = beat
    for i,s in enumerate(single_as):
        times = beat.duration_seconds/2.5
        t = t.overlay(s[:2500], position=i*500)
    n = 'temp/' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

    t.export(n,format='wav')

    print("returning: " + n)
    return n

# def mix2(arr,cl,bbox):
    

if __name__ == "__main__":
    n = mix(giverd(),random.randint(0,19))
    input('Play?')
    print(n)
    p =subprocess.Popen(['ffplay', "-nodisp", "-autoexit", "-hide_banner", n])
    p.wait()

# files = np.array([f+'\\' + i for i in os.listdir(f) if i[-3:]=='mp3' or i[-3:]=='wav'])
# mix = [1,5,17]
