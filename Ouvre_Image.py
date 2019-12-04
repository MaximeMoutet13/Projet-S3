import matplotlib.pyplot as plt
import numpy as np
from astropy.utils.data import get_pkg_data_filename
from astropy.io import fits


# Modifier le lien de l'image pour l'ouvrir
image_file = get_pkg_data_filename("/home/maxime/Documents/Workspace Python/Project_S3/photos/tn10.fts")


def show_image(name):
    image_data = fits.getdata(name, ext=0)
    image_data_flip = np.flipud(image_data)
    plt.figure()
    plt.imshow(image_data_flip)
    plt.colorbar()
    plt.show()


show_image(image_file)


# Affiche le HDU de l'image
fits.info(image_file)

print(repr(fits.getheader(image_file, 0)))




