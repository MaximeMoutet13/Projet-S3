__author__ = "maxime"
__file__ = "modelisation.py"
__date__ = "08/11/19"

import numpy as np
import matplotlib.pyplot as plt
import Paramètres
from mpl_toolkits.mplot3d import Axes3D


def F(t, Y):
    return np.array([[Y[3],
                      Y[4],
                      Y[5],
                      Y[0] * (Y[4] ** 2 + np.sin(Y[1]) ** 2 * Y[5] ** 2) - G * M / (Y[0] ** 2),
                      -(2 * Y[3] * Y[4]) / Y[0] + np.sin(Y[1]) * np.cos(Y[1]) * Y[5] ** 2,
                      -2 * Y[3] * Y[5] / Y[0] - 2 * Y[4] * Y[5] / np.tan(Y[1])]])


def euler_explicite(F, tinit, Tfinal, yinit, h):
    N = round((Tfinal - tinit) / h)
    if isinstance(yinit, np.ndarray):
        d = len(yinit)
    else:
        d = 1
    y = np.zeros((d, N + 1))
    y[:, 0] = yinit
    tn = tinit
    for n in range(N):
        y[:, n + 1] = y[:, n] + h * F(tn, y[:, n])
        tn = tn + h
    return y


M = 4e9 * Paramètres.M_Soleil
G = Paramètres.G_p_MS

t0 = 0
Tf = (153 // 3) * 3.154e+7
h = 1000

r0 = 1000
theta0 = np.pi / 4
phi0 = np.pi / 4

alpha = np.pi / 4
beta = np.pi / 4

r0_p = np.cos(alpha)
theta0_p = np.sin(alpha) * np.cos(beta) / r0
phi0_p = np.sin(alpha) * np.sin(beta) / (r0 * np.sin(theta0))

Yinit = np.array([r0, theta0, phi0, r0_p, theta0_p, phi0_p])
Y = euler_explicite(F, t0, Tf, Yinit, h)

r_t, theta_t, phi_t = Y[0, :], Y[1, :], Y[2, :]
N = round((Tf - t0) / h)
t = t0 + np.arange(N + 1) * h

fig = plt.figure()
x = r_t * np.sin(theta_t) * np.cos(phi_t)
y = r_t * np.sin(theta_t) * np.sin(phi_t)
z = r_t * np.cos(theta_t)
plt.plot(t, x)
plt.show()

