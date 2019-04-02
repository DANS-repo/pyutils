#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import logging
import os
import datetime
import sys
from io import StringIO
from logging.handlers import RotatingFileHandler

from IPython.core.display import HTML
from IPython.display import display

_log = logging.getLogger(__name__)
__STDOUT_LOG_CHANNEL__ = None
__FILE_LOG_CHANNEL__ = None


def start_logging(level=logging.DEBUG):
    """
    Start logging log messages to stdout.
    :param level: log level
    :return: None
    """
    global __STDOUT_LOG_CHANNEL__
    if __STDOUT_LOG_CHANNEL__ is None:
        __STDOUT_LOG_CHANNEL__ = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        __STDOUT_LOG_CHANNEL__.setFormatter(formatter)
        __STDOUT_LOG_CHANNEL__.setLevel(level)
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(__STDOUT_LOG_CHANNEL__)


def end_logging():
    """
    Stop logging log messages to stdout.
    :return: None
    """
    global __STDOUT_LOG_CHANNEL__
    if __STDOUT_LOG_CHANNEL__ is not None:
        root = logging.getLogger()
        root.removeHandler(__STDOUT_LOG_CHANNEL__)
        __STDOUT_LOG_CHANNEL__ = None


def debug(func, *args, **kwargs):
    """
    Wrapper for functions that want to be logged to stdout. After the function returns, logging is turned of again.
    :param func: the function to call
    :param args: arguments for the function
    :param kwargs: named arguments for the function
    :return: the return value of the function
    """
    start_logging(logging.DEBUG)
    try:
        ret_val = func(*args, **kwargs)
    finally:
        end_logging()
    return ret_val


def info(func, *args, **kwargs):
    """
    Wrapper for functions that want to be logged to stdout. After the function returns, logging is turned of again.
    :param func: the function to call
    :param args: arguments for the function
    :param kwargs: named arguments for the function
    :return: the return value of the function
    """
    start_logging(logging.INFO)
    try:
        ret_val = func(*args, **kwargs)
    finally:
        end_logging()
    return ret_val


class CsvFormatter(logging.Formatter):

    def __init__(self):
        super().__init__()
        self.output = StringIO()
        self.writer = csv.writer(self.output, quoting=csv.QUOTE_ALL)

    def format(self, record):
        time = datetime.datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
        self.writer.writerow([time, record.threadName, record.process, record.levelname, record.filename,
                              record.lineno, record.funcName, record.msg, record.pathname])
        data = self.output.getvalue()
        self.output.truncate(0)
        self.output.seek(0)
        return data.strip()


def start_file_logging(log_file='logs/pyu.log', level=logging.DEBUG, max_bytes=1000 * 1000 * 1024,
                          backup_count=3, encoding='utf-8'):
    """
    Initiate logging to a rotating file. If needed, the log file output can be picked up in a DataFrame:
    ```
    names = ['date', 'thread', 'process', 'level', 'file', 'line', 'function', 'msg', 'path']
    df = pd.read_csv('logs/pyu.log', header=None, quoting=1, converters={0: pd.to_datetime}, names=names)
    ```

    :param log_file: the path or file to write to. Directories will be created.
    :param level: the log level. one of logging levels
                logging.DEBUG (10), logging.INFO (20), logging.WARNING (30), logging.ERROR (40), logging.CRITICAL (50)
    :param max_bytes: max bytes for roll over
    :param backup_count: how many files are kept
    :param encoding: encoding of the file
    :return: None
    """
    global __FILE_LOG_CHANNEL__
    if __FILE_LOG_CHANNEL__ is None:
        path = os.path.dirname(log_file)
        os.makedirs(path, exist_ok=True)
        __FILE_LOG_CHANNEL__ = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count,
                                                   encoding=encoding)
        __FILE_LOG_CHANNEL__.setFormatter(CsvFormatter())
        __FILE_LOG_CHANNEL__.setLevel(level)
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        root.addHandler(__FILE_LOG_CHANNEL__)
        _log.info('Started file logging to {}'.format(__FILE_LOG_CHANNEL__.baseFilename))
    else:
        _log.info('Not initiating file logging. Logging to file already established: {}'
                     .format(__FILE_LOG_CHANNEL__.baseFilename))


