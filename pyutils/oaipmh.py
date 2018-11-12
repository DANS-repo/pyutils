import requests
import xml.etree.ElementTree as ET

NS_OAI = {"oai": "http://www.openarchives.org/OAI/2.0/"}


def id_generator(set_name=None):
    """
    Generate identifiers from an OAI-PMH endpoint.

    https://easy.dans.knaw.nl/oai/?verb=ListIdentifiers&metadataPrefix=oai_dc or
    https://easy.dans.knaw.nl/oai/?verb=ListIdentifiers&metadataPrefix=oai_dc&set=D30000:D37000
    """
    url = 'https://easy.dans.knaw.nl/oai/?verb=ListIdentifiers&metadataPrefix=oai_datacite'
    if set_name:
        url += ('&set=' + set_name)
    print(url)
    response = requests.get(url)
    text = str(response.content, 'utf-8', errors='replace')
    # print(text)
    root = ET.fromstring(text)
    ids = root.find('oai:ListIdentifiers', NS_OAI)
    count = 0
    resumption_token = None
    for child in list(ids):
        if child.tag == '{http://www.openarchives.org/OAI/2.0/}header':
            yield child.find('{http://www.openarchives.org/OAI/2.0/}identifier').text[22:]
            count += 1
        if child.tag == '{http://www.openarchives.org/OAI/2.0/}resumptionToken':
            resumption_token = child.text
    # print('\r', count, resumption_token, end='', flush=True)

    while resumption_token:
        result = requests.get('https://easy.dans.knaw.nl/oai/?verb=ListIdentifiers&resumptionToken=' + resumption_token)
        resumption_token = None
        root = ET.fromstring(result.text)
        ids = root.find('oai:ListIdentifiers', NS_OAI)
        for child in list(ids):
            if child.tag == '{http://www.openarchives.org/OAI/2.0/}header':
                yield child.find('{http://www.openarchives.org/OAI/2.0/}identifier').text[22:]
                count += 1
            if child.tag == '{http://www.openarchives.org/OAI/2.0/}resumptionToken':
                resumption_token = child.text

        # print('\r', count, resumption_token, end='', flush=True)
    print('total ids generated:', count)


def id_donkey(worker, maxid=10, set_name=None):
    """
    Walks the id_generator and sets the worker to work on count and dsid.

    :param worker: a method that accepts count and dsid
    :param maxid: max ids to work. negative for no max
    :param set_name: the name of the set to walk, i.e. 'D30000:D37000' for set archeology. Default: None
    """
    count = 0

    for dsid in id_generator(set_name):
        count += 1
        worker(count, dsid)
        if count >= maxid and not maxid < 0:
            break
