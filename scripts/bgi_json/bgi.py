from src.models import DBSession, Base, Colleague, ColleagueLocus, Dbentity, Locusdbentity, LocusUrl, LocusAlias, Dnasequenceannotation, So, Locussummary, Phenotypeannotation, PhenotypeannotationCond, Phenotype, Goannotation, Go, Goslimannotation, Goslim, Apo, Straindbentity, Strainsummary, Reservedname, GoAlias, Goannotation, Referencedbentity, Referencedocument, Referenceauthor, ReferenceAlias, Chebi
from sqlalchemy import create_engine, and_
import os
import json
import re
import time
import sys

engine = create_engine(os.environ['NEX2_URI'], pool_recycle=3600)
DBSession.configure(bind=engine)
Base.metadata.bind = engine

# populate text file with sgdis to be used to retrieve panther data
def get_sgdids_for_panther():
    new_data = Locusdbentity.get_s288c_genes()
    temp = []
    for loc in new_data:
        temp.append(loc.sgdid)
    result = json.dumps(temp, ensure_ascii=False)
    with open('./scripts/bgi_json/data_dump/sgd_ids_for_panther.txt',
              'w+') as res_file:
        res_file.write(
            result.replace('"', '').replace('[', '').replace(']', ''))


# pair pantherIds with corresponding sgdids
def get_panther_sgdids():
    data_dict = {}
    with open('./scripts/bgi_json/data_dump/panther/panther_search_results.json') as json_data_file:
        json_data = json.load(json_data_file)
        for item in json_data:
            temp_str = ','.join(map(str, item))
            reg_pattern = r'(SGD=S\d+)|(PTHR\d+)'
            reg_result = sorted(list(set(re.findall(reg_pattern, temp_str))))
            if(len(reg_result) > 1):
                item_str1 = ''.join(reg_result[0])
                item_str2 = ''.join(reg_result[1]).split("=")
                data_dict[item_str2[1]] = item_str1
            elif(len(reg_result) == 1):
                item_str1 = ''.join(reg_result[0]).split("=")
                data_dict[item[1]] = None
            else:
                continue

        return data_dict

# pupulate json file with basic gene infromation(bgi)
def get_bgi_data():
    combined_list = combine_panther_locus_list(get_panther_sgdids(), Locusdbentity.get_s288c_genes())
    result = []
    if(len(combined_list) > 0):
        for item_key in combined_list:
            obj = {
                "crossReferenceIds":
                    [],
                "primaryId":
                    "",
                "symbol":
                    "",
                "genomeLocations": [{
                    "startPosition": 0,
                    "chromosome": "",
                    "assembly": "R64-2-1",
                    "endPosition": 0,
                    "strand": ""
                }],
                "soTermId":
                    "",
                "taxonId":
                    "NCBITaxon:559292",
                "synonyms":
                    [],
                "geneLiteratureUrl":
                    "",
                "geneSynopsis":
                    ""
            }
            item = combined_list[item_key]["locus_obj"]
            item_panther = combined_list[item_key]["panther_id"]
            locus_alias_data = DBSession.query(LocusAlias).filter(
                LocusAlias.locus_id == item.dbentity_id).all()

            if(len(locus_alias_data) > 0):
                dna_seq_annotation_obj = DBSession.query(
                    Dnasequenceannotation).filter(
                        Dnasequenceannotation.dbentity_id == item.dbentity_id,
                        Dnasequenceannotation.taxonomy_id == 274901,
                        Dnasequenceannotation.dna_type == "GENOMIC").all()

                if(len(dna_seq_annotation_obj) > 0):
                    chromosome = dna_seq_annotation_obj[0].contig.display_name.split(" ")
                    obj["genomeLocations"][0]["startPosition"] = dna_seq_annotation_obj[0].start_index
                    obj["genomeLocations"][0]["endPosition"] = dna_seq_annotation_obj[0].end_index
                    obj["genomeLocations"][0]["strand"] = dna_seq_annotation_obj[0].strand
                    obj["genomeLocations"][0]["startPosition"] = dna_seq_annotation_obj[0].start_index
                    obj["genomeLocations"][0]["chromosome"] = "chr"+chromosome[1]
                    obj["soTermId"] = dna_seq_annotation_obj[0].so.soid
                mod_locus_alias_data = get_locus_alias_data(locus_alias_data, item.dbentity_id)

                for mod_item in mod_locus_alias_data:
                    mod_value = mod_locus_alias_data.get(mod_item)
                    if (type(mod_value) is list):
                        if (len(mod_locus_alias_data.get("aliases")) == 0):
                            obj["synonyms"].append(item.systematic_name)
                        else:
                            if (mod_locus_alias_data.get("aliases") is not None):
                                obj["synonyms"] = mod_locus_alias_data.get(
                                    "aliases")
                    else:
                        if (mod_value.get("secondaryIds") is not None):
                            temp_sec_item = mod_value.get("secondaryIds")
                            obj["name"] = item.name_description
                            if(len(temp_sec_item) > 1):
                                obj["secondaryIds"] = [','.join([str(x) for x in temp_sec_item])]
                            else:
                                obj["secondaryIds"] = [str(temp_sec_item[0])]
                        if (mod_value.get("crossReferenceIds") is not None):
                            temp_cross_item = mod_value.get("crossReferenceIds")
                            if(len(temp_cross_item) > 1):
                                obj["crossReferenceIds"] = [
                                    ','.join([str(x) for x in temp_cross_item])
                                ]
                            else:
                                obj["crossReferenceIds"] = [str(temp_cross_item[0])]


                if(item_panther is not None):
                    obj["crossReferenceIds"].append("PantherId:" + item_panther)
                    obj["primaryId"] = "SGD:" + item.sgdid
                    item = combined_list[item_key]["locus_obj"]
                    obj["geneSynopsis"] = item.description
                    obj["geneLiteratureUrl"] = "http://www.yeastgenome.org/locus/" + item.sgdid + "/literature"
                    obj["symbol"] = item.systematic_name
                    result.append(obj)

                else:
                    obj["primaryId"] = "SGD:" + item.sgdid
                    item = combined_list[item_key]["locus_obj"]
                    obj["geneSynopsis"] = item.description
                    obj["geneLiteratureUrl"] = "http://www.yeastgenome.org/locus/" + item.sgdid + "/literature"
                    obj["symbol"] = item.systematic_name
                    result.append(obj)
        if(len(result) > 0):
            output_obj = {
                "data": result
            }
            with open('./scripts/bgi_json/data_dump/SGD.1.0.1_basicGeneInformation.json','w+') as res_file:
                res_file.write(json.dumps(output_obj))


