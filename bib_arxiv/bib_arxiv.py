import requests, arxiv, sys, json
from bs4 import BeautifulSoup
# import arxiv
import urllib.request


def parse_from_json():
    """
    >>> python bib_arxiv.py '~/path/of/data' 'output/file'
    """
    with open(sys.argv[1]) as input_file:
        # data = input_file.read()
        # print(type(data))
        json_data = json.load(input_file)
        for number in json_data.values():
            arxiv_number = number

    return arxiv_number


def create_bibtex(arxiv_number_list):
    with open(sys.argv[2], mode='w') as output_file:
        hep_url = url_tracer(arxiv_number_list)
        print(hep_url)
        bibtex = [bibtex_data(hep_url[i]) for i in range(len(arxiv_number_list))]
        output_file.writelines(bibtex)



def scrape(url, **attrs):
    res = urllib.request.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser')
    attrs = soup.find_all(**attrs)
    links = []
    for a in attrs:
        links = [aa.attrs['href'] for aa in a.find_all('a')]

    return links



def url_tracer(arxiv_number):
    max_number = len(arxiv_number)
    print(arxiv_number)
    res = arxiv.query(id_list=arxiv_number)
    print(res)
    arxiv_url = [res[i].arxiv_url for i in range(max_number)]
    hep_url = [scrape(arxiv_url[i], class_='extra-ref-cite')[0] for i in range(max_number)]
    return hep_url


def bibtex_data(url):
    # 'Reference', 'BibTeX', 'LaTeX(US)', 'LaTeX(EU)', 'Harvmac', 'EndNote', 'ADS Abstract Service'
    links = scrape(url, class_='tight_list')
    bibtex_url = links[1]
    req = urllib.request.urlopen(bibtex_url)
    soup = BeautifulSoup(req, 'html.parser')
    return soup.pre.string


if __name__ == '__main__':
    number = parse_from_json()
    create_bibtex(number)
