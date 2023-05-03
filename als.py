import os
from spleeter.separator import Separator
import wave
import pyaudio
import matplotlib.pyplot as plt
import numpy as np

def Read_mv():
    read_file = "Get my way!"
    separator = Separator("spleeter:2stems")
    separator.separate_to_file("F:\\my file\\Anime\\gotoku\\op ed\\"+ read_file+".mp3", "data\\" + read_file)

def Read_wav(FileName):
    try:
        wr = wave.open(FileName, "r")
    except FileNotFoundError: #ファイルが存在しなかった場合
        print("[Error 404] No such file or directory: " + FileName)
        return 0
    data = wr.readframes(wr.getnframes())
    wr.close()
    x = np.abs(np.frombuffer(data, dtype="int16") / float((2^15)))
    r = np.array([], dtype="int8")
    for i in range(int(x.size / 100000)):
        r = np.append(r, int(np.sum(x[i*100000:i*100000+100000] / 100000)))
    np.savetxt('data/result/np_savetxt.txt', r)
    plt.plot(np.arange(r.size), r)
    plt.show()

if __name__ == "__main__":
    Read_wav("data/Get my way!/Get my way!/vocals.wav")
