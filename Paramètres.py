__author__ = "maxime"
__file__ = "Paramètres.py"
__date__ = "12/11/19"

import numpy as np

G = 6.674 * 10 ** (-11)  # constante gravitationnelle (m3 kg-1 s-2)

echelle = 10 / 38  # mesurée à la main sur les images
light_day_metre = 2.59 * 10 ** 13  # valeur d'un jour lumière en mètres
conversion_metre = echelle * light_day_metre  # valeur d'un pixel sur les images en mètres

M_Soleil = 2 * 10 ** 30  # kg

# resultats de ellfit sur 3 étoiles:
etoile1 = [2.09015808e+01, 1.96049819e+01, -8.93978661e+01, 4.63626002e+01, 2.80114359e-15]
etoile2 = [22.55206895, 41.87228216, -85.25262962, 45.72639473, 3.14159265]
etoile3 = [1.30357974e+01, 1.94142139e+01, -7.29459896e+01, 1.96759027e+01, 2.15513863e-08]

etoileprof = [9.18798322, 5.57822734, 130.19721943, 137.80082187, 1.71578036]
# on prend les mesures des demi grands axes que l'on met en mètres
a1 = 20.9015808 * conversion_metre
a2 = 41.87228216 * conversion_metre
a3 = 19.4142139 * conversion_metre
ae = 9.18798322 * conversion_metre  # étoile qui parcourt une période entière

"""
# partie ou l'on tentait de mesurer le périmètre d'une ellipse, au final inutile
point12 = u[0]
point0 = u[-1]

coeff_dir_12 = (point12[1] - y0) / (point12[0] - x0)
coeff_dir_0 = (point0[1] - y0) / (point0[0] - x0)
coeff_dir_a = (a_AL * np.sin(t_rot)) / (a_metres * np.cos(t_rot))

angle12 = abs(np.arctan(coeff_dir_12)) + abs(t_rot)
angle0 = abs(np.arctan(coeff_dir_0)) - abs(t_rot)


def perimetre(a, b):
    return 2 * np.pi * np.sqrt((a ** 2 + b ** 2) / 2)
"""


def Masse(T, a, G):
    """Utilise la 3eme loi de Kepler pour calculer la masse du trou noir"""
    return (4 * (np.pi ** 2) * (a ** 3)) / ((T ** 2) * G)


Timages = (153 // 12) * 3.154 * 10 ** 7  # temps entre la première et la dernière image converti en secondes

# on utilise des relations linéaires entre la période totale et la période des images
T1 = 3 * Timages
T2 = 2 * Timages
T3 = 6 * Timages
Te = Timages

# Calculs de la masse (en nombre de masse solaires) pour les différentes étoiles
M1 = Masse(T1, a1, G) / M_Soleil
M2 = Masse(T2, a2, G) / M_Soleil
M3 = Masse(T3, a3, G) / M_Soleil
Me = Masse(Te, ae, G) / M_Soleil
print("M1=", M1, "\nM2=", M2, "\nM3=", M3, "\nMe=", Me)

M = (M1 + M2 + M3 + Me) / 4
print("Mmoyenne =", M)
