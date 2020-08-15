from src.models import Locusdbentity, Dbentity, Geninteractionannotation, Referencedbentity
from scripts.loading.database_session import get_session

__author__ = 'sweng66'

nex_session = get_session()

locus_id_to_names =  dict([(x.dbentity_id, (x.systematic_name, x.gene_name)) for x in nex_session.query(Locusdbentity).all()])

allele_to_id = dict([(x.display_name.upper(), x.dbentity_id) for x in nex_session.query(Dbentity).filter_by(subclass='ALLELE').all()])

reference_id_to_pmid =  dict([(x.dbentity_id, x.pmid) for x in nex_session.query(Referencedbentity).all()])

all = nex_session.query(Geninteractionannotation).filter(Geninteractionannotation.description.like('%|alleles:%')).filter(Geninteractionannotation.description.like('%[SGA score%')).all()

allele_to_skip = {}
f = open("scripts/loading/allele/data/genInteractionAlleles2NOTload072020.tsv")
for line in f:
    allele_to_skip[line.strip().upper()] = 1
f.close()
    
for x in all:
    (orf, gene) = locus_id_to_names.get(x.dbentity1_id)
    (orf2, gene2) = locus_id_to_names.get(x.dbentity2_id)
    if gene is None:
        gene = orf
    if gene2 is None:
        gene2 = orf2
      
    desc_list = x.description.split('|')
    for desc in desc_list[1:]:
        if desc.startswith('alleles: '):
            pieces = desc.replace("alleles: ", "").split('[SGA score = ')
            alleles = pieces[0].split(' - ')
            scores = pieces[1].replace("]", "").replace(" P-value = ", "").split(',')
            sga_score = scores[0]
            pvalue = scores[1]
            if float(sga_score) < 0.16 or float(pvalue) >= 0.05:
                continue
            if alleles[0] in allele_to_skip or alleles[1] in allele_to_skip:
                continue
            if alleles[0] in [orf.upper(), gene.upper(), orf2.upper(), gene2.upper()] and alleles[1] in [orf.upper(), gene.upper(), orf2.upper(), gene2.upper()]:
                continue

            pmid = reference_id_to_pmid.get(x.reference_id)

            print (alleles[0] + "\t" + alleles[1]+ "\t" + str(x.annotation_id) + "\t" + gene + "/" + orf + "\t" + gene2 + "/" + orf2 + "\t" + str(x.reference_id) + "\t" + str(pmid) + "\t" + str(sga_score) + "\t" + str(pvalue) + "\t" + x.description + "\t" + str(x.date_created).split(' ')[0])
                
nex_session.close()

exit
