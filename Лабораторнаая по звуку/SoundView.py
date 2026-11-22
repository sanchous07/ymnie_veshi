import numpy as np
import matplotlib.pyplot as plt

def min_square_method(a):
    xy = sum([a[j] * j for j in range(len(a))]) / len(a)
    x = sum([j for j in range(len(a))]) / len(a)
    y = sum([a[j] for j in range(len(a))]) / len(a)
    x2 = sum([j**2 for j in range(len(a))]) / len(a)
    a = (xy-x*y)/(x2-x**2)
    return a

def count_derivative(a, n=100):
    b = []
    for i in range(len(a)-n):
         b.append(min_square_method(a[i:i+n]))
    return b

def normilize(a):
    k = 1/(max(a)-min(a))
    for i in range(len(a)):
        a[i] = a[i]*k
    return a

def meaning(a, n=100):
    b = []
    for i in range(len(a)-n):
        b.append(sum(a[i:i+n])/n)
    return b

dataPath = "data_example/"
name = "breath1"   # какую запись смотрим: air1, air2, breath1, ...

mic0 = normilize(meaning(count_derivative(np.loadtxt(dataPath + name + "_0.txt")[:2000])))
mic1 = normilize(meaning(count_derivative(np.loadtxt(dataPath + name + "_1.txt")[:2000])))

mic0 = mic0 - np.mean(mic0[:200])   # вычитаем фон, первые 200 отсчётов до импульса
mic1 = mic1 - np.mean(mic1[:200])

tau = 3.392

time0 = np.arange(len(mic0)) * 0.004 + tau   # время отсчётов, мс: шаг 4 мкс
time1 = np.arange(len(mic1)) * 0.004 + 0.002                # микрофон 1 измеряется на 2 мкс позже

plt.plot(time0, mic0, label="микрофон 0")
plt.plot(time1, mic1, label="микрофон 1")
plt.xlabel("Время, мс")
plt.legend()
plt.grid()
plt.show()