def end_file_logging():
    """
    End logging to a rotating file that was started with `initiate_file_logging`.

    :return: None
    """
    global __FILE_LOG_CHANNEL__
    if __FILE_LOG_CHANNEL__ is not None:
        _log.info('End file logging to {}'.format(__FILE_LOG_CHANNEL__.baseFilename))
        root = logging.getLogger()
        root.removeHandler(__FILE_LOG_CHANNEL__)
        __FILE_LOG_CHANNEL__ = None


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


def excel_link_easy(sid):
    formula = '=HYPERLINK("hhttps://easy.dans.knaw.nl/ui/datasets/id/{}", "{}")'.format(sid, sid)
    return formula


def link_doi(doi):
    return '<a target="_blank" href="https://doi.org/{}">{}</a>'.format(doi, doi)


def excel_link_doi(doi):
    formula = '=HYPERLINK("https://doi.org/{}", "{}")'.format(doi, doi)
    return formula


def link_fedora_file(sid):
    """
    Creates an html link tag to a file in Fedora.

    :param sid: a file id

    :return: link to the file content
    """
    return '<a href="http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/EASY_FILE/content" target="_blank">{}</a>'\
        .format(sid, sid)


def excel_fedora_file(sid):
    formula = '=HYPERLINK("http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/EASY_FILE/content", "{}")'.format(
        sid, sid)
    return formula


def link_fedora_file_md(sid):
    """
    Creates a html link tag to the EASY_FILE_METADATA of a file with the given sid.

    http://easy01.dans.knaw.nl:8080/fedora/objects/easy-file:6364865/datastreams/EASY_FILE_METADATA/content

    :param sid:  a file id
    :return: link to the file metadata
    """
    return '<a href="http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/EASY_FILE_METADATA/content" target="_blank">{}</a>'\
        .format(sid, sid)


def excel_fedora_file_md(sid):
    formula = '=HYPERLINK("http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/EASY_FILE_METADATA/content", "{}")'.format(sid, sid)
    return formula


def link_fedora_ds_license(sid):
    # http://easy01.dans.knaw.nl:8080/fedora/objects/easy-dataset:18142/datastreams/DATASET_LICENSE/content
    return '<a href="http://easy01.dans.knaw.nl:8080/fedora/objects/{}/datastreams/DATASET_LICENSE/content" target="_blank">{}</a>'\
        .format(sid, sid)


def format_size(size_in_bytes, leading=8, trailing=1):
    """
    Formats the given integer as an appropriate string with leading spaces.
    :param size_in_bytes:
    :return:
    """
    if size_in_bytes <= 1024:
        trailing = 0
    f = '{:' + str(leading) + '.' + str(trailing) + 'f}'
    if size_in_bytes >= 1024 * 1024 * 1024:
        return (f + ' GB').format(size_in_bytes / 1024 / 1024 / 1024)
    elif size_in_bytes >= 1024 * 1024:
        return (f + ' MB').format(size_in_bytes / 1024 / 1024)
    elif size_in_bytes >= 1024:
        return (f + ' KB').format(size_in_bytes / 1024)
    else:
        return (f + ' B').format(size_in_bytes)


def format_datetime(date):
    return '{0:%Y-%m-%d %H:%M:%S}'.format(date)


def format_timestamp(timestamp):
    return format_datetime(datetime.datetime.fromtimestamp(timestamp))


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
    if os.path.exists(abs_path) and not isdir:
        stats = os.stat(abs_path)
        file_size = format_size(stats.st_size)
    else:
        file_size = ''

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
    row1 = '<tr><td style="text-align: left">{}</td><td style="text-align: left">{}</td><td>{}</td></tr>' \
        .format(nbv, link_nbv, file_size)
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
    """
    Inserts a script that does a callback (on document ready) and displays
    the content of the url /ta/tech/msg/omni_present_message.txt
    :return: None
    """
    script = ('\n'
              '    <div id="omni_present_message">\n'
              '    </div>\n'
              '    <script>\n'
              '    function loadOmniPresentMessage() {\n'
              '      var xhttp = new XMLHttpRequest();\n'
              '      xhttp.onreadystatechange = function() {\n'
              '        if (this.readyState == 4 && this.status == 200) {\n'
              '          document.getElementById("omni_present_message").innerHTML = this.responseText;\n'
              '        } else {\n'
              '          document.getElementById("omni_present_message").hide();\n'
              '        }\n'
              '      };\n'
              '      xhttp.open("GET", "/ta/tech/msg/omni_present_message.txt", true);\n'
              '      xhttp.send();\n'
              '    }\n'
              '    $( document ).ready(loadOmniPresentMessage);\n'
              '    </script>\n'
              '    ')
    display(HTML(script))
