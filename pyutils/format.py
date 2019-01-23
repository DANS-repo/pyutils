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


import os
from IPython.core.display import HTML


def link(path, caption=None, color=None, extra=None):
    """
    Display relative links to the file in 'path'.

    :param path: the path to link
    :param caption: caption for links, default None
    :param color: color for caption and border, default None
    :param extra: extra text to be inserted before the caption, default None
    :return: parameter path for chaining
    """
    _blank = ['.html', '.txt', '.json', '.csv']
    _ccoll = {'.xlsx': 'green',
              '.html': 'blue',
              '.json': 'purple',
              '.csv': 'DarkSlateGray',
              '.ipynb': 'Chocolate'}
    _ctext = {'.xlsx': 'Excel-bestand',
              '.html': 'html-pagina',
              '.json': 'json-file',
              '.csv': 'csv-bestand',
              '.ipynb': 'notebook'}
    nbv = '<b>link</b>'
    dsv = '<b>directory index</b>'
    abo = '<b>office-space</b>'

    abs_path = os.path.abspath(path)
    ext = os.path.splitext(abs_path)[1]
    isdir = ext == ''
    filename = os.path.basename(abs_path)

    if caption is None:
        if isdir:
            caption = 'directory'
        else:
            caption = 'bestand'
        caption = _ctext.get(ext, caption)
        caption += ': ' + filename
    if color is None:
        color = 'grey'
        color = _ccoll.get(ext, color)

    if extra is not None:
        caption = extra + ' ' + caption

    blank = ' target="_blank"' if ext in _blank else ''

    if isdir:
        abs_dire = abs_path
        nbv_text = os.path.basename(abs_path)
    else:
        abs_dire = os.path.dirname(abs_path)
        rel_path = os.path.join('/ta', os.path.relpath(abs_path, '/office-space/TA'))
        nbv_text = path
    rel_dire = os.path.join('/ta', os.path.relpath(abs_dire, '/office-space/TA'))

    if ext == '.ipynb' or isdir:
        rel_path = path

    link_nbv = '<a href="{}" title="link to the file"{}>{}</a>'.format(rel_path, blank, nbv_text)
    link_jup = '<a href="{}" title="link from JupyterLab">&#8865;</a>'.format(path)
    link_dir = '<a href="{}" title="link to directory containing the file" target="_blank">{}</a>'.format(rel_dire,
                                                                                                          rel_dire)
    link_abs = '<span title="the directory on office-space containing the file">{}</span>'.format(abs_path)

    capt = '<caption style="text-align: left"><h3 style="color: {};">{}&nbsp;{}</h3></caption>' \
        .format(color, link_jup, caption)
    row1 = '<tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>  </td></tr>' \
        .format(nbv, link_nbv)
    row2 = '<tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>  </td></tr>' \
        .format(dsv, link_dir)
    row3 = '<tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>  </td></tr>' \
        .format(abo, link_abs)

    table = '<table style="border: 1px solid {};">{}{}{}{}</table>' \
        .format(color, capt, row1, row2, row3)

    display(HTML(table))
    return path


def toggle_code_cells(initial_show=True):
    """
    Displays a floating button to toggle the visibility of code cells.
    :return: None
    """
    show = 'false' if initial_show else 'true'
    start = '<script>code_show={};'.format(show)
    tags = start + """
        function code_toggle() {
         if (code_show){
             $("div.input").hide();
         } else {
             $("div.input").show();
         }
         code_show = !code_show
        } 
        $( document ).ready(code_toggle);
    </script>
    <style>
        div.floating-bar {
            position:fixed;
            bottom:20px;
            left:20px;
            font-size:90%;
        }
        input.toggle-button {
            color: maron;
            padding: 5px;
            outline: none;
        }
    </style>
    <div class="floating-bar">
    <form action="javascript:code_toggle()">
        <input class="toggle-button" type="submit" value="Toggle code cells">
    </form>
    </div>
    """
    display(HTML(tags))


def messages():
    script = """
    <div id="omni_present_message">
    </div>
    <script>
    function loadOmniPresentMessage() {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("omni_present_message").innerHTML = this.responseText;
        }
      };
      xhttp.open("GET", "/ta/tech/msg/omni_present_message.txt", true);
      xhttp.send();
    }
    $( document ).ready(loadOmniPresentMessage);
    </script>
    """
    display(HTML(script))
