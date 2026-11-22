import numpy as np

# Газовая постоянная, Дж/(моль·К)
R = 8.314

# Атмосферное давление, Па
PA = 101325

# Давление насыщенных паров воды, Па, при температурах, °C (таблица из т4.3)
TEMPS = [20, 22, 24, 26, 28, 30]
PW0 = [2336.8, 2642.4, 2982.4, 3360.0, 3778.5, 4241.7]

# Молярные массы, кг/моль, и числа степеней свободы молекул (таблица из т4.2)
M_N2, M_O2, M_AR, M_CO2, M_H2O = 0.02801, 0.03200, 0.03995, 0.04401, 0.01802
I_N2, I_O2, I_AR, I_CO2, I_H2O = 5, 5, 3, 6, 6

# Доли газов в сухом воздухе (т4.3). X_O2 — сумма долей кислорода и CO2: 0,2095 + 0,0003
X_N2, X_O2, X_AR = 0.7809, 0.2098, 0.0093


def h2oFraction(temperature, rh):
    pw0 = np.interp(temperature, TEMPS, PW0)   # давление насыщенных паров, Па
    h2oX = rh / 100 * pw0 / PA                 # мольная доля паров воды
    return h2oX


def speedOfSound(temperature, h2oX, co2Max):
    T = temperature + 273.15
    co2 = np.linspace(0, co2Max / 100, 51)
    k = 1 - h2oX
    xN2 = X_N2 * k
    xO2 = (X_O2 - co2) * k
    xAr = X_AR * k
    xCO2 = co2 * k
    M = M_N2 * xN2 + M_O2 * xO2 + M_AR * xAr + M_CO2 * xCO2 + M_H2O * h2oX
    Cv = (I_N2 * xN2 + I_O2 * xO2 + I_AR * xAr + I_CO2 * xCO2 + I_H2O * h2oX) / 2 * R
    Cp = Cv + R
    soundSpeed = np.sqrt(Cp / Cv * R * T / M)
    return co2 * 100, soundSpeed
