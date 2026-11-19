import sys
import numpy as np
import matplotlib.pyplot as plt
import soundPico as pico
name = sys.argv[1]
dataPath = "scripts/data/"
threshold = 20
pico.initPico()

try:
    mic0, mic1 = pico.capture(threshold)
finally:
    pico.deinitPico()

np.savetxt(dataPath + name + "_0.txt", mic0, fmt="%d")
np.savetxt(dataPath + name + "_1.txt", mic1, fmt="%d")

plt.plot(mic0, label="микрофон 0")
plt.plot(mic1, label="микрофон 1")
plt.xlabel("номер отсчета")
plt.ylabel("код АЦП")
plt.legend()
plt.show()