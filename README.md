# SGDBackend-Nex2

[![Build Status](https://travis-ci.org/yeastgenome/SGDBackend-Nex2.svg)](https://travis-ci.org/yeastgenome/SGDBackend-Nex2) [![Coverage Status](https://coveralls.io/repos/github/yeastgenome/SGDBackend-Nex2/badge.svg?branch=qa)](https://coveralls.io/github/yeastgenome/SGDBackend-Nex2?branch=qa)

A restful web service for the Saccharomyces Genome Database (SGD) NEX 2, as well as an authenticated curation interface.

SGD API documentation can be found at https://github.com/yeastgenome/SGDBackend-Nex2/blob/master/docs/webservice.MD.

## Setup

Prerequisites: node.js 6.0.0+ and Python 2.7.x.  To simplify Python setup, virtualenv is highly suggested.

Make sure you have the needed environmental variables configured in dev_variables.sh, then

    $ make build

## Run Locally

    $ make run

## Run Tests

Be sure to have a test_variables.sh file to configure test environemntal variables.

    $ make tests

This command runs both the JavaScript tests as well as the Python tests.  To run just the JavaScript tests

    $ npm test

Or the python tests

    $ source test_variables.sh && nosetests -s

### Varnish Cache and Rebuilding the cache

Caching uses [varnish](https://varnish-cache.org/).  To rebuild the cache, run

    $ source /data/envs/sgd/bin/activate && source prod_variables.sh && python src/loading/scrapy/pages/spiders/pages_spider.py

using environmental variable `CACHE_URLS`, a comma-sepratated list of varshish host URLs (or a single one) such as `http://locahost:5000`.