# create single gene list containing genes with pantherids and genes without pantherids
def combine_panther_locus_list(panther_list, locus_list):
    combined_list = {}
    if(len(panther_list) > 0 and len(locus_list) > 0):
        for item in locus_list:
            obj = {
                "panther_id": "",
                "locus_obj": ""
            }
            if(panther_list.get(item.sgdid) is not None):
                obj["panther_id"] = panther_list.get(item.sgdid)
                obj["locus_obj"] = item
                combined_list[item.dbentity_id] = obj
            else:
                obj["panther_id"] = None
                obj["locus_obj"] = item
                combined_list[item.dbentity_id] = obj
    return combined_list


# helper method to get locus_alias data
def get_locus_alias_data(locus_alias_list, id):
    data_container = {}
    aliases = []
    aliases_types = ["Uniform", "Non-uniform"]
    for item in locus_alias_list:
        if(item.alias_type in aliases_types):
            aliases.append(item.display_name)

        if(item.alias_type == "SGDID Secondary"):
            obj = {
                "secondaryIds": [],
                "locus_id": id
            }
            obj["secondaryIds"].append(item.source.format_name+":" + item.display_name)
            data_container[item.alias_id] = obj
        else:
            if (item.alias_type == "UniProtKB ID"):
                obj = {"crossReferenceIds": [], "locus_id": id}
                obj["crossReferenceIds"].append("UniProtKB:" + item.display_name)
                data_container[item.alias_id] = obj
            if (item.alias_type == "NCBI protein name"):
                obj = {"crossReferenceIds": [], "locus_id": id}
                obj["crossReferenceIds"].append("NCBI_Gene:" + item.display_name)
                data_container[item.alias_id] = obj

    data_container["aliases"] = aliases
    return data_container

# entry point
if __name__ == '__main__':
    start_time = time.time()
    print "--------------start loading genes--------------"
    get_bgi_data()
    print "--------------done loading genes--------------"
    with open('./scripts/bgi_json/data_dump/log_time.txt', 'w+') as res_file:
        time_taken = "time taken: " + ("--- %s seconds ---" % (time.time() - start_time))
        res_file.write(time_taken)
