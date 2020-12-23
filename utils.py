import matplotlib.pyplot as plt
import numpy as np


def make_space_params_plot(table, group, outdir='/home/jorge/',
                           filter_q=True, filter_z=False, filter_prob=True):
    # Separating sources
    field_sources = table[table['label'] != group]
    group_sources = table[table['label'] == group]

    # Compute color errors
    group_sources['eJ-Ks'] = np.sqrt(np.power(group_sources['eJ'], 2.) +
                                     np.power(group_sources['eKs'], 2.))
    group_sources['eH-Ks'] = np.sqrt(np.power(group_sources['eH'], 2.) +
                                     np.power(group_sources['eKs'], 2.))
    group_sources['eJ-H'] = np.sqrt(np.power(group_sources['eJ'], 2.) +
                                    np.power(group_sources['eH'], 2.))
    group_sources['eQ'] = np.sqrt(np.power(1.0 * group_sources['eJ'], 2.) +
                                  np.power(2.8 * group_sources['eH'], 2.) +
                                  np.power(1.8 * group_sources['eKs'], 2.))

    # Add colors to the table
    # q_match = [True if (-0.2 <= q <= 0.2) else False for q in highlighted_sources['Q']]
    # match = (-0.2 <= highlighted_sources['Q']) * (highlighted_sources['Q'] <= 0.2)
    # nomatch = [not elem for elem in match]

    # filter sources that match
    match = [True] * len(group_sources)
    if filter_q:
        match *= (group_sources['Q'] < 0.2) * (group_sources['Q'] > -0.2)
    if filter_z:
        group_sources['Z-J'] = group_sources['mag_Z'] - group_sources['mag_J']
        match_zj = group_sources['Z-J'] > 3
        match *= match_zj.tolist()
    if filter_prob:
        match *= group_sources['probabilities'] > 0.9

    no_match = [not elem for elem in match]

    # Plot parameters
    kargs_field = dict(c='#7f7f7f', s=40, linewidth=0, alpha=0.2, marker='.')  # dimgrey
    kargs_highlighted_nomatch = dict(facecolors='none', edgecolors='#1f77b4', alpha=0.6, s=20)  # crimson
    kargs_highlighted_match = dict(c='#1f77b4', linewidth=0, alpha=0.60, marker='o')
    kargs_errorbars = dict(color='#1f77b4', fmt='.', ms=1, alpha=0.20)

    fig, axis = plt.subplots(2, 3)
    fig.set_size_inches(w=15, h=10)

    # Subplot assignment
    spd_ax = axis[0, 0]
    ccd_ax = axis[0, 1]
    cmd_ax = axis[0, 2]
    qmd_ax = axis[1, 0]
    pmd_ax = axis[1, 1]

    # Spatial plot -------------------------------------------------------
    spd_ax.scatter(field_sources['l'], field_sources['b'], **kargs_field)
    spd_ax.scatter(group_sources['l'][match], group_sources['b'][match], **kargs_highlighted_match)
    spd_ax.scatter(group_sources['l'][no_match], group_sources['b'][no_match], **kargs_highlighted_nomatch)
    spd_ax.set_xlabel(r'$l$, deg')
    spd_ax.set_ylabel(r'$b$, deg')
    lmin, lmax = spd_ax.get_xlim()
    spd_ax.set_xlim(lmax, lmin)
    spd_ax.ticklabel_format(useOffset=False, style='plain')
    spd_ax.xaxis.set_major_locator(plt.MaxNLocator(4))
    spd_ax.set_aspect('equal')

    # Color-Color plot (J - H) vs (H - Ks) ---------------------------------------------
    ccd_ax.scatter(field_sources['H-Ks'], field_sources['J-H'], **kargs_field)
    ccd_ax.scatter(group_sources['H-Ks'][no_match], group_sources['J-H'][no_match], **kargs_highlighted_nomatch)
    ccd_ax.errorbar(group_sources['H-Ks'], group_sources['J-H'],
                    xerr=group_sources['eH-Ks'], yerr=group_sources['eJ-H'],
                    **kargs_errorbars)
    ccd_ax.scatter(group_sources['H-Ks'][match], group_sources['J-H'][match], **kargs_highlighted_match)
    ccd_ax.set_xlabel(r'$(H - K_s)$, mag')
    ccd_ax.set_ylabel(r'$(J - H)$, mag')
    ccd_ax.set_xlim(-0.5, 2.5)
    ccd_ax.set_ylim(0.3, 4.5)

    # Color-Magnitude Plot Ks vs (J - Ks) ----------------------------------------------
    cmd_ax.scatter(field_sources['J-Ks'], field_sources['mag_Ks'], **kargs_field)
    cmd_ax.scatter(group_sources['J-Ks'][no_match], group_sources['mag_Ks'][no_match], **kargs_highlighted_nomatch)
    cmd_ax.scatter(group_sources['J-Ks'][match], group_sources['mag_Ks'][match], **kargs_highlighted_match)
    cmd_ax.errorbar(group_sources['J-Ks'], group_sources['mag_Ks'],
                    xerr=group_sources['eJ-Ks'], yerr=group_sources['eKs'],
                    **kargs_errorbars)
    cmd_ax.set_xlabel(r'$J - K_S$, mag')
    cmd_ax.set_ylabel(r'$K_s$, mag')
    ymin, ymax = cmd_ax.get_ylim()
    cmd_ax.set_ylim(ymax, ymin)
    cmd_ax.set_xlim(0.0, 7.0)
    cmd_ax.set_ylim(17.5, 8.5)

    # PseudoColor-Magnidue Ks vs Q -----------------------------------------------------
    qmd_ax.axvline(x=-0.2, c='#2ca02c', alpha=0.3)  # turquoise
    qmd_ax.axvline(x=0.2, c='#2ca02c', alpha=0.3)
    qmd_ax.axvspan(-0.2, 0.2, alpha=0.05, color='#2ca02c')
    qmd_ax.scatter(field_sources['Q'], field_sources['mag_Ks'], **kargs_field)
    qmd_ax.scatter(group_sources['Q'][no_match], group_sources['mag_Ks'][no_match], **kargs_highlighted_nomatch)
    qmd_ax.scatter(group_sources['Q'][match], group_sources['mag_Ks'][match], **kargs_highlighted_match)
    qmd_ax.errorbar(group_sources['Q'], group_sources['mag_Ks'],
                    xerr=group_sources['eQ'], yerr=group_sources['eKs'],
                    **kargs_errorbars)
    qmd_ax.set_xlabel(r'$Q=(J-H)-1.8(H-K_s)$, mag')
    qmd_ax.set_ylabel(r'$K_S$')
    ymin, ymax = qmd_ax.get_ylim()
    qmd_ax.set_ylim(ymax, ymin)
    qmd_ax.set_xlim(-1.05, 1.05)
    qmd_ax.set_ylim(17.5, 8)

    # Proper Motions -----------------------------------------------------
    pmd_ax.scatter(field_sources['pmra'], field_sources['pmdec'], **kargs_field)
    pmd_ax.scatter(group_sources['pmra'][no_match], group_sources['pmdec'][no_match], **kargs_highlighted_nomatch)
    pmd_ax.scatter(group_sources['pmra'][match], group_sources['pmdec'][match], **kargs_highlighted_match)
    pmd_ax.errorbar(group_sources['pmra'], group_sources['pmdec'],
                    xerr=group_sources['epmra'], yerr=group_sources['epmdec'],
                    **kargs_errorbars)
    pmd_ax.set_xlabel(r'$\mu_{\alpha*}$, mas/yr')
    pmd_ax.set_ylabel(r'$\mu_\delta$, mas/yr')
    pmd_ax.set_xlim(-10, 2)
    pmd_ax.set_ylim(-10, 2)

    # ??? ----------------------------------------------------------------
    # axis[1, 2].set_xlabel('')
    # axis[1, 2].set_ylabel('')
    axis[1, 2].set_axis_off()

    plt.tight_layout()
    # fig_filename = path.join(outdir, table.meta['TILENAME'] + '_' + str(group) + '.pdf')
    # plt.savefig(fig_filename, overwrite=True)
    return fig, axis
