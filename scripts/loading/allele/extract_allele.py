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
            allele1 = alleles[0].strip()
            allele2 = alleles[1].strip()
            
            if float(sga_score) < 0.16 or float(pvalue) >= 0.05:
                continue
            
            if allele1 in allele_to_skip:
                allele1 = None
            if allele2 in allele_to_skip:
                allele2 = None
            if allele1 is None and allele2 is None:
                continue

            if allele1 is not None:
                if allele1.upper() == gene.upper() or allele1.upper() == gene2.upper():
                    allele1 = None
                elif not allele1.upper().startswith(gene.upper()) and not allele1.upper().startswith(gene2.upper()):
                    allele1 = None
                    
            if allele2 is not None:
                if allele2.upper() == gene.upper() or allele2.upper() == gene2.upper():
                    allele2 = None
                elif not allele2.upper().startswith(gene.upper()) and not allele2.upper().startswith(gene2.upper()):
                    allele2 = None
                                    
            if allele1 is None or allele2 is None:
            # if allele1 is None and allele2 is None: 
                continue

            pmid = reference_id_to_pmid.get(x.reference_id)

            print (str(allele1) + "\t" + str(allele2) + "\t" + str(x.annotation_id) + "\t" + gene + "/" + orf + "\t" + gene2 + "/" + orf2 + "\t" + str(x.reference_id) + "\t" + str(pmid) + "\t" + str(sga_score) + "\t" + str(pvalue) + "\t" + x.description + "\t" + str(x.date_created).split(' ')[0])
                
nex_session.close()

exit
