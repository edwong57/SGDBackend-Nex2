from pyramid.httpexceptions import HTTPBadRequest, HTTPOk
import json
from src.models import DBSession, Locusdbentity, Dnasequencealignment, \
     Proteinsequencealignment, Sequencevariant, Taxonomy, Goannotation,\
     Proteindomainannotation, Dnasequenceannotation, Proteinsequenceannotation,\
     Contig
from src.curation_helpers import get_curator_session
from scripts.loading.util import strain_order

TAXON = 'TAX:559292'

def get_variant_data(request):

    sgdid = request.matchdict['id'].upper()

    dbentity = DBSession.query(Locusdbentity).filter_by(sgdid=sgdid).one_or_none()

    if dbentity is None:
        return {}

    taxonomy = DBSession.query(Taxonomy).filter_by(taxid=TAXON).one_or_none()
    taxonomy_id = taxonomy.taxonomy_id
    
    data = { 'sgdid': dbentity.sgdid,
             'name': dbentity.display_name,
             'format_name': dbentity.systematic_name,
             'category': dbentity.subclass.lower(),
             'url': dbentity.obj_url + '/overview',
             'href': dbentity.obj_url + '/overview',
             'description': dbentity.headline
    }
    
    locus_id = dbentity.dbentity_id

    dnaseqannot = DBSession.query(Dnasequenceannotation).filter_by(dbentity_id=locus_id, dna_type='GENOMIC', taxonomy_id=taxonomy_id).one_or_none()

    data['strand'] = dnaseqannot.strand
    data['chrom_start'] = dnaseqannot.start_index
    data['chrom_end'] = dnaseqannot.end_index
    data['dna_length'] = len(dnaseqannot.residues)
    
    contig = DBSession.query(Contig).filter_by(contig_id=dnaseqannot.contig_id).one_or_none()

    data['contig_name'] = contig.display_name
    data['contig_href'] = contig.obj_url + '/overview'

    protseqannot = DBSession.query(Proteinsequenceannotation).filter_by(dbentity_id=locus_id, taxonomy_id=taxonomy_id).one_or_none()

    data['protein_length'] = len(protseqannot.residues)

    go_terms = []
    for x in DBSession.query(Goannotation).filter_by(dbentity_id=locus_id).all():
        go_terms.append(x.go.display_name)
    data['go_terms'] = go_terms

    domains = []
    for x in DBSession.query(Proteindomainannotation).filter_by(dbentity_id=locus_id).all():
        row = { "id": x.annotation_id,
                "start": x.start_index,
                "end": x.end_index,
                "sourceName": x.proteindomain.source.display_name,
                "sourceId": x.proteindomain.source_id,
                "name": x.proteindomain.display_name,
                "href": x.proteindomain.obj_url
        }
        domains.append(row)
    data['protein_domains'] = domains,

    # absolute_genetic_start = 3522089??   
    # 'dna_scores': locus['dna_scores'],
    # 'protein_scores': locus['protein_scores'],
    
    strain_to_id = strain_order()
    dna_seqs = []
    snp_seqs = []
    for x in DBSession.query(Dnasequencealignment).filter_by(dna_type='genomic', locus_id=locus_id).all():
        [name, strain] = x.display_name.split('_')
        if strain == 'S288C':
            data['block_sizes'] = x.block_sizes.split(',')
            data['block_starts'] = x.block_starts.split(',')
        row = { "strain_display_name": strain,
                "strain_link": "/strain/" + strain.replace(".", "") + "/overview",
                "strain_id": strain_to_id[strain],
                "sequence": x.aligned_sequence
        }
        dna_seqs.append(row)
        snp_row = { "snp_sequence": x.snp_sequence,
                    "name": strain,
                    "id":  strain_to_id[strain]
        }
        snp_seqs.append(snp_row)
    data['aligned_dna_sequences'] = dna_seqs
    data['snp_seqs'] = snp_seqs
    
    protein_seqs = []
    for x in DBSession.query(Proteinsequencealignment).filter_by(locus_id=locus_id).all():
        [name, strain] = x.display_name.split('_')
        row = { "strain_display_name": strain,
                "strain_link": "/strain/"	+ strain.replace(".", "") + "/overview",
                "strain_id": strain_to_id[strain],
                "sequence": x.aligned_sequence
        }
        protein_seqs.append(row)
    data['aligned_protein_sequences'] = protein_seqs

    variant_dna = []
    variant_protein = []
    for x in DBSession.query(Sequencevariant).filter_by(locus_id=locus_id).all():
        if x.seq_type == 'DNA':
            dna_row = { "start": x.start_index,
                        "end": x.end_index,
                        "score": x.score,
                        "variant_type": x.variant_type }
            if x.variant_type not in ['Insertion', 'Deletion']:
                dna_row['snp_type'] = x.snp_type.capitalize()
            variant_dna.append(dna_row)    
        if x.seq_type == 'protein':
            protein_row = { "start": x.start_index,
                            "end": x.end_index,
                            "score": x.score,
                            "variant_type": x.variant_type }
            if x.variant_type not in ['Insertion', 'Deletion']:
                protein_row['snp_type'] = x.snp_type.capitalize()
            variant_protein.append(protein_row)
    data['variant_data_dna'] = variant_dna
    data['variant_data_protein'] = variant_protein
    
    return data
 
    