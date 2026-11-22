import numpy as np
import matplotlib.pyplot as plt
import requests
import os
import base64
import soundFunctions as s

def min_square_method(a):
    xy = sum([a[j] * j for j in range(len(a))]) / len(a)
    x = sum([j for j in range(len(a))]) / len(a)
    y = sum([a[j] for j in range(len(a))]) / len(a)
    x2 = sum([j**2 for j in range(len(a))]) / len(a)
    a = (xy-x*y)/(x2-x**2)
    return a

def count_derivative(a, n=10):
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

def find_max(a):
    mx = 0
    ans = 0
    for i in range(len(a)):
        if a[i][1] > mx:
            mx = a[i][1]
            ans = i
    return ans, mx

def find_min(a):
    mn = 99999999999
    ans = 0
    for i in range(len(a)):
        if a[i][1] < mn:
            mn = a[i][1]
            ans = i
    return ans, mn

def find_tau_1(a, b):
    a1 = normilize(count_derivative(a))
    b1 = normilize(count_derivative(b))
    best_tau = [[0, 99999999],[0, 99999999],[0, 99999999],[0, 99999999],[0, 99999999]]
    best_error = 99999999
    cr = 0
    for tau in range(int(0.5*len(a))):
        error = find_mean_square_error(a1[tau:], b1[:len(b1)-tau])
        if error < best_error:
            t = 1
            for i in range(5):
                if abs((-1)*tau - best_tau[i][0]) < 200 and i!=cr:
                    t = 0
                    if error < best_tau[i][1]:
                        best_tau[i][0] = (-1) * tau
                        best_tau[i][1] = error
                    break
            if t == 1:
                best_tau[cr][0] = (-1) * tau
                best_tau[cr][1] = error
                cr, best_error = find_max(best_tau)
    for tau in range(int(0.5*len(a))):
        error = find_mean_square_error(b1[tau:], a1[:len(b1)-tau])
        if error < best_error:
            t = 1
            for i in range(5):
                if abs(tau - best_tau[i][0]) < 200 and i!=cr:
                    t = 0
                    if error < best_tau[i][1]:
                        best_tau[i][0] = tau
                        best_tau[i][1] = error
                    break
            if t == 1:
                best_tau[cr][0] = tau
                best_tau[cr][1] = error
                cr, best_error = find_max(best_tau)
    for i in range(len(best_tau)):
        best_tau[i][0] *= 0.004
    return best_tau

def meaning(a, n=50):
    b = []
    for i in range(len(a)-n):
        b.append(sum(a[i:i+n])/n)
    return b

