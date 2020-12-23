from astropy.table import Table
from apolo.data import dirconfig
from os import path
import glob
import utils
import rgb
import aplpy
import wrapper

# Data directories
data_dir = path.join(dirconfig.base_data_path, '..', 'jupiter_results', 'output_4096_v2')
fits_files = glob.glob(data_dir + '/tile_*.fits')
raw_fits_images_dir = 'raw_fits_images'
output_fits_datacubes_dir = 'datacubes'
output_rgb_images_dir = 'rgb_images'
output_plots_dir = 'plots'


# Our selection of groups
selected_groups = Table.read('fina_seleccion.csv', format='csv')

for row in selected_groups:
    fits_file = [s for s in fits_files if f"{row['tile']:04d}" in s]
    table = Table.read(fits_file[0])

    raw_images = [path.join(raw_fits_images_dir, im_name) for im_name in row['image_Ks', 'image_H', 'image_J']]
    cube_filename = path.join(output_fits_datacubes_dir, row['id'] + '.fits')
    rgb.make_rgb_cube_fits(raw_images, cube_filename)
    rgb_image_filename = path.join(output_rgb_images_dir, row['id'] + '.png')
    aplpy.make_rgb_image(cube_filename, rgb_image_filename, stretch_r='sqrt', stretch_g='sqrt', stretch_b='sqrt')

    fig, axis = utils.make_space_params_plot(table, row['group'])
    output_plot_filename = path.join(output_plots_dir, row['id'] + '.pdf')
    wrapper.add_rgb_image(cube_filename, rgb_image_filename, fig, table, row['group'], output_plot_filename)
