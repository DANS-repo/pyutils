#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
from IPython.core.display import HTML
from IPython.display import display


class RFC4180(object):
    delimiter = ','
    quotechar = '"'
    escapechar = None
    doublequote = True
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_MINIMAL


def link_easy(sid):
    """
    Creates an html link to a dataset page in Easy.

    :param sid: a dataset id

    :return: link to the page for that dataset
    """
    prefix = 'https://easy.dans.knaw.nl/ui/datasets/id/'
    return '<a target="_blank" href="{}{}">{}</a>'.format(prefix, sid, sid)


def link_doi(doi):
    return '<a target="_blank" href="https://doi.org/{}">{}</a>'.format(doi, doi)


def link_fedora_file(sid):
    """
    Creates an html link tag to a file in Fedora.

    :param sid: a file id

    :return: link to the file content
    """
    return '<a href="http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/EASY_FILE/content" target="_blank">{}</a>'\
        .format(sid, sid)


def link_fedora_ds_license(sid):
    # http://easy01.dans.knaw.nl:8080/fedora/objects/easy-dataset:18142/datastreams/DATASET_LICENSE/content
    return '<a href="http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/DATASET_LICENSE/content" target="_blank">{}</a>'\
        .format(sid, sid)


def link(path, caption=None, caption_color=None):
    """
    Display relative links to the file in 'path'.

    :param path: the path to link
    :param caption: caption for links, default None
    :param caption_color: color for caption, default None
    :return: parameter path for chaining
    """
    _blank = ['.html', '.txt', '.json']
    _ccoll = {'.xlsx': 'green', '.html': 'blue', '.json': 'purple', '.csv': 'DarkSlateGray'}
    _ctext = {'.xlsx': 'Excel-bestand', '.html': 'html-pagina', '.json': 'json-file', '.csv': 'csv-bestand'}
    nbv = '<b>link</b>'
    dsv = '<b>directory index</b>'
    abo = '<b>office-space</b>'

    ext = os.path.splitext(path)[1]
    filename = os.path.basename(path)
    if caption is None:
        caption = 'bestand'
        caption = _ctext.get(ext, caption)
        caption += ': ' + filename
    if caption_color is None:
        caption_color = 'grey'
        caption_color = _ccoll.get(ext, caption_color)

    blank = ' target="_blank"' if ext in _blank else ''
    abs_path = os.path.abspath(path)
    abs_dire = os.path.dirname(abs_path)
    rel_path = os.path.join('/ta', os.path.relpath(abs_path, '/office-space/TA'))
    rel_dire = os.path.join('/ta', os.path.relpath(abs_dire, '/office-space/TA'))

    link_nbv = '<a href="{}" title="link to the file"{}>{}</a>'.format(rel_path, blank, path)
    link_jup = '<a href="{}" title="link from JupyterLab">&#8865;</a>'.format(path)
    link_abs = '<span title="the directory on office-space containing the file">{}</span>'.format(abs_path)
    link_dir = '<a href="{}" title="link to directory containing the file" target="_blank">{}</a>'.format(rel_dire,
                                                                                                          rel_dire)

    table = """
    <table>
    <caption style="text-align: left"><h3 style="color: {};">{}&nbsp;{}</h3></caption>
    <tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>  </td></tr>
    <tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>  </td></tr>
    <tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>  </td></tr>
    </table>
    """.format(caption_color, link_jup, caption, nbv, link_nbv, dsv, link_dir, abo, link_abs)

    display(HTML(table))
    return path
