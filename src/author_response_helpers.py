from pyramid.httpexceptions import HTTPBadRequest, HTTPOk
from sqlalchemy.exc import IntegrityError, DataError
import transaction
import json
from src.models import DBSession, Authorresponse, Referencedbentity, Source
from src.curation_helpers import get_curator_session

def insert_author_response(request):

    try:
        sgd = DBSession.query(Source).filter_by(display_name='SGD').one_or_none()
        source_id = sgd.source_id
        created_by = 'OTTO'

        email = request.params.get('email')
        if email == '':
            return HTTPBadRequest(body=json.dumps({'error': "Please enter your email address"}), content_type='text/json')
        pmid = request.params.get('pmid')
        if pmid == '':
            return HTTPBadRequest(body=json.dumps({'error': "Please enter Pubmed ID for your paper"}), content_type='text/json')
        
        pmid = pmid.replace('PMID:', '').replace('Pubmed ID:', '').strip()

        has_novel_research = request.params.get('has_novel_research')
        
        # return HTTPBadRequest(body=json.dumps({'error': "TESTING: has_novel_research=" + has_novel_research}), content_type='text/json')
    
        has_large_scale_data = request.params.get('has_large_scale_data')

        # return HTTPBadRequest(body=json.dumps({'error': "TESTING: has_large_scale_data=" + has_large_scale_data}), content_type='text/json')

        research_results = request.params.get('research_result')
    
        gene_list = request.params.get('gene_list')
     
        dataset_description = request.params.get('dataset_desc')

        other_description = request.params.get('other_desc')

        x = Authorresponse(source_id = source_id,
                           reference_id = reference_id,
                           author_email = email,
                           has_novel_research = has_novel_research,
                           has_large_scale_data = has_large_scale_data,
                           research_results = research_results,
                           gene_list = gene_list,
                           dataset_description = dataset_description,
                           other_description = other_description,
                           created_by = created_by)

        DBSession.add(x)
        transaction.commit()
        return HTTPOk(body=json.dumps({'success': "Your data has been succesfully added into our database.", 'AUTHOR_RESPONSE': "AUTHOR_RESPONSE"}), content_type='text/json')
    except Exception as e:
        transaction.abort()
        return HTTPBadRequest(body=json.dumps({'error': str(e)}), content_type='text/json')


