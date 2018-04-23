#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import collections
import pandas as pd


def list_extensions(folder=".", ext_filter=lambda ext: True, path_filter=lambda path: True):
    """Walk a directory recursively, count files and total size per extension.
    Optionally filter for specific extensions.
    """
    if not os.path.exists(folder):
        raise FileNotFoundError("Not found: " + folder)

    pd.options.display.float_format = '{:,.2f}'.format
    extensions = collections.defaultdict(list)

    for path, dirs, files in os.walk(folder):
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            if ext_filter(ext) and path_filter(path):
                if not ext in extensions:
                    extensions[ext] = [0, 0]
                extensions[ext][0] += 1
                statinfo = os.stat(os.path.join(path, filename))
                extensions[ext][1] += statinfo.st_size

    df = pd.DataFrame(extensions)
    if len(extensions) > 0:
        df = df.transpose()
        df.columns = ["count", "size"]
        df["Mb"] = df["size"] / 1048576
    return df