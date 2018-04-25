#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import collections
import hashlib
import pandas as pd
from functools import partial


def list_extensions(folder='.', ext_filter=lambda ext: True, path_filter=lambda path: True):
    """
    Walk a directory recursively, count files and total size per extension.
    Optionally filter for file extension and/or path.

    :param folder: the folder to search
    :param ext_filter: lambda that works with file extension (optional)
    :param path_filter: lambda that works with path (optional)

    :return: a dataframe listing the found file extensions, count, size (in bytes and Mb)
    """
    if not os.path.exists(folder):
        raise FileNotFoundError('Not found: ' + folder)
    pd.options.display.float_format = '{:,.2f}'.format
    extensions = collections.defaultdict(list)

    for path, dirs, files in os.walk(folder):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext_filter(ext) and path_filter(path) and not filename.startswith('.'):
                if not ext in extensions:
                    extensions[ext] = [0, 0]
                extensions[ext][0] += 1
                statinfo = os.stat(os.path.join(path, filename))
                extensions[ext][1] += statinfo.st_size

    df = pd.DataFrame(extensions)
    if len(extensions) > 0:
        df = df.transpose()
        df.columns = ['count', 'size']
        df['Mb'] = df['size'] / 1048576
    return df


def find_files(folder='.', ext_filter=lambda ext: True, path_filter=lambda path: True, exclude_hidden=True):
    """
    Walk a directory recursively and list files.
    Optionally filter for file extension and/or path.

    :param folder: the folder to search
    :param ext_filter: lambda that works with file extension (optional)
    :param path_filter: lambda that works with path (optional)
    :param exclude_hidden: exclude hidden files

    :return: list of paths to found files
    """
    if not os.path.exists(folder):
        raise FileNotFoundError('Not found: ' + folder)
    found_files = []
    for path, dirs, files in os.walk(folder):
        for filename in files:
            if not(exclude_hidden and filename.startswith('.')):
                ext = os.path.splitext(filename)[1].lower()
                if ext_filter(ext) and path_filter(path):
                    found_files.append(os.path.join(path, filename))

    return found_files


def sha1_for_file(filename, block_size=2**14):
    """Compute SHA1 digest for a file

    Optional block_size parameter controls memory used to do MD5 calculation.
    This should be a multiple of 128 bytes.
    """
    with open(filename, mode='rb') as f:
        d = hashlib.sha1()
        for buf in iter(partial(f.read, block_size), b''):
            d.update(buf)
    return d.hexdigest()


def display(filename, lines=10, line_number=False):
    count = 0
    with open(filename, 'r') as f:
        for line in f:
            count += 1
            if line_number:
                print(count, line, end='')
            else:
                print(line, end='')
            if count >= lines:
                break