#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import csv


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


