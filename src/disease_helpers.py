from pyramid.httpexceptions import HTTPBadRequest, HTTPForbidden, HTTPOk, HTTPNotFound, HTTPFound
from sqlalchemy.exc import IntegrityError, DataError
import transaction
import json
from src.models import DBSession, Diseaseannotation, Disease, Source, Dbentity, Locusdbentity, Referencedbentity,\
     Straindbentity, Ro, Eco
from src.curation_helpers import get_curator_session



def insert_update_disease_annotations(request):
    try:
        CREATED_BY = request.session['username']
        curator_session = get_curator_session(request.session['username'])
        source_id = 834

        annotation_id = request.params.get('annotation_id')

        dbentity_id = request.params.get('dbentity_id')
        if not dbentity_id:
            return HTTPBadRequest(body=json.dumps({'error': "gene is blank"}), content_type='text/json')

        taxonomy_id = request.params.get('taxonomy_id')
        if not taxonomy_id:
            return HTTPBadRequest(body=json.dumps({'error': "taxonomy is blank"}), content_type='text/json')
        
        reference_id = request.params.get('reference_id')
        if not reference_id:
            return HTTPBadRequest(body=json.dumps({'error': "reference is blank"}), content_type='text/json')

        eco_id = request.params.get('eco_id')
        if not eco_id:
            return HTTPBadRequest(body=json.dumps({'error': "eco is blank"}), content_type='text/json')
        
        # disease_id = request.params.get('disease_id')
        # if not disease_id:
        #     return HTTPBadRequest(body=json.dumps({'error': "disease_id is blank"}), content_type='text/json')
        
        association_type = request.params.get('association_type')
        if not association_type:
            return HTTPBadRequest(body=json.dumps({'error': "association type is blank"}), content_type='text/json')

        annotation_type = request.params.get('annotation_type')
        if not annotation_type:
            return HTTPBadRequest(body=json.dumps({'error': "annotation type is blank"}), content_type='text/json')

        with_ortholog = request.params.get('with_ortholog')
        if not with_ortholog:
            with_ortholog = None

        dbentity_in_db = None
        dbentity_in_db = DBSession.query(Dbentity).filter(or_(Dbentity.sgdid == dbentity_id, Dbentity.format_name == gene_id)).filter(Dbentity.subclass == 'LOCUS').one_or_none()
        if dbentity_in_db is not None:
            dbentity_id = dbentity_in_db.dbentity_id
        else:
            return HTTPBadRequest(body=json.dumps({'error': "gene value not found in database"}), content_type='text/json')

        dbentity_in_db = None
        pmid_in_db = None
        dbentity_in_db = DBSession.query(Dbentity).filter(and_(Dbentity.sgdid == reference_id,Dbentity.subclass == 'REFERENCE')).one_or_none()
        if dbentity_in_db is None:
            try:
                dbentity_in_db = DBSession.query(Dbentity).filter(and_(Dbentity.dbentity_id == int(reference_id), Dbentity.subclass == 'REFERENCE')).one_or_none()
            except ValueError as e:
                pass
        if dbentity_in_db is None:
            try:
                pmid_in_db = DBSession.query(Referencedbentity).filter(Referencedbentity.pmid == int(reference_id)).one_or_none()
            except ValueError as e:
                pass

        if dbentity_in_db is not None:
            reference_id = dbentity_in_db.dbentity_id
        elif (pmid_in_db is not None):
            reference_id = pmid_in_db.dbentity_id
        else:
            return HTTPBadRequest(body=json.dumps({'error': "reference value not found in database"}), content_type='text/json')
        

        isSuccess = False
        returnValue = ''
        reference_in_db = None

        if(int(annotation_id) > 0):
            try:
                update_disease = {'dbentity_id': dbentity_id,
                                    'taxonomy_id': taxonomy_id,
                                    'reference_id': reference_id,
                                    'eco_id': eco_id,
                                    'association_type': association_type,
                                    'annotation_type': annotation_type,
                                    'disease_id': disease_id,
                                    'with_ortholog': with_ortholog
                                    }

                curator_session.query(Diseaseannotation).filter(Diseaseannotation.annotation_id == annotation_id).update(update_disease)
                transaction.commit()
                isSuccess = True
                returnValue = 'Record updated successfully.'

                disease = curator_session.query(Diseaseannotation).filter(Diseaseannotation.annotation_id == annotation_id).one_or_none()
                reference_in_db = {
                    'id': disease.annotation_id,
                    'dbentity_id': {
                        'id': disease.dbentity.format_name,
                        'display_name': disease.dbentity.display_name
                    },
                    'taxonomy_id': '',
                    'reference_id': disease.reference.pmid,
                    'eco_id': '',
                    'association_type': disease.association_type,
                    'annotation_type': disease.annotation_type,
                    'with_ortholog': disease.with_ortholog
                }
                if disease.eco:
                    reference_in_db['eco_id'] = str(disease.eco.eco_id)

                if disease.association_type:
                    reference_in_db['association_type'] = str(disease.association_type)

                if regulation.taxonomy:
                    reference_in_db['taxonomy_id'] = disease.taxonomy.taxonomy_id

            except IntegrityError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Integrity Error: ' + str(e.orig.pgerror)
            except DataError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Data Error: ' + str(e.orig.pgerror)
            except InternalError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                error = str(e.orig).replace('_', ' ')
                error = error[0:error.index('.')]
                returnValue = 'Updated failed, ' + error
            except Exception as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Updated failed, ' + str(e)
            finally:
                if curator_session:
                    curator_session.close()

        
        if(int(annotation_id) == 0):
            try:
                y = None
                y = Diseaseannotation(dbentity_id = dbentity_id,
                                    source_id = source_id,
                                    taxonomy_id = taxonomy_id,
                                    reference_id = reference_id,
                                    eco_id = eco_id,
                                    association_type = association_type,
                                    annotation_type = annotation_type,
                                    with_ortholog = with_ortholog,
                                    created_by = CREATED_BY)
                curator_session.add(y)
                transaction.commit()
                isSuccess = True
                returnValue = 'Record added successfully.'
            except IntegrityError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Integrity Error: ' + str(e.orig.pgerror)
            except DataError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Data Error: ' + str(e.orig.pgerror)
            except Exception as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Insert failed ' +str(e)
            finally:
                if curator_session:
                    curator_session.close()

        if isSuccess:
            return HTTPOk(body=json.dumps({'success': returnValue,'disease':reference_in_db}), content_type='text/json')

        return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

    except Exception as e:
        return HTTPBadRequest(body=json.dumps({'error': str(e)}), content_type='text/json')

