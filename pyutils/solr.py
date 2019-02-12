#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import urllib


def search(query, start=0, rows=200):
    """
    Execute a query on the solr search-index.

    :param query: the query to execute
    :param start: first result to return
    :param rows: number of results to return. default: 200

    :return: Pandas.DataFrame with results
    """
    q = urllib.parse.quote(query)
    url = 'http://easy01.dans.knaw.nl:8080/solr/datasets/select?wt=csv&start={}&rows={}&q={}' \
        .format(start, rows, q)
    return pd.read_csv(url)


def search_all(query):
    """
    Execute a query on the solr search-index and return all results.

    :param query: the query to execute

    :return: Pandas.DataFrame with results
    """
    start = 0
    rows = 200
    df = search(query, start, rows)
    df2 = df
    while len(df2) == 200:
        start += 200
        if start % 5000 == 0:
            print('\r', start, end='', flush=True)
        df2 = search(query, start, rows)
        df = pd.concat([df, df2], ignore_index=True)
    print('\r', start + len(df2), 'results', end='', flush=True)
    return df
