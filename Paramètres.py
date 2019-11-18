__author__ = "maxime"
__file__ = "Paramètres.py"
__date__ = "12/11/19"

import numpy as np

G = 6.674e-11
echelle = 10 / 38
parsec = 3.26156 #AL
AL = 9.461e+15 #mètre
parsec2 = 3.086e+16 #mètres
M_Soleil = 2e30

G_p_MS = G / (parsec2 ** 3 * M_Soleil)

b_AL = 19.304 * echelle
b_metres = b_AL * AL
b_parsec = b_AL * parsec
a_AL = 38.052 * echelle
a_metres = a_AL * AL
a_parsec = a_AL * parsec
t_rot = -0.692
x0, y0 = 109.203, 159.219

# point12 = u[0]
# point0 = u[-1]
#
# coeff_dir_12 = (point12[1] - y0) / (point12[0] - x0)
# coeff_dir_0 = (point0[1] - y0) / (point0[0] - x0)
# coeff_dir_a = (a_AL * np.sin(t_rot)) / (a_metres * np.cos(t_rot))
#
# angle12 = abs(np.arctan(coeff_dir_12)) + abs(t_rot)
# angle0 = abs(np.arctan(coeff_dir_0)) - abs(t_rot)
#
#
# def perimetre(a, b):
#     return 2 * np.pi * np.sqrt((a ** 2 + b ** 2) / 2)


def Masse(T, a, G):
    return (4 * np.pi * a ** 3) / (T ** 2 * G)


T = (153 // 3) * 3.154e+7

M = Masse(T, a_metres, G)
print((M / M_Soleil) * 10 ** (-6))