def get_diseases_by_filters(request):
    try:
        console.log(request);
        dbentity_id = str(request.params.get('dbentity_id')).strip()
        reference_id = str(request.params.get('reference_id')).strip()

        if not(dbentity_id or reference_id):
            raise Exception("Please provide input for gene, reference or combination to get the regulations.")

        diseases_in_db = DBSession.query(Diseaseannotation)
        
        gene_dbentity_id,reference_dbentity_id = None,None

        if dbentity_id:
            gene_dbentity_id = DBSession.query(Dbentity).filter(or_(Dbentity.sgdid==dbentity_id, Dbentity.format_name==dbentity_id)).one_or_none()

            if not gene_dbentity_id:
                raise Exception('gene not found, please provide sgdid or systematic name')
            else:
                gene_dbentity_id = gene_dbentity_id.dbentity_id
                diseases_in_db = diseases_in_db.filter_by(gene_id=gene_dbentity_id)
        
        if reference_id:
            if reference_id.startswith('S00'):
                reference_dbentity_id = DBSession.query(Dbentity).filter(Dbentity.sgdid == reference_id).one_or_none()
            else:
                reference_dbentity_id = DBSession.query(Referencedbentity).filter(or_(Referencedbentity.pmid == int(reference_id),Referencedbentity.dbentity_id == int(reference_id))).one_or_none()
            
            if not reference_dbentity_id:
                raise Exception('Reference not found, please provide sgdid , pubmed id or reference number')
            else:
                reference_dbentity_id = reference_dbentity_id.dbentity_id
                regulations_in_db = regulations_in_db.filter_by(reference_id=reference_dbentity_id)
        
        diseases = diseases_in_db.options(joinedload(Diseaseannotation.eco), joinedload(Diseaseannotation.do), joinedload(Diseaseannotation.taxonomy)
                                                , joinedload(Diseaseannotation.reference), joinedload(Diseaseannotation.dbentity)).order_by(Diseaseannotation.annotation_id.asc()).all()
        console.log(diseases);
        list_of_diseases = []
        for disease in diseases:
            currentDisease = {
                'id': disease.annotation_id,
                'gene_id': {
                    'id': disease.dbentity.format_name,
                    'display_name': disease.dbentity.display_name
                },
                'taxonomy_id': '',
                'reference_id': disease.reference.pmid,
                'eco_id': '',
                'association_type': disease.association_type,
                'annotation_type': disease.annotation_type,
                'disease_id': disease.disease_id,
                'with_ortholog': ''
            }

            if disease.eco:
                currentDisease['eco_id'] = str(disease.eco.eco_id)

            if disease.do:
                currentDisease['disease_id'] = str(disease.do.do_id)

            if diseaes.taxonomy:
                currentDisease['taxonomy_id'] = disease.taxonomy.taxonomy_id

            list_of_diseases.append(currentDisease)
        
        return HTTPOk(body=json.dumps({'success': list_of_diseases}), content_type='text/json')
    except Exception as e:
        return HTTPBadRequest(body=json.dumps({'error': e.message}), content_type='text/json')

