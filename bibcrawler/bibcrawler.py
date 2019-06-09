import urllib.request
import re, json
import sys
from bs4 import BeautifulSoup

URL = 'http://inspirehep.net/search?p='

def json_parser():
    with open(sys.argv[1]) as input_file:
        # data = input_file.read()
        # print(type(data))
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
    print(search_list)
    print(search_list[pattern])

    bibtex = []
    for word in search_list[pattern]:
        url = URL + 'find' + '+' + pattern + '+' + word + r'&of=hx'
        try:
            dt = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(dt, 'html.parser')
            bibtex.append(soup.pre.string)
        except:
            bibtex.append('no data')

    return bibtex

    # with open(sys.argv[2], mode='w') as of:
    #     of.writelines(bibtexs)
    # for bibtex in bibtexs:
    #     with open(sys.argv[2], mode='w') as of:
    #         of.writelines(bibtex)


if __name__ == '__main__':
    json_data = json_parser()
    bibtex = inspire_hep_api("eprint", json_data)

    with open(sys.argv[2], mode='w') as of:
        of.writelines(bibtex)
