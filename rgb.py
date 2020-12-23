import os
import numpy as np
from astropy.io import fits
from reproject import reproject_interp
from reproject.mosaicking import find_optimal_celestial_wcs


def make_rgb_cube_fits(files, output_name, hdu_indx=1):
    """
    This function create a RGB data-cube image using 3 channels: Ks, H and J.
    The coordinates are galactic.
    :param files: a list with the respective namefiles [file_ks, file_H, file_J]
    :param output_name: filename of the resulting data-cube
    :param hdu_indx: 1 for the case of VVV images.
    :return:
    """

    hdus = []
    for f in files:
        if not os.path.exists(f):
            raise Exception("File does not exist : " + f)
        hdus.append(fits.open(f)[hdu_indx])

    wcs_opt, shape_out = find_optimal_celestial_wcs(hdus, frame='galactic')
    header = wcs_opt.to_header()

    image_cube = np.zeros((len(files),) + shape_out, dtype=np.float32)
    for i, hdu in enumerate(hdus):
        image_cube[i, :, :] = reproject_interp(hdu, wcs_opt, shape_out=shape_out)[0]

    fits.writeto(output_name, image_cube, header, overwrite=True)
    fits.writeto(output_name.replace('.fits', '_2d.fits'), np.mean(image_cube, axis=0), header, overwrite=True)

