__Author__ = "aillet"
__Filename__ = "model.py"
__Creationdate__ = "18/11/2019"

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation

# distance
conversion_metre = 2.59 * 10 ** 13 * (10 / 22)
b4 = 5.57822734 * conversion_metre
a4 = 9.18798322 * conversion_metre
ua = 150 * 10 ** 6  # convertion km en unité astronomique
b_ua = b4 / ua
c = np.sqrt(a4 ** 2 - b4 ** 2)  # distance réelle entre les deux foyers d'une ellipse
a_ua = (a4 / ua) / 10 ** (5)  # On réajuste nos valeur d'un facteur 10**5 de manière a obtenir une echelle utilisable
c_ua = c / ua
x_0 = (a_ua * 10 ** (5) - c_ua) / 10 ** (5)  # La plus courte distance entre l'etoile et un foyer
T0 = 13  # période suposé de notre étoile en années
val = (a_ua ** 3 * 4 * np.pi ** 2) / (T0 ** 2)

# conditions initales:
Tf = 13  # période supposé de notre étoile
t0 = 0
h = 0.005
Yinit = np.array([x_0, 0, 0, 10.32])


def f2(t, Y):
    # Fonction effectuant une premiere itération de notre schéma numérique c'est a dire kn
    def f2bis(a, b, c, d):
        return np.array([c,
                         d,
                         (-val * a) / ((a ** 2 + b ** 2) ** (3 / 2)),
                         (-val * b) / ((a ** 2 + b ** 2) ** (3 / 2))])

    Y2 = f2bis(Y[0], Y[1], Y[2], Y[3])
    return Y2


def f(t, Y, Ybis, h):
    # Cette fonction permet de calculer kn'
    return np.array([
        Y[2] + (h / 2) * Ybis[2],
        Y[3] + (h / 2) * Ybis[3],
        (-val * (Y[0] + (h / 2) * Ybis[0])) / (
                (((Y[0] + (h / 2) * Ybis[0]) ** 2) + ((Y[1] + (h / 2) * Ybis[1]) ** 2)) ** (3 / 2)),
        ((-val * (Y[1] + (h / 2) * Ybis[1])) / (
                (((Y[0] + (h / 2) * Ybis[0]) ** 2) + ((Y[1] + (h / 2) * Ybis[1]) ** 2)) ** (3 / 2)))
    ])


def epsilon(Ybis1, Ybis2, h):
    # permet de calculer epsilon de maniere à savoir si nous augmentons ou diminuons le pas h
    return (h / 2) * (((Ybis2[0] - Ybis1[0]) ** 2) + ((Ybis2[1] - Ybis1[1]) ** 2) + ((Ybis2[2] - Ybis1[2]) ** 2) + (
            (Ybis2[3] - Ybis1[3]) ** 2)) ** (1 / 2)


def Euler_Richardson(tinit, Tfinal, yinit, h, epsis):
    # schéma d'euler-richardson
    hbis = h
    N = round((Tfinal - tinit) / h)
    if isinstance(yinit, np.ndarray):
        d = len(yinit)
    else:
        d = 1
    y = np.zeros((d, N + 1))
    y[:, 0] = yinit
    tn = tinit
    n = 0
    while n < N:

        Ybis1 = f2(tn, y[:, n])

        Ybis2 = f(tn, y[:, n], Ybis1, hbis)
        epsi = epsilon(Ybis1, Ybis2, hbis)
        a = epsi / epsis
        hbis = 0.9 * hbis / a ** (1 / 2)
        if a > 1:
            y[:, n + 1] = y[:, n]
            print(1)
        else:
            y[:, n + 1] = y[:, n] + hbis * Ybis2
            tn = tn + hbis
            n += 1
    return y


"""
Code permettant d'effectuer le schéma d'Euler_explicite
def Euler_explicite(tinit, Tfinal, yinit, h):
    hbis = h
    N = round((Tfinal - tinit) / h)
    if isinstance(yinit, np.ndarray):
        d = len(yinit)
    else:
        d = 1
    y = np.zeros((d, N + 1))
    y[:, 0] = yinit
    tn = tinit
    for n in range (N):
        y[:, n + 1] = y[:, n] + hbis * f2(tn, y[:, n])
        tn = tn + h
    return y
"""

Y = Euler_Richardson(t0, Tf, Yinit, h, 0.00005)
# on prend une erreur seuil très faible pour avoir une bonne précision sur l'ellipse
thetha = np.pi / 4  # angle de projection

fig = plt.figure()
ax = p3.Axes3D(fig)

xR, yR = Y[0, :], Y[1, :]
zR = xR * 0
xbis, ybis, zbis = xR, yR, ((xR ** 2 + yR ** 2) ** (1 / 2) * np.tan(thetha) - Yinit[0])

# affichage
pointbis, = ax.plot(xbis, ybis, zbis, 'o', label="Etoile_4 projetée d'angle pi/4")
point, = ax.plot([xR[0]], [yR[0]], [zR[0]], 'o', label='Etoile_4')

ax.plot([-12], [0], [0], 'o', label='Trou noir')

line, = ax.plot(xR, yR, zR, label="trajectoire de l'Etoile")
linebis, = ax.plot(xbis, ybis, zbis, label="trajectectoir projetée d'angle pi/4")

# Setting the axes properties
ax.set_xlim3d([-13, 2.0])
ax.set_xlabel('X ua e+5')

ax.set_ylim3d([-5.0, 5.0])
ax.set_ylabel('Y ua e+5')

ax.set_zlim3d([0.0, 10.0])
ax.set_zlabel('Z ua e+5')

ax.set_title('Modelisation Euler-Richardson')
plt.legend()


def animate(n, x, y, z, point):
    # fonction pour animer une étoile sur la trajectoire
    point.set_data(np.array([x[n], y[n]]))
    point.set_3d_properties(z[n], 'z')
    return point


ani = animation.FuncAnimation(fig, animate, frames=2600, fargs=(xR, yR, zR, point), interval=1)
ani2 = animation.FuncAnimation(fig, animate, frames=2600, fargs=(xbis, ybis, zbis, pointbis), interval=1)
plt.show()
