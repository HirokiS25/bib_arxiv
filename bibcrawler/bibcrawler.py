import urllib.request
import re, json
import sys
from bs4 import BeautifulSoup

URL = 'http://inspirehep.net/search?p='

def json_parser():
    with open(sys.argv[1]) as input_file:
        json_data = json.load(input_file)

    return json_data

def inspire_hep_api(pattern, search_list):
    """
    -----------------
    args
    -----------------
        pattern: str,
            search parameter using inspire-hep, ex. "eprint", "a", ...
        search_list: dict,
            json list
    """

    bibtex = []
    for word in search_list[pattern]:
        word = word.replace(" ", "+")
        url = URL + 'find' + '+' + pattern + '+' + word + r'&of=hx'
        try:
            dt = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(dt, 'html.parser')
            bibtex.append(soup.pre.string)
        except:
            bibtex.append('no data\n')

    return bibtex



if __name__ == '__main__':
    queries = ['doi', 'eprint', 'journal', 'title']
    json_data = json_parser()
    bibtex = inspire_hep_api("eprint", json_data)

    items = [];
    for query in queries:
        items += inspire_hep_api(query, json_data)


    with open(sys.argv[2], mode='w') as openfile:
        for bibtex in items:
            openfile.writelines(bibtex)
