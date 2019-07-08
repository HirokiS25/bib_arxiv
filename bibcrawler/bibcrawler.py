# import urllib.request
import json
import os, logging, time
import asyncio, async_timeout, aiohttp
from bs4 import BeautifulSoup
from argparse import ArgumentParser


URL = 'http://inspirehep.net/search?p='

def json_parser(path):
    with open(path) as input_file:
        json_data = json.load(input_file)
    return json_data


def inspire_url(search_list):
    urls = []
    for pattern, keywords in search_list.items():
        for keyword in keywords:
            url = URL + r'find+' + pattern + r'+' + keyword + r'&of=hx'
            urls.append(url)
    return urls


async def inspire_api(url):
    try:
        async with aiohttp.ClientSession() as session:
            with async_timeout.timeout(10):
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    bibtex = soup.pre.string
    except:
        bibtex = 'no data for {}\n'.format(url)


    return bibtex


def _write_log(input_data, success):
    logging.basicConfig(filename='./bibcrawler.log')
    pass



def output(argv):
    urls = inspire_url(json_parser(argv.input))
    loop = asyncio.get_event_loop()
    wraped = [asyncio.ensure_future(inspire_api(url)) for url in urls]
    results = list(map(loop.run_until_complete, wraped))

    with open(argv.output, mode='w') as f:
        for result in results:
            f.writelines(result)

    return

def makeBibliography(argv):
    time_stump = os.stat(argv.input).st_mtime
    if argv.watch == False:
        output(argv)
    else:
        print('{} watching..'.format(argv.input))
        try:
            while True:
                # print(argv.input)
                new_time_stump = os.stat(argv.input).st_mtime
                if time_stump < new_time_stump:
                    print('file is updated')
                    output(argv)
                time.sleep(1)
                time_stump = new_time_stump
        except KeyboardInterrupt:
            print('watching done...')

    return


def test():
    url = 'http://inspirehep.net/search?p=find+eprint+1905.05503&of=hx'
    loop =  asyncio.get_event_loop()
    loop.run_until_complete(inspire_api(url))


if __name__ == '__main__':
    # queries = ['doi', 'eprint', 'journal', 'title']
    # json_data = json_parser()
    # bibtex = inspire_hep_api("eprint", json_data)
    # dirname = os.path.dirname(os.path.abspath("__file__"))
    usage = 'Usage: python bibcrawler.py -i INPUT-FILE -o OUTPUT-FILE [--watch]'
    argparser = ArgumentParser(usage=usage)
    argparser.add_argument('-i', '--input', type=str,
                           help='input file, json format')
    argparser.add_argument('-o', '--output', type=str,
                           help='output file, bib format')
    argparser.add_argument('--watch', action='store_true',
                           help='')

    args = argparser.parse_args()
    # print(args.watch)

    makeBibliography(args)

