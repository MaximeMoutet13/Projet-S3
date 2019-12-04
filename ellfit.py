#!//usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from main import nuage_points


def fun(p, d):
    X = d[:, 0]
    Y = d[:, 1]

    a = p[0]
    b = p[1]
    x0 = p[2]
    y0 = p[3]
    al = p[4]

    if (al > np.pi) or (al < 0):
        return 1e30

    x = X - x0
    y = Y - y0
    t = (((x * np.cos(al) + y * np.sin(al)) / a) ** 2 + ((-y * np.cos(al) + x * np.sin(al)) / b) ** 2 - 1) ** 2
    return np.sum(t)


# ----------------

fig = plt.figure()

# ----------------

i = 29
ref = 17
u = nuage_points(i, ref)

d = np.array(u)


X = d[:, 0]
Y = d[:, 1]

# ----------------
'''
a = 5
b = 2
u = -1
v = 1
t_rot = 0.55

t = np.linspace(0, 2*np.pi, 20)
Ell = np.array([a*np.cos(t) , b*np.sin(t)])  
R_rot = np.array([[np.cos(t_rot) , -np.sin(t_rot)],[np.sin(t_rot) , np.cos(t_rot)]])
Ell_rot = np.zeros((2,Ell.shape[1]))
for i in range(Ell.shape[1]):
  Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])

X = u+Ell_rot[0,:] + np.random.normal(scale=0.2,size=t.size)
Y = v+Ell_rot[1,:] + np.random.normal(scale=0.2,size=t.size)
d = np.array([X,Y]).T
'''
# ----------------

plt.plot(X, Y, '.')

# étoile d'indice 22: angle 0; 27: angle pi; 16: angle pi / 5 pour obtenir les meilleures ellipses
guess = [0.5 * (X.max() - X.min()), 0.5 * (Y.max() - Y.min()), X.mean(), Y.mean(), np.pi / 5]
res = minimize(fun, guess, args=d, method='Nelder-Mead', tol=1e-9)

print(res.x)

# ----------------

a = res.x[0]
b = res.x[1]
u = res.x[2]
v = res.x[3]
t_rot = res.x[4]

t = np.linspace(0, 2 * np.pi, 100)
Ell = np.array([a * np.cos(t), b * np.sin(t)])
R_rot = np.array([[np.cos(t_rot), -np.sin(t_rot)], [np.sin(t_rot), np.cos(t_rot)]])
Ell_rot = np.zeros((2, Ell.shape[1]))
for i in range(Ell.shape[1]):
    Ell_rot[:, i] = np.dot(R_rot, Ell[:, i])
plt.plot(u + Ell_rot[0, :], v + Ell_rot[1, :], 'lightblue')

# plt.xlabel("x , en nombre de pixels")
# plt.ylabel("y , en nombre de pixels")
# plt.legend()
# plt.title("Ellipse optimisée pour les points de l'étoile 4")
# plt.grid()
# plt.savefig("ell4.png")
plt.show()