def find_spades(a, n=20, m=1000):
    b = []
    for i in range(m//2, len(a)-m//2-1):
        b.append((sum(a[i-m//2:i+m//2])/m-sum(a[i-n//2:i+n//2])/n))
    return b

def find_tau_2(a, b):
    a1 = normilize(find_spades(meaning(a)))
    b1 = normilize(find_spades(meaning(b)))
    best_tau = [[0, 99999999],[0, 99999999],[0, 99999999],[0, 99999999],[0, 99999999]]
    best_error = 99999999
    cr = 0
    for tau in range(int(0.5*len(a))):
        error = find_mean_square_error(b1[tau:], a1[:len(a)-tau])
        if error < best_error:
            t = 1
            for i in range(5):
                if abs(tau-best_tau[i][0]) < 200 and i!=cr:
                    t = 0
                    if error < best_tau[i][1]:
                        best_tau[i][0] = tau
                        best_tau[i][1] = error
            if t == 1:
                best_tau[cr][0] = tau
                best_tau[cr][1] = error
                cr, best_error = find_max(best_tau)
    for tau in range(int(0.5*len(a))):
        error = find_mean_square_error(a1[tau:], b1[:len(a)-tau])
        if error < best_error:
            t = 1
            for i in range(5):
                if abs((-1)*tau - best_tau[i][0]) < 200 and i!=cr:
                    t = 0
                    if error < best_tau[i][1]:
                        best_tau[i][0] = (-1) * tau
                        best_tau[i][1] = error
            if t == 1:
                best_tau[cr][0] = (-1) * tau
                best_tau[cr][1] = error
                cr, best_error = find_max(best_tau)
    for i in range(len(best_tau)):
        best_tau[i][0] *= 0.004
    return best_tau

def make_plot(a,b,tau=0,show=True,save=False):
    a = a - np.mean(a[:200])
    b = b - np.mean(a[:200])

    time0 = np.arange(len(a)) * 0.004 + tau
    time1 = np.arange(len(b)) * 0.004 + 0.002

    plt.title(f'график для тау равной {tau}')
    plt.plot(time0, a, label="микрофон 0")
    plt.plot(time1, b, label="микрофон 1")
    plt.xlabel("Время, мс")
    plt.legend()
    plt.grid()

    if show:
        plt.show()

    if save:
        plt.savefig(f'tmp/plot_{tau}.png')

    plt.close()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def message_to_lm(system_prompt: str, prompt: str, model: str = "local-model", temperature: float = 1.0, max_tokens: int = 8000, base_url: str = "http://127.0.0.1:1234/v1"):
    user_content = [{"type": "text", "text": prompt}]
    images = []
    for filename in os.listdir('tmp'):
        images.append(encode_image(os.path.join('tmp', filename)))
    for image in images:
        user_content.append({
        "type": "image_url",
        "image_url": {"url": f"data:image/png;base64,{image}"},
    })
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=300)
        response.raise_for_status()

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return None
    except:
        return 99999.0

def ask_AI(a,b,best_best_tau):
    for filename in os.listdir('tmp'):
        os.remove(os.path.join('tmp', filename))
    for i in range(len(best_best_tau)):
        make_plot(a,b,best_best_tau[i][0],False,True)
    promt = "Я делаю лабораторную работу и у меня есть 2 графика записей микрофонов, которые получились со сдвигом. Я подобрал несколько тау сдвигов, которые подозреваю в правильности. Посмотри на графики, что я приложил и напиши в ответ только одно число это лучшее тау сдвиг. Ориентируйся на провалы графика и характер убывания и возрастания функций"
    model = "google/gemma-4-e4b"
    answer = message_to_lm("", promt, model)
    if answer == 99999.0:
        ans, best_error = find_max(best_best_tau)
        return ans
    else:
        return float(answer)

def normilize_error(a):
    ans, min_error = find_min(a)
    for i in range(len(a)):
        a[i][1] = min_error/a[i][1]
    return a

def find_tau_general(a,b):
    best_tau_1 = normilize_error(find_tau_1(a,b))
    best_tau_2 = normilize_error(find_tau_2(a,b))
    best_tau = []
    for i in range(len(best_tau_1)):
        t = 1
        for j in range(len(best_tau)):
            if abs(best_tau[j][0]-best_tau_1[i][0])<1*0.004:
                t = 0
                best_tau[j][1]+=best_tau_1[i][1]
                best_tau[j][0] = 0.5*(best_tau[j][0]+best_tau_1[i][0])
        if t==1:
            best_tau.append([best_tau_1[i][0], best_tau_1[i][1]])
    for i in range(len(best_tau_2)):
        t = 1
        for j in range(len(best_tau)):
            if abs(best_tau[j][0]-best_tau_2[i][0])<5*0.004:
                t = 0
                best_tau[j][1]+=best_tau_2[i][1]
                best_tau[j][0] = 0.5*(best_tau[j][0]+best_tau_2[i][0])
        if t==1:
            best_tau.append([best_tau_2[i][0], best_tau_2[i][1]])
    ans, best_rating = find_max(best_tau)
    best_best_tau = []
    for i in range(len(best_tau)):
        if 1.3*best_tau[i][1] >= best_rating:
            best_best_tau.append(best_tau[i])
    if len(best_best_tau)>1:
        ans_tau = ask_AI(a,b,best_best_tau)
    else:
        ans_tau = best_best_tau[0][0]
    print(best_best_tau)
    return ans_tau

L = 1.158
t, rh = 24.0, 36.4

t, rh = 21.9, 34      # из conditions.txt

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

dataPath = "data_example/"
name_air = "air1"
name_breath = "breath1"

mic_air_1 = np.loadtxt(dataPath + name_air + "_0.txt")
mic_air_2 = np.loadtxt(dataPath + name_air + "_1.txt")
mic_breath_1 = np.loadtxt(dataPath + name_breath + "_0.txt")
mic_breath_2 = np.loadtxt(dataPath + name_breath + "_1.txt")

i, u = find_min(find_tau_1(mic_air_1, mic_air_2))
tau_air = find_tau_1(mic_air_1, mic_air_2)[i][0]
j, u = find_min(find_tau_1(mic_breath_1, mic_breath_2))
tau_breath = find_tau_1(mic_breath_1, mic_breath_2)[i][0]
'''

tau_air = find_tau_general(mic_air_1,mic_air_2)
tau_breath = find_tau_general(mic_breath_1, mic_breath_2)
'''

print(tau_air, tau_breath)

tauAir = np.array([tau_air])
tauBreath = np.array([tau_breath])

cAir = L / (np.mean(tauAir) / 1000)
cBreath = L / (np.mean(tauBreath) / 1000)

co2Air = np.polyval(fitRoom, cAir)
co2Breath = np.polyval(fitWet, cBreath)

print("Воздух: c = %.1f м/с, CO2 = %.1f %%" % (cAir, co2Air))
print("Выдох:  c = %.1f м/с, CO2 = %.1f %%" % (cBreath, co2Breath))

'''
dataPath = "data_example/"
name2 = "air1"
name1 = "breath1"

mic10 = np.loadtxt(dataPath + name1 + "_0.txt")
mic11 = np.loadtxt(dataPath + name1 + "_1.txt")
mic20 = np.loadtxt(dataPath + name2 + "_0.txt")
mic21 = np.loadtxt(dataPath + name2 + "_1.txt")

mic10 = mic10 - np.mean(mic10[:200])
mic11 = mic11 - np.mean(mic11[:200])
mic20 = mic20 - np.mean(mic20[:200])
mic21 = mic21 - np.mean(mic21[:200])

tau = find_tau_general(mic10, mic11)
print(tau)

time0 = np.arange(len(mic10)) * 0.004 + tau
time1 = np.arange(len(mic11)) * 0.004 + 0.002

plt.plot(time0, mic10, label="микрофон 0")
plt.plot(time1, mic11, label="микрофон 1")
plt.xlabel("Время, мс")
plt.legend()
plt.grid()
plt.show()
'''
