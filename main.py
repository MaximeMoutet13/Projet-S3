from astropy.io import fits
import matplotlib.pyplot as plt
from photutils import DAOStarFinder
from astropy.stats import sigma_clipped_stats


def dao(i):
    """Entrée:
        i: numéro de l'image que l'on veut étudier
    Sortie:
        la liste des objets présents sur l'image i avec leurs données sous forme d'une liste de liste (indice de l'objet,
         coord x, coord y, sharpness, roundness 1, roundness 2, npix, sky, peak, flux, mag)
    """

    # Ouvre l'image format .fits suivante
    hdul = fits.open(
        '/home/maxime/Documents/Workspace Python/Project_S3/tn%d0.fts' % i)  # Modifier le chemin d'accès pour ouvrir les images
    hdu = hdul[0].data

    # On utilise des paramètres adaptés afin de détecter tous les objets sur l'image
    mean, median, std = sigma_clipped_stats(hdu, sigma=3.0)
    daofind = DAOStarFinder(fwhm=10.0, threshold=5 * std)
    sources = daofind(hdu - median)

    # Construit une table avec les données relatives aux objets détéctés
    for col in sources.colnames:
        sources[col].info.format = '%.8g'  # for consistent table output
    return sources


"""
# Affiche tous les objets détéctés sur l'image i
i = 0

k = dao(i)
plt.plot(k[1][:], k[2][:], "+r")
plt.show()
"""


def cherche_autour(etoile, daostarfinder, x, y):
    """Entrées:
        etoile: les données d'une étoile sur une image i,
        daostarfinder: les données de tous les objets sur l'image i + 1,
        x, y: une distance x et une distance y.
    Sortie:
        les données de l'objet qui 'ressemble' le plus a etoile sous forme d'une liste

    Cherche dans une zone rectangulaire xy autour des coordonnées de etoile l'objet qui possède les données les plus proches de etoile
    Ce programme n'est pas optimal mais il a permis de trouver les données dont nous avions besoin, il est donc tout a
    fait possible qu'il ne rende pas le resultat voulu, cela depend aussi de la precision de la detection des objets
    sur les images
    """

    list = []
    ecart = []

    # On parcourt les objets sur l'image i + 1 afin de comparer leurs données à celles de etoile
    for ligne in daostarfinder:

        # l'indice 1 correspond a la coordonnée x de l'objet, 2 sa coordonnée y
        if (abs((ligne[1] - etoile[1])) <= x):
            if ((abs(ligne[2] - (etoile[2])) <= y)):
                # On creer une liste contenant les objets a proximité de etoile (proximite definie par xy)
                list += [ligne]

    # On regarde maintenant les proprietes de chaque objet a proximite de etoile pour determiner lequel est le plu ressemblant
    for candidate in list:
        # On compare uniquement sharpness et mag car les tests ont montres qu'il permettait de trouver le bon objet
        ecart_sharpness = abs(candidate[3] - etoile[3])
        ecart_mag = abs(candidate[9] - etoile[9])
        ecart += [[ecart_sharpness, ecart_mag]]

    # On parcourt la liste des ecarts, on regarde l'objet qui possede l'ecart minimal (pour sharpness et mag) avec les donnees de etoile
    # et on ajoute l'indice de cet objet dans une liste tableau
    tableau = []
    for i in range(len(ecart[0])):
        u = 8000
        indice = None
        for j in range(len(ecart)):
            if ecart[j][i] <= u:
                u = ecart[j][i]
                indice = j
        tableau += [indice]

    # Dans le cas ou on ne trouve pas d'objet a proximite de etoile, les parametre x et y on mal ete choisis
    if ecart == []:
        return None

    tableau_bis = []
    # On compte le nombre de fois qu'apparait chaque indice d'objet dans tableau
    for g in range(len(ecart)):
        tableau_bis.append(tableau.count(g))

    # on choisit l'objet qui possede le plus d'inidices dans tableau soit celui qui a les parametres sharpness et mag
    # qui se rapprochent le plus de ceux de etoile
    NEXT = tableau_bis.index(max(tableau_bis))
    return list[NEXT]


def nuage_points(indice, iref):
    """Entrees:
        indice: indice sur l'image 1 de l'etoile dont l'on veut etudier la trajectoire
        iref: indice sur l'image 1 de l'etoile de référence par rapport a laquelle on veut calculer les coordonnées
    Sortie:
        les positions de l'étoile calculées en placant l'origine sur l'etoile de reference
        sur toutes les images sous la forme d'une liste
    """

    List1 = []
    a = dao(0)[indice]
    ref = dao(0)[iref]
    List1.append([a[1] - ref[1], a[2] - ref[2]])

    # On parcourt les images depuis la deuxieme a la derniere
    for i in range(11):
        # On utilise la fonction cherche_autour
        a = cherche_autour(dao(i)[a[0] - 1], dao(i + 1), 8, 8)
        ref = cherche_autour(dao(i)[ref[0] - 1], dao(i + 1), 8, 8)
        List1.append([a[1] - ref[1], a[2] - ref[2]])
    return List1


"""
# L'indice de l'etoile de reference sur l'image 1 est 17
# indices d'etoile qui parcourt beaucoup de distance sur les image: 22,

# Permet d'afficher les coordonnée d'une etoile sur chaque image et donc de retrouver une partie de sa trajectoire

i = 22
ref = 17
u = nuage_points(i, ref)
for coord in u:
    x, y = coord
    plt.plot(x, y, "+b")
plt.show()

# Creer un fichier avec les coordonnees de l'etoile traquee
# f = open("Coordonnées_etoile%d.txt" % i, "w")
# f.write("X" + "\t" + "Y")
# for coord in u:
#     x, y = coord
#     f.write(str(x) + ";" + str(y) + "\n")
# f.close()
"""
