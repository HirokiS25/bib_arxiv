# bibcrawler

* Improve the process and speed
* New option `--watch`


## install
`python setup.py install`

## use
`python bibcrawler.py -i "path/to/json/data" -o "path/to/output/" [--watch]`

## bugs
The queries 'title' and 'journal' is not recommended
because `inspire-hep` cannot find such queries well.
