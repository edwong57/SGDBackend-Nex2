from elasticsearch import Elasticsearch
from es7_mapping import mapping
import os
import requests
import json

INDEX_NAME = os.environ.get("ES_VARIANT_INDEX_NAME", "variant_data_index")
DOC_TYPE = "searchable_item"
ES_URI = os.environ["WRITE_ES_URI"]
es = Elasticsearch(ES_URI, retry_on_timeout=True)

def delete_mapping():
    print("Deleting mapping...")
    response = requests.delete(ES_URI + INDEX_NAME + "/")
    if response.status_code != 200:
        print(("ERROR: " + str(response.json())))
    else:
        print("SUCCESS")

def put_mapping():
    print("Putting mapping... ")
    try:
        response = requests.put(ES_URI + INDEX_NAME + "/", json=mapping)
        if response.status_code != 200:
            print(("ERROR: " + str(response.json())))
        else:
            print("SUCCESS")
    except Exception as e:
        print(e)

def cleanup():
    delete_mapping()
    put_mapping()

def setup():
    # see if index exists, if not create it
    indices = list(es.indices.get_alias().keys())
    index_exists = INDEX_NAME in indices
    if not index_exists:
        put_mapping()
        
def index_variant_data():
    variant_url = "https://www.yeastgenome.org/backend/get_all_variant_objects"
    variant_response = requests.get(variant_url).json()
    loci = variant_response['loci']
    bulk_data = []
    print(("Indexing " + str(len(loci)) + " variants"))
    for x in loci:
        obj = { "category": 'variant',
                "sgdid": x['sgdid'],
                "name": x['name'],
                "href": x['href'],
                "absolute_genetic_start": x['absolute_genetic_start'],
                "format_name": x['format_name'],
                "dna_scores": x['dna_scores'],
                "protein_scores": x['protein_scores'],
                "snp_seqs": x['snp_seqs'] }
        
        bulk_data.append({
                "index": {
                    "_index": INDEX_NAME,
                    "_id": "variant_" + x['format_name']
                }
            })
        
        bulk_data.append(obj)            
        if len(bulk_data) == 300:
                es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)
                bulk_data = []
                
    if len(bulk_data) > 0:
        es.bulk(index=INDEX_NAME, body=bulk_data, refresh=True)

        
if __name__ == "__main__":

    cleanup()
    setup()

    index_variant_data()
        
