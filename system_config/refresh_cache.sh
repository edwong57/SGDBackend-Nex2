#! /bin/sh

# keep in /home/deploy/bin/refresh_cache.sh

cd /data/www/SGDBackend-NEX2/current
source /data/envs/sgd/bin/activate && source prod_variables.sh && python src/loading/scrapy/pages/spiders/pages_spider.py
