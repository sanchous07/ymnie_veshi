import numpy as np
import matplotlib.pyplot as plt
import soundFunctions as s

def min_square_method(a):
    xy = sum([a[j] * j for j in range(len(a))]) / len(a)
    x = sum([j for j in range(len(a))]) / len(a)
    y = sum([a[j] for j in range(len(a))]) / len(a)
    x2 = sum([j**2 for j in range(len(a))]) / len(a)
    a = (xy-x*y)/(x2-x**2)
    return a

def count_derivative(a, n=70):
    b = []
    for i in range(len(a)-n):
         b.append(min_square_method(a[i:i+n]))
    return b

def normilize(a):
    k = 1/(max(a)-min(a))
    for i in range(len(a)):
        a[i] = a[i]*k
    return a

def find_mean_square_error(a,b):
    error = 0
    for i in range(min(len(a), len(b))):
        error+=(a[i]-b[i])**2
    return error/min(len(a), len(b))

def find_tau_1(a, b):
    a1 = normilize(count_derivative(count_derivative(a)))
    b1 = normilize(count_derivative(count_derivative(b)))
    best_tau = 0.0
    best_error = 99999999
    for tau in range(int(0.5*len(a))):
        error = find_mean_square_error(b1[tau:], a1[:(len(a1) - tau)])
        if error < best_error:
            best_tau = tau
            best_error = error
    return best_tau * 0.004

def meaning(a, n=50):
    b = []
    for i in range(len(a)-n):
        b.append(sum(a[i:i+n])/n)
    return b

L = 1.158
t, rh = 24.0, 36.4

#t, rh = 21.9, 34

co2, speedRoom = s.speedOfSound(t, s.h2oFraction(t, rh), 5)
co2, speedWet = s.speedOfSound(t, s.h2oFraction(t, 100), 5)

fitRoom = np.polyfit(speedRoom, co2, 1)
fitWet = np.polyfit(speedWet, co2, 1)
print("Прямая, влажность аудитории:", fitRoom)
print("Прямая, влажность 100 %:", fitWet)

plt.plot(co2, speedRoom, label="влажность %d %%" % rh)
plt.plot(co2, speedWet, label="влажность 100 %")
plt.xlabel("Доля CO₂ в сухом воздухе, %")
plt.ylabel("Скорость звука, м/с")
plt.grid()
plt.legend()

for i in range(1,17):
    dataPath = "data/"
    name_air = f"air{i}/data"
    #name_breath = "breath1/data"

    mic_air_1 = np.loadtxt(dataPath + name_air + "_0.txt")[:2000]
    mic_air_2 = np.loadtxt(dataPath + name_air + "_1.txt")[:2000]
    #mic_breath_1 = np.loadtxt(dataPath + name_breath + "_0.txt")[:2000]
    #mic_breath_2 = np.loadtxt(dataPath + name_breath + "_1.txt")[:2000]

    tau_air = find_tau_1(mic_air_1, mic_air_2)
    #tau_breath = find_tau_1(mic_breath_1, mic_breath_2)

    tauAir = np.array([tau_air])
    #tauBreath = np.array([tau_breath])

    cAir = L / (np.mean(tauAir) / 1000)
    #cBreath = L / (np.mean(tauBreath) / 1000)

    co2Air = np.polyval(fitRoom, cAir)
    #co2Breath = np.polyval(fitWet, cBreath)

    print(f"Измерение {i}:","Воздух: c = %.1f м/с, CO2 = %.1f %%" % (cAir, co2Air))
    #print("Выдох:  c = %.1f м/с, CO2 = %.1f %%" % (cBreath, co2Breath))

for j in range(1,4):
    dataPath = "data/"
    name_breath = f"breath{j}/data"

    mic_breath_1 = np.loadtxt(dataPath + name_breath + "_0.txt")[:2000]
    mic_breath_2 = np.loadtxt(dataPath + name_breath + "_1.txt")[:2000]

    tau_breath = find_tau_1(mic_breath_1, mic_breath_2)

    tauBreath = np.array([tau_breath])

    cBreath = L / (np.mean(tauBreath) / 1000)

    co2Breath = np.polyval(fitWet, cBreath)

    print("Выдох:  c = %.1f м/с, CO2 = %.1f %%" % (cBreath, co2Breath))