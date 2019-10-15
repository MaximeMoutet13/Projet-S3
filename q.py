from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from photutils import DAOStarFinder
from astropy.stats import sigma_clipped_stats
from photutils import datasets
from Truc_finder import *
from scratch import *
from math import *
plt.axis([0,256,0,256])



def dao(i):
     hdul = fits.open('/home/maxime/Documents/Workspace Python/Project_S3/tn%d0.fts' %i)
     hdu = hdul[0].data
     mean, median, std = sigma_clipped_stats(hdu, sigma=3.0)
     daofind = DAOStarFinder(fwhm=10.0, threshold=5.*std)
     sources = daofind(hdu - median)
     for col in sources.colnames:
          sources[col].info.format = '%.8g'  # for consistent table output
     return sources



plt.plot(dao(0)[22][1],dao(0)[22][2])
a = cherche_autour(dao(0)[22], dao(1), 10, 10)
plt.plot(a[1], a[2], "+r")
for i in range(10):
      a = cherche_autour(dao(i+1)[a[0]-1], dao(i + 2), 8, 8)
      plt.plot(a[1], a[2], "+r")


def elippse():
    List = []
    plt.plot(dao(0)[22][1],dao(0)[22][2])
    a = cherche_autour(dao(0)[22], dao(1), 10, 10)
    print(a)
    for i in range(10):
        a = cherche_autour(dao(i+1)[a[0]-1], dao(i + 2), 8, 8)
        List.append([a[1],a[2]])
        print(a)
    return List

if __name__ == '__main__':

    points = elippse()
    a_points = np.array(points)
    x = a_points[:, 0]
    y = a_points[:, 1]
    center, phi, axes = find_ellipse(x, y)
    u = center[0]
    v = center[1]
    a = axes[0]
    b = axes[1]
    t_rot = phi
    t = np.linspace(0, 2 * pi, 100)
    Ell = np.array([a * np.cos(t), b * np.sin(t)])
    # u,v removed to keep the same center location
    R_rot = np.array([[cos(t_rot), -sin(t_rot)], [sin(t_rot), cos(t_rot)]])
    # 2-D rotation matrix
    Ell_rot = np.zeros((2, Ell.shape[1]))
    for i in range(Ell.shape[1]):
        Ell_rot[:, i] = np.dot(R_rot, Ell[:, i])
    plt.plot(u + Ell_rot[0, :], v + Ell_rot[1, :], 'darkblue')  # rotated ellipse
    plt.grid(color='lightgray', linestyle='--')

    plt.show()
