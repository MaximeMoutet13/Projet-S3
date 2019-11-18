__author__ = "maxime"
__file__ = "Exo7.py"
__date__ = 30 / 10 / 19

import numpy as np
import matplotlib.pyplot as plt


def euler_explicite(f, tinit, Tfinal, yinit, h):
    if isinstance(yinit, np.ndarray):
        dim = len(yinit)
    else:
        dim = 1

    N = round((Tfinal - tinit) / h)
    tn = tinit
    Y = np.zeros((dim, N + 1))
    Y[:, 0] = yinit

    for i in range(N):
        Y[:, i + 1] = Y[:, i] + h * f(tn, Y[:, i])
        tn += h

    return Y


def Heun(f, tinit, Tfinal, yinit, h):
    if isinstance(yinit, np.ndarray):
        dim = len(yinit)
    else:
        dim = 1

    N = round((Tfinal - tinit) / h)
    tn = tinit
    Y = np.zeros((dim, N + 1))
    Y[:, 0] = yinit

    for i in range(N):
        y2 = Y[:, i] + h * f(tn, Y[:, i])
        Y[:, i + 1] = Y[:, i] + h / 2 * (f(tn, Y[:, i]) + f(tn + h, y2))
        tn += h

    return Y


def RK4(f, tinit, Tfinal, yinit, h):
    if isinstance(yinit, np.ndarray):
        dim = len(yinit)
    else:
        dim = 1

    N = round((Tfinal - tinit) / h)
    tn = tinit
    Y = np.zeros((dim, N + 1))
    Y[:, 0] = yinit

    for i in range(N):
        a = Y[:, i] + h / 2 * f(tn, Y[:, i])
        b = Y[:, i] + h / 2 * f(tn + h / 2, a)
        c = Y[:, i] + h / 2 * f(tn + h / 2, b)
        Y[:, i + 1] = Y[:, i] + h / 6 * (f(tn, Y[:, i]) + 2 * f(tn + h / 2, a) + 2 * f(tn + h / 2, b) + f(tn + h, c))
        tn += h

    return Y


def f0(a, b):
    return b


def sol_exacte_f0(t, tinit, yinit):
    return yinit * np.exp(t - tinit)


ti = 0
Tf = 5
h_test = [1, 0.1, 0.05, 0.01, 0.05, 0.001]
yi = 1
Eeul = []
Eheun = []
ERK = []
aff = True
for h in h_test:
    N = round((Tf - ti) / h)
    t = (ti + np.arange(N + 1) * h).reshape((1, N + 1))
    yeul = euler_explicite(f0, ti, Tf, yi, h)
    yheun = Heun(f0, ti, Tf, yi, h)
    yRK = RK4(f0, ti, Tf, yi, h)
    phiex = sol_exacte_f0(t, ti, yi)
    if aff:
        plt.figure(0)
        plt.plot(t.T, yeul.T, 'x', t.T, yheun.T, 's', t.T, yRK.T, 'o', t.T, phiex.T)
        plt.legend(['sol app Euler', 'sol app Heun', 'sol app RK4', 'sol exact'])
        aff = False
    eeul = np.max(np.abs(yeul - phiex))
    eheun = np.max(np.abs(yheun - phiex))
    eRK = np.max(np.abs(yRK - phiex))
    Eeul.append(eeul)
    Eheun.append(eheun)
    ERK.append(eRK)

plt.figure(1)
plt.plot(h_test, Eeul, 'x', h_test, Eheun, 's', h_test, ERK, 'o')
plt.figure(2)
plt.loglog(h_test, Eeul, 'x', h_test, Eheun, 's', h_test, ERK, 'o', h_test, h_test, h_test, np.array(h_test) ** 2,
           h_test, np.array(h_test) ** 4)
plt.legend(['Erreur Euler', 'Erreur Heun', 'Erreur RK', '$y = h$', '$y = h^2$', '$y=h^4$'])
plt.show()
