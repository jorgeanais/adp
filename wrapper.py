import aplpy


def add_rgb_image(cube_filename, rgb_image_filename, fig, table, group, output):
    gc = aplpy.FITSFigure(cube_filename.replace('.fits', '_2d.fits'), figure=fig, subplot=(2, 3, 6))
    gc.show_rgb(rgb_image_filename)

    group_sources = table[table['label'] == group]
    gc.show_circles(group_sources['l'], group_sources['b'], 1.2 / 3600., layer='marker_sel_sources', color='red', lw=1, alpha=0.8)

    #gc.tick_labels.set_font(size='xx-large')
    #gc.axis_labels.set_font(size='xx-large')
    #gc.ticks.set_linewidth(2)
    gc.tick_labels.set_yformat('d.dd')
    gc.tick_labels.set_xformat('d.dd')
    #gc.set_title('NAME', fontsize='xx-large')
    gc.save(output, adjust_bbox=False)