def delete_disease_annotation(request):
    try:
        id = request.matchdict['id']
        curator_session = get_curator_session(request.session['username'])
        isSuccess = False
        returnValue = ''
        disease_in_db = curator_session.query(Diseaseannotation).filter(Diseaseannotation.annotation_id == id).one_or_none()
        if(disease_in_db):
            try:
                curator_session.delete(disease_in_db)
                transaction.commit()
                isSuccess = True
                returnValue = 'Diseaseannot successfully deleted.'
            except Exception as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Error occurred deleting diseaseannot: ' + str(e.message)
            finally:
                if curator_session:
                    curator_session.close()

            if isSuccess:
                return HTTPOk(body=json.dumps({'success': returnValue}), content_type='text/json')

            return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

        return HTTPBadRequest(body=json.dumps({'error': 'diseaseannot not found in database.'}), content_type='text/json')

    except Exception as e:
        return HTTPBadRequest(body=json.dumps({'error': str(e.message)}), content_type='text/json')


def upload_disease_file(request):

    try:
        file = request.POST['file'].file
        filename = request.POST['file'].filename
        CREATED_BY = request.session['username']
        xl = pd.ExcelFile(file)
        list_of_sheets = xl.sheet_names

        COLUMNS = {
            'gene': 'Gene',
            'reference': 'Reference',
            'taxonomy': 'Taxonomy',
            'eco': 'Eco',
            'disease ID': 'Disease ID',
            'association_type': 'Association type',
            'direction':'Direction',
            'with_ortholog':'With Ortholog',
            'annotation_type':'Annotation type'
        }

        SOURCE_ID = 834
        SEPARATOR = '|'
        HIGH_THROUGHPUT = 'high-throughput'

        list_of_diseases = []
        list_of_diseases_errors = []
        df = pd.read_excel(io=file, sheet_name="Sheet1")

        null_columns = df.columns[df.isnull().any()]
        for col in null_columns:
            if COLUMNS['with_ortholog'] != col and COLUMNS['evidence code'] !=col:
                rows = df[df[col].isnull()].index.tolist()
                rows = ','.join([str(r+2) for r in rows])
                list_of_diseases_errors.append('No values in column ' + col + ' rows ' + rows)
        
        if list_of_diseases_errors:
            err = [e + '\n' for e in list_of_diseases_errors]
            return HTTPBadRequest(body=json.dumps({"error": list_of_diseases_errors}), content_type='text/json')


        sgd_id_to_dbentity_id, systematic_name_to_dbentity_id = models_helper.get_dbentity_by_subclass(['LOCUS', 'REFERENCE'])
        strain_to_taxonomy_id = models_helper.get_common_strains()
        eco_displayname_to_id = models_helper.get_all_eco_mapping()
        happensduring_to_id = models_helper.get_all_go_mapping()
        pubmed_id_to_reference, reference_to_dbentity_id = models_helper.get_references_all()
        list_of_regulator_types = ['chromatin modifier','transcription factor','protein modifier','RNA-binding protein','RNA modifier']
        list_of_regulation_types = ['transcription','protein activity','protein stability','RNA activity','RNA stability']
        list_of_directions = ['positive','negative']

        for index_row,row in df.iterrows():
            index  = index_row + 2;
            column = ''
            try:
                regulation_existing = {
                    'target_id': '',
                    'regulator_id': '',
                    'source_id':SOURCE_ID,
                    'taxonomy_id': '',
                    'reference_id': '',
                    'eco_id': '',
                    'regulator_type': '',
                    'regulation_type': '',
                    'direction': None,
                    'happens_during': '',
                    'annotation_type': HIGH_THROUGHPUT
                }
                regulation_update = {
                    'annotation_type': HIGH_THROUGHPUT
                }

                column = COLUMNS['target']
                target = row[column]
                target_current = str(target.split(SEPARATOR)[0]).strip()
                key = (target_current,'LOCUS')
                if key in sgd_id_to_dbentity_id:
                    regulation_existing['target_id'] = sgd_id_to_dbentity_id[key]
                elif(key in systematic_name_to_dbentity_id):
                    regulation_existing['target_id'] = systematic_name_to_dbentity_id[key]
                else:
                    list_of_regulations_errors.append('Error in target gene on row ' + str(index)+ ', column ' + column)
                    continue
                                
                if SEPARATOR in target:
                    target_new = str(target.split(SEPARATOR)[1]).strip()
                    key = (target_new,'LOCUS')
                
                    if key in sgd_id_to_dbentity_id:
                        regulation_update['target_id'] = sgd_id_to_dbentity_id[key]
                    elif(key in systematic_name_to_dbentity_id):
                        regulation_update['target_id'] = systematic_name_to_dbentity_id[key]
                    else:
                        list_of_regulations_errors.append('Error in target gene on row ' + str(index)+ ', column ' + column)
                        continue
                
                column = COLUMNS['regulator_gene']
                regulator_gene = row[column]
                regulator_gene_current = str(regulator_gene.split(SEPARATOR)[0]).strip()
                key = (regulator_gene_current,'LOCUS')
                if key in sgd_id_to_dbentity_id:
                    regulation_existing['regulator_id'] = sgd_id_to_dbentity_id[key]
                elif(key in systematic_name_to_dbentity_id):
                    regulation_existing['regulator_id'] = systematic_name_to_dbentity_id[key]
                else:
                    list_of_regulations_errors.append('Error in regulator gene on row ' + str(index)+ ', column ' + column)
                    continue
                
                if SEPARATOR in regulator_gene:
                    regulator_gene_new = str(regulator_gene.split(SEPARATOR)[1]).strip()
                    key = (regulator_gene_new,'LOCUS')
                    if key in sgd_id_to_dbentity_id:
                        regulation_update['regulator_id'] = sgd_id_to_dbentity_id[key]
                    elif(key in systematic_name_to_dbentity_id):
                        regulation_update['regulator_id'] = systematic_name_to_dbentity_id[key]
                    else:
                        list_of_regulations_errors.append('Error in regulator gene on row ' + str(index)+ ', column ' + column)
                        continue
                
                column = COLUMNS['reference']
                reference = row[column]
                reference_current = str(reference).split(SEPARATOR)[0]
                key = (reference_current,'REFERENCE')
                if(key in sgd_id_to_dbentity_id):
                    regulation_existing['reference_id'] = sgd_id_to_dbentity_id[key]
                elif(reference_current in pubmed_id_to_reference):
                    regulation_existing['reference_id'] = pubmed_id_to_reference[reference_current]
                elif(reference_current in reference_to_dbentity_id):
                    regulation_existing['reference_id'] = int(reference_current)
                else:
                    list_of_regulations_errors.append('Error in reference on row ' + str(index) + ', column ' + column)
                    continue
                
                if SEPARATOR in str(reference):
                    reference_new = str(reference).split(SEPARATOR)[1]
                    key = (reference_new,'REFERENCE')
                    if(key in sgd_id_to_dbentity_id):
                        regulation_update['reference_id'] = sgd_id_to_dbentity_id[key]
                    elif(reference_new in pubmed_id_to_reference):
                        regulation_update['reference_id'] = pubmed_id_to_reference[reference_new]
                    elif(reference_new in reference_to_dbentity_id):
                        regulation_update['reference_id'] = int(reference_new)
                    else:
                        list_of_regulations_errors.append('Error in reference on row ' + str(index) + ', column ' + column)
                        continue
                 
                column = COLUMNS['taxonomy']
                taxonomy = row[column]
                taxonomy_current = str(taxonomy).upper().split(SEPARATOR)[0]
                if taxonomy_current in strain_to_taxonomy_id:
                    regulation_existing['taxonomy_id'] = strain_to_taxonomy_id[taxonomy_current]
                else:
                    list_of_regulations_errors.append('Error in taxonomy on row ' + str(index) + ', column ' + column)
                    continue
                
                if SEPARATOR in taxonomy:
                    taxonomy_new = str(taxonomy).upper().split(SEPARATOR)[1]
                    if taxonomy_new in strain_to_taxonomy_id:
                        regulation_update['taxonomy_id'] = strain_to_taxonomy_id[taxonomy_new]
                    else:
                        list_of_regulations_errors.append('Error in taxonomy on row ' + str(index) + ', column ' + column)
                        continue
                    
                column = COLUMNS['eco']
                eco = row[column]
                eco_current = str(eco).split(SEPARATOR)[0]
                if eco_current in eco_displayname_to_id:
                    regulation_existing['eco_id'] = eco_displayname_to_id[eco_current]
                else:
                    list_of_regulations_errors.append('Error in eco on row ' + str(index) + ', column ' + column)
                    continue
                
                if SEPARATOR in eco:
                    eco_new = str(eco).split(SEPARATOR)[1]
                    if eco_new in eco_displayname_to_id:
                        regulation_update['eco_id'] = eco_displayname_to_id[eco_new]
                    else:
                        list_of_regulations_errors.append('Error in eco on row ' + str(index) + ', column ' + column)
                        continue
                    

                column = COLUMNS['regulator_type']
                regulator_type = row[column]
                regulator_type_current = str(regulator_type).split(SEPARATOR)[0]
                if regulator_type_current in list_of_regulator_types:
                    regulation_existing['regulator_type'] = regulator_type_current
                else:
                    list_of_regulations_errors.append('Error in regulator type on row ' + str(index) + ', column ' + column)
                    continue
                
                if SEPARATOR in regulator_type:
                    regulator_type_new = str(regulator_type).split(SEPARATOR)[1]
                    if regulator_type_new in list_of_regulator_types:
                        regulation_update['regulator_type'] = regulator_type_new
                    else:
                        list_of_regulations_errors.append('Error in regulator type on row ' + str(index) + ', column ' + column)
                        continue
                    
                column = COLUMNS['regulation_type']
                regulation_type = row[column]
                regulation_type_current = str(regulation_type).split(SEPARATOR)[0]
                if regulation_type_current in list_of_regulation_types:
                    regulation_existing['regulation_type'] = regulation_type_current
                else:
                    list_of_regulations_errors.append('Error in regulation type on row ' + str(index) + ', column ' + column)
                    continue
                
                if SEPARATOR in regulation_type:
                    regulation_type_new = str(regulation_type).split(SEPARATOR)[1]
                    if regulation_type_new in list_of_regulation_types:
                        regulation_update['regulation_type'] = regulation_type_new
                    else:
                        list_of_regulations_errors.append('Error in regulation type on row ' + str(index) + ', column ' + column)
                        continue
                
                column = COLUMNS['direction']
                direction = row[column]
                direction_current = None if pd.isnull(direction) else None if not str(direction).split(SEPARATOR)[0] else str(direction).split(SEPARATOR)[0]
                if direction_current and direction_current not in list_of_directions:
                    list_of_regulations_errors.append('Error in direction on row ' + str(index) + ', column ' + column)
                    continue
                else:
                    regulation_existing['direction'] = direction_current

                if not pd.isnull(direction) and SEPARATOR in direction:
                    direction_new = None if pd.isnull(direction) else None if not str(direction).split(SEPARATOR)[1] else str(direction).split(SEPARATOR)[1]
                    if direction_new and direction_new not in list_of_directions:
                        list_of_regulations_errors.append('Error in direction on row ' + str(index) + ', column ' + column)
                        continue
                    else:
                        regulation_update['direction'] = direction_new
                        
                column = COLUMNS['happens_during']
                happens_during = row[column]
                happens_during_current = None if pd.isnull(happens_during) else None if not str(happens_during).split(SEPARATOR)[0] else str(happens_during).split(SEPARATOR)[0]
                if happens_during_current and happens_during_current not in happensduring_to_id:
                    list_of_regulations_errors.append('Error in direction on row ' + str(index) + ', column ' + column)
                else:
                    regulation_existing['happens_during'] = None if happens_during_current == None else happensduring_to_id[happens_during_current]
                
                if not pd.isnull(happens_during) and SEPARATOR in happens_during:
                    happens_during_new = None if pd.isnull(happens_during) else None if not str(happens_during).split(SEPARATOR)[1] else str(happens_during).split(SEPARATOR)[1]
                    if happens_during_new and happens_during_new not in happensduring_to_id:
                        list_of_regulations_errors.append('Error in happens during on row ' + str(index) + ', column ' + column)
                    else:
                        regulation_update['happens_during'] = None if happens_during_new == None else  happensduring_to_id[happens_during_new]


                list_of_regulations.append([regulation_existing,regulation_update])
            
            except Exception as e:
                list_of_regulations_errors.append('Error in on row ' + str(index) + ', column ' + column + ' ' + e.message)
        

        if list_of_regulations_errors:
            err = [e + '\n' for e in list_of_regulations_errors]
            return HTTPBadRequest(body=json.dumps({"error":list_of_regulations_errors}),content_type='text/json')
        
        INSERT = 0
        UPDATE = 0
        curator_session = get_curator_session(request.session['username'])
        isSuccess = False
        returnValue = ''
        
        if list_of_regulations:
            for item in list_of_regulations:
                regulation,update_regulation = item
                if (len(update_regulation)>1):
                    regulation_in_db = curator_session.query(Regulationannotation).filter(and_(
                        Regulationannotation.target_id == regulation['target_id'],
                        Regulationannotation.regulator_id == regulation['regulator_id'],
                        Regulationannotation.taxonomy_id == regulation['taxonomy_id'],
                        Regulationannotation.reference_id == regulation['reference_id'],
                        Regulationannotation.eco_id == regulation['eco_id'],
                        Regulationannotation.regulator_type == regulation['regulator_type'],
                        Regulationannotation.regulation_type == regulation['regulation_type'],
                        Regulationannotation.happens_during == regulation['happens_during']
                        )).one_or_none()
                    if regulation_in_db is not None:
                        curator_session.query(Regulationannotation).filter(and_(
                        Regulationannotation.target_id == regulation['target_id'],
                        Regulationannotation.regulator_id == regulation['regulator_id'],
                        Regulationannotation.taxonomy_id == regulation['taxonomy_id'],
                        Regulationannotation.reference_id == regulation['reference_id'],
                        Regulationannotation.eco_id == regulation['eco_id'],
                        Regulationannotation.regulator_type == regulation['regulator_type'],
                        Regulationannotation.regulation_type == regulation['regulation_type'],
                        Regulationannotation.happens_during == regulation['happens_during']
                        )).update(update_regulation)
                        UPDATE  = UPDATE + 1

                else:    
                    r = Regulationannotation(
                        target_id = regulation['target_id'],
                        regulator_id = regulation['regulator_id'], 
                        source_id = SOURCE_ID,
                        taxonomy_id = regulation['taxonomy_id'],
                        reference_id = regulation['reference_id'], 
                        eco_id = regulation['eco_id'],
                        regulator_type = regulation['regulator_type'],
                        regulation_type= regulation['regulation_type'],
                        direction = regulation['direction'],
                        happens_during = regulation['happens_during'],
                        created_by = CREATED_BY,
                        annotation_type = regulation['annotation_type']
                    )
                    curator_session.add(r)
                    INSERT = INSERT + 1
            
            try:
                transaction.commit()
                err = '\n'.join(list_of_regulations_errors)
                isSuccess = True    
                returnValue = 'Inserted:  ' + str(INSERT) + ' <br />Updated: ' + str(UPDATE) + '<br />Errors: ' + err
            except IntegrityError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Integrity Error: '+str(e.orig.pgerror)
            except DataError as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = 'Data Error: '+str(e.orig.pgerror)
            except Exception as e:
                transaction.abort()
                if curator_session:
                    curator_session.rollback()
                isSuccess = False
                returnValue = str(e)
            finally:
                if curator_session:
                    curator_session.close()
        
        if isSuccess:
            return HTTPOk(body=json.dumps({"success": returnValue}), content_type='text/json')
        
        return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')    

    except Exception as e:
        return HTTPBadRequest(body=json.dumps({"error":str(e)}),content_type='text/json')
