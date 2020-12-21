import json, os

dirname = os.path.dirname(__file__)
filePath = dirname + '/src/bib_sample.bib'

foo = dict(cls='article', title='foo')

with open(filePath) as b:
    bib = b.readlines()


if __name__ == '__main__':
    print(bib[1])
    print(foo)