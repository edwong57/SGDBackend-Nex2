from datetime import datetime
import os
import sys
from src.models import Source, Locusdbentity, Taxonomy, Proteindomain, Proteindomainannotation
from scripts.loading.database_session import get_session

__author__ = 'sweng66'

CREATED_BY = os.environ['DEFAULT_USER']

domain_file = 'scripts/loading/NISS/data/NISSpilotSet102119_protein_iprscan.tsv'
log_file = 'scripts/loading/NISS/logs/proteindomainannotation.log'

taxid = "TAX:4932"

def load_domain_annotations():

    nex_session = get_session()

    fw = open(log_file, "w")
    
    read_data_and_update_database(nex_session, fw)

    nex_session.close()

    fw.close()

def read_data_and_update_database(nex_session, fw):

    ipr = nex_session.query(Source).filter_by(format_name='InterPro').one_or_none()
    taxon = nex_session.query(Taxonomy).filter_by(taxid=taxid).one_or_none() 
    name_to_dbentity_id = dict([(x.systematic_name, x.dbentity_id) for x in nex_session.query(Locusdbentity).all()])
    format_name_to_id =  dict([(x.format_name, x.proteindomain_id) for x in nex_session.query(Proteindomain).all()])
    
    source_id = ipr.source_id
    taxonomy_id = taxon.taxonomy_id

    key_to_annotation = {}
    for x in nex_session.query(Proteindomainannotation).all():
        key = (x.dbentity_id, x.proteindomain_id, x.start_index, x.end_index)
        key_to_annotation[key] = x

    f = open(domain_file)

    i = 0
    found = {}
    for line in f:
        items = line.strip().split("\t")
        name = items[0].split('_')[0]
        dbentity_id = name_to_dbentity_id.get(name)
        if dbentity_id is None:
            print("The systematic_name ", name, " is not in the LOCUSDBENTITY table.")
            continue
        domain_name = items[4].replace(' ', '_')
        proteindomain_id = format_name_to_id.get(domain_name)
        if proteindomain_id is None:
            print("The domain name:", domain_name, " is not in the PROTEINDOMAIN table.")
            continue
        start = int(items[6])
        end = int(items[7])
        run_time = items[10].split('-')
        run_date = run_time[2] + '-' + run_time[1] + '-' + run_time[0]
        key = (dbentity_id, proteindomain_id, start, end)
        if key not in key_to_annotation and key not in found:
            i = i + 1
            insert_annotation(nex_session, fw, dbentity_id, proteindomain_id,
                              source_id, taxonomy_id, start, end, run_date)
            nex_session.commit()
            found[key] = 1
           
    f.close()
    
    nex_session.commit()

def insert_annotation(nex_session, fw, dbentity_id, proteindomain_id, source_id, taxonomy_id, start, end, run_date):

    x = Proteindomainannotation(dbentity_id = dbentity_id,
                                taxonomy_id = taxonomy_id,
                                source_id = source_id,
                                proteindomain_id = proteindomain_id,
                                start_index = start, 
                                end_index = end,
                                date_of_run = run_date,
                                created_by = CREATED_BY)

    nex_session.add(x)

    fw.write("Insert new annotation for dbentity_id=" + str(dbentity_id) + ", proteindomain_id=" + str(proteindomain_id) + ", start_index=" + str(start) + ", end_index=" + str(end) + "\n")

    
if __name__ == "__main__":
        
    load_domain_annotations()


    
        
