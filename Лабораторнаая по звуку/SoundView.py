import numpy as np
import matplotlib.pyplot as plt

dataPath = "data/air12/"
name = "data"   # какую запись смотрим: air1, air2, breath1, ...

mic0 = np.loadtxt(dataPath + name + "_0.txt")
mic1 = np.loadtxt(dataPath + name + "_1.txt")

mic0 = mic0 - np.mean(mic0[:200])   # вычитаем фон, первые 200 отсчётов до импульса
mic1 = mic1 - np.mean(mic1[:200])

time0 = np.arange(len(mic0)) * 0.004   # время отсчётов, мс: шаг 4 мкс
time1 = time0 + 0.002                  # микрофон 1 измеряется на 2 мкс позже

plt.plot(time0, mic0, label="микрофон 0")
plt.plot(time1, mic1, label="микрофон 1")
plt.xlabel("Время, мс")
plt.legend()
plt.grid()
plt.show()