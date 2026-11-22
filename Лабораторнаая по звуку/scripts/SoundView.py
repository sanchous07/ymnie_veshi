import numpy as np
import matplotlib.pyplot as plt

dataPath = "../data/breath3/"
name = "data"

mic0 = np.loadtxt(dataPath + name + "_0.txt")
mic1 = np.loadtxt(dataPath + name + "_1.txt")

mic0 = mic0 - np.mean(mic0[:200])
mic1 = mic1 - np.mean(mic1[:200])

tau = 0.0

time0 = np.arange(len(mic0)) * 0.004 + tau
time1 = np.arange(len(mic1)) * 0.004 + 0.002

plt.plot(time0, mic0, label="микрофон 0")
plt.plot(time1, mic1, label="микрофон 1")
plt.xlabel("Время, мс")
plt.legend()
plt.grid()
plt.show()