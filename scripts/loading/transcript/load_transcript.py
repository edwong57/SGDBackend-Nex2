import logging
import os
from datetime import datetime
import sys
from src.models import Source, Dbentity, Referencedbentity, Transcriptdbentity, TranscriptReference,\
                       Contig, Dnasequenceannotation, So, Taxonomy
from scripts.loading.database_session import get_session

__author__ = 'sweng66'

logging.basicConfig(format='%(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO)

CREATED_BY = os.environ['DEFAULT_USER']

TAXON = "TAX:559292"

file_names = [ "scripts/loading/transcript/data/longest_full-ORF_transcripts_gal.gff3",
	       "scripts/loading/transcript/data/longest_full-ORF_transcripts_ypd.gff3" ]

PMID = 23615609

def load_data():

    nex_session = get_session()

    log.info(str(datetime.now()))
    log.info("Getting data from database...")
    
    source = nex_session.query(Source).filter_by(display_name='SGD').one_or_none()
    source_id = source.source_id
    taxonomy = nex_session.query(Taxonomy).filter_by(taxid=TAXON).one_or_none()
    taxonomy_id = taxonomy.taxonomy_id
    so = nex_session.query(So).filter_by(display_name='primary transcript').one_or_none()
    so_id = so.so_id
    reference = nex_session.query(Referencedbentity).filter_by(pmid=PMID).one_or_none()
    reference_id = reference.dbentity_id
    chr_to_contig = dict([(x.format_name, (x.contig_id, x.residues)) for x in nex_session.query(Contig).filter(Contig.format_name.like('Chromosome_%')).all()])

    count = 0
    
    for file in file_names:
        
        log.info("Loading data from " + file + "...")
        
        f = open(file)
        for line in f:
            if line.startswith('#'):
                continue
            pieces = line.strip().split("\t")
            chr = pieces[0].replace("chr", "Chromosome_")
            (contig_id, chrSeq) = chr_to_contig.get(chr)
            if chr not in chr_to_contig:
                print (chr)
                continue
            
            count = count + 1
            
            (contig_id, chrSeq) = chr_to_contig.get(chr)
            start = int(pieces[3])
            end = int(pieces[4])
            strand = pieces[6]
            transcript = pieces[8].split(";")
            cond_name = transcript[0].split('=')[0]
            cond_value = transcript[0].split('=')[1]
            display_name = transcript[1].split("=")[1]
        
            log.info("adding transcriptdbentiy: " + display_name + "...")

            transcript_id = insert_transcriptdbentity(nex_session, display_name, cond_name, cond_value, source_id)
        
            log.info("adding transcript_reference for transcript_id = " + str(transcript_id) + "...")
            
            insert_transcript_reference(nex_session, transcript_id, reference_id, source_id)

            seq = get_seq_from_chr(chrSeq, start, end, strand)
            file_header = display_name + " " + pieces[0] + ":" + str(start) + ".." + str(end)
            download_filename = display_name + "_" + cond_name + ".fsa"

            log.info("adding dnasequenceannotation for transcript_id = " + str(transcript_id) + "...")
            
            insert_dnasequenceannotation(nex_session, transcript_id, source_id, taxonomy_id, so_id, contig_id, start, end, strand, file_header, download_filename, seq)

            if count >= 300:
                # nex_session.rollback()  
                nex_session.commit()
                count = 0
            
        f.close()
        
        # nex_session.rollback()
        nex_session.commit()
        
    nex_session.close()
    log.info("Done!")
    log.info(str(datetime.now()))
    
def insert_dnasequenceannotation(nex_session, transcript_id, source_id, taxonomy_id, so_id, contig_id, start, end, strand, file_header, download_filename, seq):

    x = Dnasequenceannotation(dbentity_id = transcript_id,
                              source_id = source_id,
                              taxonomy_id = taxonomy_id,
                              so_id = so_id,
                              contig_id = contig_id,
                              dna_type = 'GENOMIC',
                              start_index = start,
                              end_index = end,
                              strand = strand,
                              file_header = file_header,
                              download_filename = download_filename,
                              residues = seq,
                              created_by = CREATED_BY)
    nex_session.add(x)

def get_seq_from_chr(chrSeq, start, end, strand):
    seq = chrSeq[start-1:end]
    if strand == '-':
        seq = reverse_complement(seq)
    return seq

def reverse_complement(seq):

    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    bases = list(seq)
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)
    return bases

def insert_transcript_reference(nex_session, transcript_id, reference_id, source_id):

    x = TranscriptReference(transcript_id = transcript_id,
                            reference_id = reference_id,
                            source_id = source_id,
                            created_by = CREATED_BY)

    nex_session.add(x)

def insert_transcriptdbentity(nex_session, display_name, cond_name, cond_value, source_id):
    
    x = Transcriptdbentity(format_name= display_name + "_" + cond_name,
                           display_name = display_name,
                           source_id = source_id,
                           subclass = 'TRANSCRIPT',
                           dbentity_status = 'Active',
                           created_by = CREATED_BY,
                           condition_name = cond_name,
                           condition_value = cond_value,
                           in_ncbi = '0')
    
    nex_session.add(x)
    nex_session.flush()
    nex_session.refresh(x)
    return x.dbentity_id

if __name__ == "__main__":

    load_data()
