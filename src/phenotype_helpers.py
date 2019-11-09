from pyramid.httpexceptions import HTTPBadRequest, HTTPOk
from sqlalchemy.exc import IntegrityError, DataError
import transaction
import json
from src.models import DBSession, Phenotypeannotation, PhenotypeannotationCond, Phenotype,\
     Allele, Reporter, Apo, Chebi, Source, Dbentity, Locusdbentity, Referencedbentity,\
     Straindbentity
from src.curation_helpers import get_curator_session

def insert_phenotype(curator_session, CREATED_BY, source_id, format_name, display_name, observable_id, qualifier_id):

    isSuccess = False
    returnValue = ""
    phenotype_id = None
    try:
        x = None
        if qualifier_id:
            x = Phenotype(format_name = format_name,
                          display_name = display_name,
                          obj_url = '/phenotype/' + format_name,
                          source_id = source_id,
                          observable_id = observable_id,
                          qualifier_id = qualifier_id,
                          created_by = CREATED_BY)
        else:
            x = Phenotype(format_name = format_name,
                          display_name = display_name,
                          obj_url = '/phenotype/' + format_name,
                          source_id = source_id,
                          observable_id = observable_id,
                          created_by = CREATED_BY)

        curator_session.add(x)
        transaction.commit()
        isSuccess = True
        returnValue = "Phenotype: '" + display_name + "' added successfully."
    except IntegrityError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotype failed: ' + str(e.orig.pgerror)
    except DataError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotype failed: ' + str(e.orig.pgerror)
    except Exception as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotype failed: ' + str(e.orig.pgerror)
    finally:
        phenotype_id = x.phenotype_id

    if isSuccess:
        return phenotype_id
    else:
        return returnValue

def insert_allele(curator_session, CREATED_BY, source_id, allele):

    isSuccess = False
    returnValue = ""
    allele_id = None
    try:
        format_name = allele.replace(" ", "_")
        x = Allele(format_name = format_name,
                   display_name = allele,
                   obj_url = '/allele/' + format_name,
                   source_id = source_id,
                   created_by = CREATED_BY)
        curator_session.add(x)
        transaction.commit()
        isSuccess = True
        returnValue = "Allele: '" + allele + "' added successfully."
    except IntegrityError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert allele failed: ' + str(e.orig.pgerror)
    except DataError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert allele failed: ' + str(e.orig.pgerror)
    except Exception as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert allele failed' + ' ' + str(e.orig.pgerror)
    finally:
        allele_id = x.allele_id

    if isSuccess:
        return allele_id
    else:
        return returnValue


def insert_reporter(curator_session, CREATED_BY, source_id, reporter):

    isSuccess = False
    returnValue = ""
    reporter_id = None
    try:
        format_name = reporter.replace(" ", "_")
        x = Reporter(format_name = format_name,
                     display_name = reporter,
                     obj_url = '/reporter/' + format_name,
                     source_id = source_id,
                     created_by = CREATED_BY)
        curator_session.add(x)
        transaction.commit()
        isSuccess = True
        returnValue = "Reporter: '" + reporter + "' added successfully."

    except IntegrityError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert reporter failed: ' + str(e.orig.pgerror)
    except DataError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert reporter failed: ' + str(e.orig.pgerror)
    except Exception as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert reporter failed: ' + str(e.orig.pgerror)
    finally:
        reporter_id = x.reporter_id

    if isSuccess:
        return reporter_id
    else:
        return returnValue

def insert_phenotypeannotation(curator_session, CREATED_BY, source_id, dbentity_id, reference_id, experiment_id, mutant_id, phenotype_id, taxonomy_id, strain_name, experiment_comment, details, allele_id, allele_comment, reporter_id, reporter_comment):

    isSuccess = False
    returnValue = ""
    annotation_id = None

    annot = DBSession.query(Phenotypeannotation).filter_by(dbentity_id=dbentity_id,
                                                           reference_id=reference_id,
                                                           experiment_id=experiment_id,
                                                           mutant_id=mutant_id,
                                                           phenotype_id=phenotype_id,
                                                           taxonomy_id=taxonomy_id,
                                                           strain_name=strain_name,
                                                           details=details,
                                                           allele_id=allele_id,
                                                           reporter_id=reporter_id).one_or_none()
    if annot is not None:
        annotation_id = annot.annotation_id
        conds = DBSession.query(PhenotypeannotationCond).filter_by(annotation_id=annotation_id).all()
        group_id = 0
        if conds is not None:
            for cond in conds:
                if cond.group_id > group_id:
                    group_id = cond.group_id
        return [annotation_id, group_id, 0]
    try:
        x = Phenotypeannotation(dbentity_id=dbentity_id,
                                reference_id=reference_id,
                                experiment_id=experiment_id,
                                mutant_id=mutant_id,
                                phenotype_id=phenotype_id,
                                taxonomy_id=taxonomy_id,
                                strain_name=strain_name,
                                experiment_comment=experiment_comment,
                                details=details,
                                allele_id=allele_id,
                                allele_comment=allele_comment,
                                reporter_id=reporter_id,
                                reporter_comment=reporter_comment,
                                source_id = source_id,
                                created_by = CREATED_BY)
        curator_session.add(x)
        transaction.commit()
        isSuccess = True
        returnValue = "Phenotypeannotation got added successfully."
    except IntegrityError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotypeannotation failed: ' + str(e.orig.pgerror)
    except DataError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotypeannotation failed: ' + str(e.orig.pgerror)
    except Exception as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotypeannotation failed: ' + str(e.orig.pgerror)
    finally:
        annotation_id = x.annotation_id

    if isSuccess:
        return [annotation_id, None, 1]

def insert_phenotypeannotation_cond(curator_session, CREATED_BY, annotation_id, group_id, condition_class, condition_name, condition_value, condition_unit):

    conds = DBSession.query(PhenotypeannotationCond).filter_by(annotation_id=annotation_id,
                                                               condition_class=condition_class,
                                                               condition_name=condition_name,
                                                               condition_value=condition_value,
                                                               condition_unit=condition_unit).all()
    if len(conds) > 0:
        return [conds[0].condition_id, 0]

    if condition_name is None or condition_name == '':
        return 

    try:
        x = PhenotypeannotationCond(annotation_id=annotation_id,
                                    group_id = group_id,
                                    condition_class = condition_class,
                                    condition_name = condition_name,
                                    condition_value = condition_value,
                                    condition_unit = condition_unit,
                                    created_by = CREATED_BY)
        curator_session.add(x)
        transaction.commit()
        isSuccess = True
        returnValue = "Phenotypeannotation_cond row got added successfully."
    except IntegrityError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotypeannotation_cond failed: ' + str(e.orig.pgerror)
    except DataError as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotypeannotation_cond failed: ' + str(e.orig.pgerror)
    except Exception as e:
        transaction.abort()
        if curator_session:
            curator_session.rollback()
        isSuccess = False
        returnValue = 'Insert phenotypeannotation_cond failed: ' + str(e.orig.pgerror)
    finally:
        condition_id = x.condition_id

    if isSuccess:
        return [condition_id, 1]
    return [returnValue, 0]


def add_phenotype_conditions(curator_session, CREATED_BY, annotation_id, group_id, cond_class, cond_names, cond_values, cond_units):

    i = 0
    added = 0
    for cond_name in cond_names:
        if cond_name == '' or cond_name is None:
            continue
        cond_value = ''
        cond_unit = ''
        if cond_class == 'temperature':
            cond_unit = cond_units
            if "pick a degree" in cond_unit:
                cond_unit = ''
        else:
            if len(cond_units) > i:
                cond_unit = cond_units[i]

        if len(cond_values) > i:
            cond_value = cond_values[i]

        [returnValue, count] = insert_phenotypeannotation_cond(curator_session, CREATED_BY,
                                                               annotation_id, group_id,
                                                               cond_class, cond_name,
                                                               cond_value, cond_unit)
        added = added + count
        if str(returnValue).isdigit() is False:
            return [returnValue, 0]
        i = i + 1

    return [1, added]


def check_gene_names(genes, dbentity_id_list, dbentity_id_to_gene_name):

    for gene in genes:
        if gene.startswith('SGD:S') or gene.startswith('S0'):
            sgdid = gene.replace('SGD:', '')
            dbentity = DBSession.query(Locusdbentity).filter_by(sgdid=sgdid).one_or_none()
            if dbentity is not None:
                dbentity_id_list.append(dbentity.dbentity_id)
                dbentity_id_to_gene_name[dbentity.dbentity_id] = dbentity.gene_name
            else:
                return HTTPBadRequest(body=json.dumps({'error': "The SGDID " + sgdid + " is not in the database or it is not for a gene."}), content_type='text/json')
        else:
            dbentity = DBSession.query(Locusdbentity).filter_by(systematic_name=gene).one_or_none()
            if dbentity is not None:
                dbentity_id_list.append(dbentity.dbentity_id)
                dbentity_id_to_gene_name[dbentity.dbentity_id] = dbentity.gene_name
            else:
                return HTTPBadRequest(body=json.dumps({'error': "The systematic_name " + gene + " is not in the database."}), content_type='text/json')
        

def check_reference(ref_id):

    reference_id = None
    if ref_id.startswith('SGD:') or ref_id.startswith('S'):
        ref_id = ref_id.replace("SGD:", "")
        dbentity = DBSession.query(Dbentity).filter_by(sgdid=ref_id).one_or_none()
        if dbentity is None:
            return HTTPBadRequest(body=json.dumps({'error': "The SGDID " + ref_id + " is not in the database"}), content_type='text/json')
        elif dbentity.subclass != 'REFERENCE':
            return HTTPBadRequest(body=json.dumps({'error': "The SGDID " + ref_id + " is not for a reference"}), content_type='text/json')
        reference_id = dbentity.dbentity_id
    elif ref_id.startswith('PMID:'):
        ref_id = ref_id.replace('PMID:', '')
        dbentity = DBSession.query(Referencedbentity).filter_by(pmid=int(ref_id)).one_or_none()
        if dbentity is None:
            return HTTPBadRequest(body=json.dumps({'error': "The PMID " + ref_id + " is not in the database"}), content_type='text/json')
        reference_id = dbentity.dbentity_id
    else:
        dbentity = DBSession.query(Referencedbentity).filter_by(dbentity_id=int(ref_id)).one_or_none()
        if dbentity is None:
            return HTTPBadRequest(body=json.dumps({'error': "The reference_id " + ref_id + " is not in the database"}), content_type='text/json')
        reference_id = int(ref_id)
        
    return reference_id


def check_allele(allele, dbentity_id_list, dbentity_id_to_gene_name):

    if str(allele).isdigit():
        allele_obj = DBSession.query(Allele).filter_by(allele_id=int(allele)).one_or_none() 
        if allele_obj is None:
            return HTTPBadRequest(body=json.dumps({'error': "allele_id " + allele + " is not in the database."}), content_type='text/json')
        allele = allele_obj.display_name

    if len(dbentity_id_list) > 1:
        return HTTPBadRequest(body=json.dumps({'error': "Make sure no allele provided since you have entered the multiple genes."}), content_type='text/json')

    gene_name = dbentity_id_to_gene_name[dbentity_id_list[0]]

    if allele.upper().startswith(gene_name.upper()):
        return 0
    else:
        return HTTPBadRequest(body=json.dumps({'error': "Allele name " + allele + " doesn't match the standard gene name " + gene_name + "."}), content_type='text/json')

def observable_id_mapping():

    all_apo = DBSession.query(Apo).filter_by(apo_namespace='observable').all()
    mapping = {}
    for apo in all_apo:
        mapping[apo.apo_id] = apo.display_name
    return mapping

def check_observable(observable, qualifier_id, chemical_names, reporter_id):
    
    if ("chemical compound" in observable or "resistance to chemicals" in observable) and len(chemical_names) == 0:
        return HTTPBadRequest(body=json.dumps({'error': "Please add a chemical since you have entered observable: " + observable}), content_type='text/json')

    if reporter_id is None and ("protein activity" in observable or "protein/peptide" in observable or "RNA" in observable or observable.startswith("prion")):
        return HTTPBadRequest(body=json.dumps({'error': "Please add a reporter since you have entered observable: " + observable}), content_type='text/json')
    
    if qualifier_id != '' and observable in ("viable", "inviable", "auxotrophy", "sterile", "petite"):
        return HTTPBadRequest(body=json.dumps({'error': "Please do not pick a qualifier since you have entered observable: " + observable}), content_type='text/json')

    return 0

def check_chemicals(chebi_list, chemical_names):

    for id in chebi_list:
        if id == '':
            continue

        if id.startswith("CHEBI:"):
            chebi = DBSession.query(Chebi).filter_by(chebiid=id).one_or_none()
            if chebi is None:
                return HTTPBadRequest(body=json.dumps({'error': id + " is not in the database."}), content_type='text/json')
            else:
                chemical_names.append(chebi.display_name)
        else:    
            return HTTPBadRequest(body=json.dumps({'error': id + " is not a CHEBI ID."}), content_type='text/json')

    return 0


def check_phenotype(curator_session, CREATED_BY, source_id, observable_id, qualifier_id):

    ## adding phenotype if not in database already
    phenotype_id = None
    pheno = None
    if qualifier_id != '':
        pheno = DBSession.query(Phenotype).filter_by(observable_id=observable_id, qualifier_id=qualifier_id).one_or_none()
    else:
        pheno = DBSession.query(Phenotype).filter_by(observable_id=observable_id).filter(Phenotype.qualifier_id.is_(None)).one_or_none()
    if pheno is not None:
        phenotype_id = pheno.phenotype_id
        return [0, phenotype_id, pheno.display_name]

    if phenotype_id is None:
        o = DBSession.query(Apo).filter_by(apo_id=observable_id).one_or_none()
        observable = o.display_name
        qualifier = None
        if qualifier_id != '':
            q = DBSession.query(Apo).filter_by(apo_id=qualifier_id).one_or_none()
            qualifier = q.display_name
        display_name = observable
        format_name = observable
        if qualifier is not None:
            display_name = observable + ": " + qualifier
            format_name = qualifier + "_" + observable
        format_name = format_name.replace(" ", "_")
        returnValue = insert_phenotype(curator_session, CREATED_BY, source_id,
                                       format_name, display_name,
                                       observable_id, qualifier_id)
        return [1, returnValue, display_name]
        
def add_phenotype_annotations(request):

    try:
        CREATED_BY = request.session['username']
        curator_session = get_curator_session(request.session['username'])
        sgd = DBSession.query(Source).filter_by(display_name='SGD').one_or_none()
        source_id = sgd.source_id

        ## gene list: loop through and check every gene 
        genelist = request.params.get('gene_list')
        if genelist == '':
            return HTTPBadRequest(body=json.dumps({'error': "gene list field is blank"}), content_type='text/json')

        genes = genelist.split("|")
        dbentity_id_list = []
        dbentity_id_to_gene_name = {}
        error = check_gene_names(genes, dbentity_id_list, dbentity_id_to_gene_name)

        if error is not None:
            return error

        ## reference
        ref_id = request.params.get('reference_id')
        if ref_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "reference field is blank"}), content_type='text/json')
    
        returnVal = check_reference(ref_id)
        reference_id = None
        if str(returnVal).isdigit():
            reference_id = returnVal
        else:
            return returnVal

        ## experiment_type
        experiment_id = request.params.get('experiment_id')
        if experiment_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "experiment_type field is blank"}), content_type='text/json')
        experiment_id = int(experiment_id)

        ## mutant_type
        mutant_id = request.params.get('mutant_id')
        if mutant_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "mutant_type field is blank"}), content_type='text/json')
        mutant_id = int(mutant_id)

        ## observable
        observable_id = request.params.get('observable_id')
        if observable_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "observable field is blank or the observable you entered is not in the database,"}), content_type='text/json')
        observable_id = int(observable_id)

        ## qualifier
        qualifier_id = request.params.get('qualifier_id')
        if qualifier_id != '':
            qualifier_id = int(qualifier_id)

        ## taxonomy
        taxonomy_id = request.params.get('taxonomy_id')
        if taxonomy_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "Strain background field is blank"}), content_type='text/json')
        taxonomy_id = int(taxonomy_id)

        ## strain_name
        strain_name = request.params.get('strain_name')

        ## experiment_comment
        experiment_comment = request.params.get('experiment_comment')

        ## details
        details = request.params.get('details')

        ## allele
        allele = request.params.get('allele_id')

        ## allele_comment
        allele_comment = request.params.get('allele_comment')

        ## reporter
        reporter = request.params.get('reporter_id')

        ## reporter_comment 
        reporter_comment = request.params.get('reporter_comment')

        success_message= ""

        ## adding phenotype if not in database already   
        [status, returnValue, phenotype] = check_phenotype(curator_session, CREATED_BY, source_id, observable_id, qualifier_id)

        phenotype_id = None
        if status == 0:
            phenotype_id = returnValue
        elif str(returnValue).isdigit():
            phenotype_id = returnValue
            success_message = "The new phenotype '" + phenotype + "' has been added into the database."
        else:
            return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

        ## adding allele if it is not in the database yet
        allele_id = None
        if allele != '':
            err = check_allele(allele, dbentity_id_list, dbentity_id_to_gene_name)
            if err == 0:
                if str(allele).isdigit():
                    allele_id = int(allele)
                else:
                    returnValue = insert_allele(curator_session, CREATED_BY, source_id, allele)
                    if str(returnValue).isdigit():
                        allele_id = returnValue
                        success_message = success_message + "<br>" + "The new allele '" + allele + "' has been added into the database. "
                    else:
                        return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')
            else:
                return err

        ## adding reporter if it is not in the database yet
        reporter_id = None
        if reporter != '':
            if str(reporter).isdigit():
                reporter_id = int(reporter)
            else:
                returnValue = insert_reporter(curator_session, CREATED_BY, source_id, reporter)
                if str(returnValue).isdigit():
                    reporter_id =returnValue
                    success_message = success_message + "<br>" + "The new reporter '" + reporter + "' has been added into the database. "
                else:
                    return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

        ## chemicals                                                                                    
        chebi_list = request.params.get('chemical_name').split("|")

        chemical_names = []
        err = check_chemicals(chebi_list, chemical_names)
        if err != 0:
            return err

        chemical_values = request.params.get('chemical_value').split("|")
        chemical_units = request.params.get('chemical_unit').split("|")


        ## check observable
        observable_id_to_name = observable_id_mapping()
        observable = observable_id_to_name[observable_id]
        err = check_observable(observable, qualifier_id, chemical_names, reporter_id)
        if err != 0:
            return err


        ## media
        media_names = request.params.get('media_name').split("|")
        media_values = request.params.get('media_value').split("|")
        media_units = request.params.get('media_unit').split("|")

        ## temperature
        temperature_names = request.params.get('temperature_name').split("|")
        temperature_values = request.params.get('temperature_value').split("|")
        temperature_unit = request.params.get('temperature_unit')

        ## treatments
        treatment_names = request.params.get('treatment_name').split("|")
        treatment_values = request.params.get('treatment_value').split("|")
        treatment_units = request.params.get('treatment_unit').split("|")

        ## assay - only one
        assay_name = request.params.get('assay_name')
        assay_value = request.params.get('assay_value')
        assay_unit = request.params.get('assay_unit')

        ## phase
        phase_names = request.params.get('phase_name').split("|")
        phase_values = request.params.get('phase_value').split("|")
        phase_units = request.params.get('phase_unit').split("|")

        ## radiation
        radiation_names = request.params.get('radiation_name').split("|")
        radiation_values = request.params.get('radiation_value').split("|")
        radiation_units = request.params.get('radiation_unit').split("|")


        ## loop through each gene and check to see if the annotation is in the database; 
        ## if not, insert it
        index = 0
        for dbentity_id in dbentity_id_list:
            ## add annotation
            [returnValue, curr_group_id, phenoAdded] = insert_phenotypeannotation(curator_session,
                                                                      CREATED_BY, source_id,
                                                                      dbentity_id, reference_id,
                                                                      experiment_id, mutant_id,
                                                                      phenotype_id, taxonomy_id,
                                                                      strain_name, experiment_comment,
                                                                      details, allele_id, allele_comment,
                                                                      reporter_id, reporter_comment)
            annotation_id = None
            if str(returnValue).isdigit():
                annotation_id = returnValue
            else:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            if curr_group_id is None:
                curr_group_id = 0
            group_id = curr_group_id + 1

            conditions_added = 0 

            ## add chemicals
            [returnValue, count] = add_phenotype_conditions(curator_session, CREATED_BY, annotation_id,
                                                            group_id, 'chemical', chemical_names,
                                                            chemical_values, chemical_units)
            conditions_added = conditions_added + count
            if str(returnValue).isdigit() is False:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            ## add media
            [returnValue, count] = add_phenotype_conditions(curator_session, CREATED_BY, annotation_id,
                                                            group_id, 'media', media_names, media_values,
                                                            media_units)
            conditions_added = conditions_added+ count
            if str(returnValue).isdigit() is False:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            ## add temperatures
            if temperature_unit == '--Pick a degree unit--':
                temperature_unit = ''
            [returnValue, count] = add_phenotype_conditions(curator_session, CREATED_BY, annotation_id,
                                                            group_id, 'temperature', temperature_names,
                                                            temperature_values, temperature_unit)
            conditions_added = conditions_added+ count
            if str(returnValue).isdigit() is False:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            ## add treatments 
            [returnValue, count] = add_phenotype_conditions(curator_session, CREATED_BY, annotation_id,
                                                            group_id, 'treatment', treatment_names,
                                                            treatment_values, treatment_units)
            conditions_added = conditions_added+ count
            if str(returnValue).isdigit() is False:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            ## add assay
            if assay_name != '' and assay_name is not None:
                [returnValue, count] = insert_phenotypeannotation_cond(curator_session, CREATED_BY,
                                                                       annotation_id, group_id,
                                                                       'assay', assay_name,
                                                                       assay_value,
                                                                       assay_unit)
                conditions_added = conditions_added+ count
                if str(returnValue).isdigit() is False:
                    return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            ## add phases
            [returnValue, count] = add_phenotype_conditions(curator_session, CREATED_BY, annotation_id,
                                                            group_id, 'phase', phase_names, phase_values,
                                                            phase_units)
            conditions_added = conditions_added+ count
            if str(returnValue).isdigit() is False:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            ## add radiations
            [returnValue, count] = add_phenotype_conditions(curator_session, CREATED_BY, annotation_id,
                                                            group_id, 'radiation', radiation_names,
                                                            radiation_values, radiation_units)
            conditions_added = conditions_added+ count
            if str(returnValue).isdigit() is False:
                return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

            if phenoAdded > 0:
                if conditions_added > 0:
                    success_message = success_message + "<br>" + "The new phenotype annotation along with its condition(s) has been added into the database for " + genes[index] + "."
                else:
                    success_message = success_message + "<br>" + "The new phenotype annotation has been added into the database for " + genes[index] + "."
            else:
                if conditions_added > 0:
                    success_message = success_message + "<br>" + "The phenotype annotation is already in the database, but its condition(s) have been added into the database for " + genes[index] + "."
                else:
                    success_message = success_message + "<br>" + "The phenotype annotation is already in the database for " + genes[index] + "."

            index = index + 1

        transaction.commit()
        return HTTPOk(body=json.dumps({'success': success_message, 'phenotype': "PHENOTYPE"}), content_type='text/json')
    except Exception as e:
        return HTTPBadRequest(body=json.dumps({'error': str(e)}), content_type='text/json')


def update_conditions(curator_session, CREATED_BY, annotation_id, group_id, cond_class, names, values, units):

    newRow = {}
    i = 0
    for name in names:
        if name == '':
            continue
        unit = units
        if cond_class != 'experiment':
            unit = units[i]
        key = (name, values[i], unit)
        i = i + 1
        newRow[key] = 1

    conds = curator_session.query(PhenotypeannotationCond).filter_by(annotation_id=annotation_id, 
                                                                     group_id=group_id, 
                                                                     condition_class=cond_class).all()
    update_count = 0
    oldRow = {}
    for cond in conds:
        key = (cond.condition_name, cond.condition_value, cond.condition_unit)
        oldRow[key] = 1
        if key in newRow:
            continue
        curator_session.delete(cond)
        update_count = update_count + 1

    for key in newRow:
        if key not in oldRow:
            (name, value, unit) = key
            if name is None or name == '':
                continue
            insert_phenotypeannotation_cond(curator_session, CREATED_BY, annotation_id, 
                                            group_id, cond_class, name, value, unit)
            update_count = update_count + 1

    return update_count


def update_all_conditions(request, curator_session, CREATED_BY, annotation_id, group_id):

    ## chemicals
    chebi_list = request.params.get('chemical_name').split("|")
    chemical_names = []
    err = check_chemicals(chebi_list, chemical_names)
    if err != 0:
        return err
    chemical_values = request.params.get('chemical_value').split("|")
    chemical_units = request.params.get('chemical_unit').split("|")
    
    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id, 
                              'chemical', chemical_names, chemical_values, chemical_units)
    update_count = count

    ## media
    media_names = request.params.get('media_name').split("|")
    media_values = request.params.get('media_value').split("|")
    media_units = request.params.get('media_unit').split("|")

    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id,
                              'media', media_names, media_values, media_units)
    update_count = update_count + count

    ## temperature
    temperature_names = request.params.get('temperature_name').split("|")
    temperature_values = request.params.get('temperature_value').split("|")
    temperature_unit = request.params.get('temperature_unit')

    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id,
                              'temperature', temperature_names, temperature_values, 
                              temperature_unit)
    update_count = update_count + count
    
    ## treatments
    treatment_names = request.params.get('treatment_name').split("|")
    treatment_values = request.params.get('treatment_value').split("|")
    treatment_units = request.params.get('treatment_unit').split("|")

    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id,
                              'treatment', treatment_names, treatment_values, 
                              treatment_units)
    update_count = update_count + count

    ## assay - only one
    assay_name = request.params.get('assay_name')
    assay_value = request.params.get('assay_value')
    assay_unit = request.params.get('assay_unit')
    
    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id,
                              'assay', [assay_name], [assay_value], [assay_unit])
    update_count = update_count + count

    ## phase
    phase_names = request.params.get('phase_name').split("|")
    phase_values = request.params.get('phase_value').split("|")
    phase_units = request.params.get('phase_unit').split("|")

    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id,
                              'phase', phase_names, phase_values, phase_units)
    update_count = update_count + count

    ## radiation
    radiation_names = request.params.get('radiation_name').split("|")
    radiation_values = request.params.get('radiation_value').split("|")
    radiation_units = request.params.get('radiation_unit').split("|")

    count = update_conditions(curator_session, CREATED_BY, annotation_id, group_id,
                              'radiation', radiation_names, radiation_values, 
                              radiation_units)
    update_count = update_count + count

    return update_count

def get_apo_by_id(apo_id):

    return DBSession.query(Apo).filter_by(apo_id=apo_id).one_or_none()

def get_strains_by_taxon_id(taxonomy_id):
    
    return DBSession.query(Straindbentity).filter_by(taxonomy_id=taxonomy_id).all()

def update_phenotype_annotations(request):

    try:
        CREATED_BY = request.session['username']
        curator_session = get_curator_session(request.session['username'])
        sgd = DBSession.query(Source).filter_by(display_name='SGD').one_or_none()
        source_id = sgd.source_id

        gene_id_list = request.params.get('gene_id_list')

        if gene_id_list == '':
            return HTTPBadRequest(body=json.dumps({'error': "Please choose one or more genes from the pulldown menu."}), content_type='text/json')

        gene_ids = gene_id_list.split(' ')

        annotation_ids = []
        annotation_id_to_gene = {}
        for gene_id in gene_ids:
            [gene, id] = gene_id.split('|')
            annotation_id = int(id)
            annotation_ids.append(annotation_id)
            annotation_id_to_gene[annotation_id] = gene
        
        update_all = request.params.get('update_all')

        ## get annotation from database for one annotation_id in the list plus group_id 
        annotation_id = int(annotation_ids[0])
        group_id = request.params.get('group_id')
        if group_id is not None:
            if group_id.isdigit():
                group_id = int(group_id)
            else:
                group_id = 0

        paRow = curator_session.query(Phenotypeannotation).filter_by(annotation_id=annotation_id).one_or_none()

        success_message = ''
        updateParams = {}
        paUpdatedCols = []
        ## reference
        ref_id = request.params.get('reference_id')
        if ref_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "reference field is blank"}), content_type='text/json')

        returnVal = check_reference(ref_id)
        reference_id = None
        if str(returnVal).isdigit():
            reference_id = returnVal
        else:
            return returnVal

        if reference_id != paRow.reference_id:
            updateParams['reference_id'] = reference_id
            # success_message = success_message + "<br>" + "The reference has been updated."
            paUpdatedCols.append('reference_id')
        ## experiment_type
        experiment_id = request.params.get('experiment_id')
        if experiment_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "experiment_type field is blank"}), content_type='text/json')
        experiment_id = int(experiment_id)
        
        if experiment_id != paRow.experiment_id:
            updateParams['experiment_id'] = experiment_id
            # success_message = success_message + "<br>" + "The experiment type has been updated."
            paUpdatedCols.append('experiment_id')
        ## mutant_type
        mutant_id = request.params.get('mutant_id')
        if mutant_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "mutant_type field is blank"}), content_type='text/json')
        mutant_id = int(mutant_id)

        if mutant_id != paRow.mutant_id:
            updateParams['mutant_id'] = mutant_id
            # success_message = success_message + "<br>" + "The mutant type has been updated."
            paUpdatedCols.append('mutant_id')
        ## observable
        observable_id = request.params.get('observable_id')
        if observable_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "observable field is blank or the observable you entered is not in the database,"}), content_type='text/json')
        observable_id = int(observable_id)

        ## qualifier
        qualifier_id = request.params.get('qualifier_id')
        if qualifier_id != '':
            qualifier_id = int(qualifier_id)
 
        [status, returnValue, phenotype] = check_phenotype(curator_session, CREATED_BY, source_id, observable_id, qualifier_id)
        
        phenotype_id = None
        if status == 0:
            phenotype_id = returnValue
        elif str(returnValue).isdigit():
            phenotype_id = returnValue
            success_message = success_message + "<br>The new phenotype '" + phenotype + "' has been added into the database."
        else:
            return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')

        if phenotype_id != paRow.phenotype_id:
            updateParams['phenotype_id'] = phenotype_id
            # success_message = success_message + "<br>" + "The phenotype has been updated."
            paUpdatedCols.append('phenotype_id')
        
        ## taxonomy
        taxonomy_id = request.params.get('taxonomy_id')
        if taxonomy_id == '':
            return HTTPBadRequest(body=json.dumps({'error': "Strain background field is blank"}), content_type='text/json')
        taxonomy_id = int(taxonomy_id)

        if taxonomy_id != paRow.taxonomy_id:
            updateParams['taxonomy_id'] = taxonomy_id
            # success_message = success_message + "<br>" + "The Strain_background has been updated."
            paUpdatedCols.append('taxonomy_id')

        ## strain_name 
        strain_name = request.params.get('strain_name')
        if (strain_name or paRow.strain_name) and strain_name != paRow.strain_name:
            updateParams['strain_name'] = strain_name
            # success_message = success_message + "<br>" + "The strain_name has been updated."
            paUpdatedCols.append('strain_name')
        ## experiment_comment
        experiment_comment = request.params.get('experiment_comment')
        if (experiment_comment or paRow.experiment_comment) and experiment_comment != paRow.experiment_comment:
            updateParams['experiment_comment'] = experiment_comment
            # success_message = success_message + "<br>" + "The experiment_comment has been updated."
            paUpdatedCols.append('experiment_comment')

        ## details
        details = request.params.get('details')
        if (details or paRow.details) and details != paRow.details:
            updateParams['details'] = details
            # success_message = success_message + "<br>" + "The details has been updated."
            paUpdatedCols.append('details')

        ## allele
        allele = request.params.get('allele_id')
        if allele and len(annotation_ids) > 1:
            return HTTPBadRequest(body=json.dumps({'error': "You can't provide allele since you have entered multiple genes"}), content_type='text/json')

        ## check allele and adding allele if it is not in the database yet
        allele_id = None
        if allele == '':
            if paRow.allele_id:
                updateParams['allele_id'] = allele_id
                # success_message = success_message + "<br>" + "The allele has been updated."
                paUpdatedCols.append('allele_id')
        elif str(allele).isdigit():
            allele_id = int(allele)
            if allele_id != paRow.allele_id:
                updateParams['allele_id'] = allele_id
                # success_message = success_message + "<br>" + "The allele has been updated."
                paUpdatedCols.append('allele_id')
        else:
            if allele.upper().startswith(paRow.dbentity.gene_name.upper()):
                returnValue = insert_allele(curator_session, CREATED_BY, source_id, allele)
                if str(returnValue).isdigit():
                    allele_id = returnValue
                    # success_message = success_message + "<br>" + "The new allele '" + allele + "' has been added into the database. "
                    paUpdatedCols.append('allele_id')
                    if allele_id != paRow.allele_id:
                        updateParams['allele_id'] = allele_id
                        # success_message = success_message + "<br>" + "The allele has been updated."
                        paUpdatedCols.append('allele_id')
                else:
                    return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')
            else:
                return HTTPBadRequest(body=json.dumps({'error': "Allele name " + allele + " doesn't match the standard gene name " + gene_name + "."}), content_type='text/json')

        ## allele_comment
        allele_comment = request.params.get('allele_comment')
        if (allele_comment or paRow.allele_comment) and allele_comment != paRow.allele_comment:
            updateParams['allele_comment'] = allele_comment
            # success_message = success_message + "<br>" + "The allele_comment has been updated."
            paUpdatedCols.append('allele_comment')

        ## reporter
        reporter = request.params.get('reporter_id')
        ## adding reporter if it is not in the database yet
        reporter_id = None
        if reporter != '':
            if str(reporter).isdigit():
                reporter_id = int(reporter)
            else:
                returnValue = insert_reporter(curator_session, CREATED_BY, source_id, reporter)
                if str(returnValue).isdigit():
                    reporter_id =returnValue
                    # success_message = success_message + "<br>" + "The new reporter '" + reporter + "' has been added into the database. "
                    paUpdatedCols.append('reporter_id')
                else:
                    return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')
        if reporter_id != paRow.reporter_id:
            updateParams['reporter_id'] = reporter_id
            # success_message = success_message + "<br>" + "The reporter has been updated."
            paUpdatedCols.append('reporter_id')

        ## reporter_comment
        reporter_comment = request.params.get('reporter_comment')
        if (reporter_comment or paRow.reporter_comment) and reporter_comment != paRow.reporter_comment:
            updateParams['reporter_comment'] = reporter_comment
            # success_message = success_message + "<br>" + "The reporter_comment has been updated."
            paUpdatedCols.append('reporter_comment')
 
        for annotation_id in annotation_ids:
            
            paRow = curator_session.query(Phenotypeannotation).filter_by(annotation_id=annotation_id).one_or_none()

            if paRow is None:
                return HTTPBadRequest(body=json.dumps({'error': "annotation_id="+str(annotation_id)+" is not in Phenotypeannotation table."}), content_type='text/json')

            gene_name = annotation_id_to_gene[annotation_id]

            allConds = curator_session.query(PhenotypeannotationCond).filter_by(annotation_id=annotation_id).all()

            new_annotation_id = None
            new_group_id = None

            if update_all is not None:
                ## update phenotypeannotaton directly
                if len(updateParams.keys()) > 0:
                    curator_session.query(Phenotypeannotation).filter_by(annotation_id=annotation_id).update(updateParams)
                    success_message = success_message + "<br>" + "The column(s): <strong>" + ', '.join(paUpdatedCols) + "</strong> in phenotypeannotation has been updated for gene " + gene_name + " and annotation_id=" + str(annotation_id)
                elif success_message == '':
                    success_message = success_message + "<br>" + "Nothing is changed in phenotypeannotation table"
            else:
                if len(allConds) == 0:
                    if group_id == 0:
                        if len(updateParams.keys()) > 0:
                            curator_session.query(Phenotypeannotation).filter_by(annotation_id=annotation_id).update(updateParams)
                            success_message = success_message + "<br>" + "The column(s): <strong>" + ', '.join(paUpdatedCols) + "</strong> in phenotypeannotation has been updated for gene " + gene_name + " and annotation_id=" + str(annotation_id)
                        elif success_message == '':
                            success_message = success_message + "<br>" + "Nothing is changed in phenotypeannotation table."
                        continue
                    else:
                        return HTTPBadRequest(body=json.dumps({'error': 'There is no condition associated with annotation_id='+str(annotation_id) + ' for gene ' + gene_name + ', but a condition group_id=' + str(group_id) + ' is passed in.'}), content_type='text/json')

                elif len(allConds) == 1:
                    if group_id == allConds[0].group_id:
                        ## update paRow row directly
                        if len(updateParams.keys()) > 0:
                            # paRow.update(updateParams)
                            curator_session.query(Phenotypeannotation).filter_by(annotation_id=annotation_id).update(updateParams)
                            success_message = success_message + "<br>" + "The column(s): <strong>" + ', '.join(paUpdatedCols) + "</strong> in phenotypeannotation has been updated for gene " + gene_name + " and annotation_id=" + str(annotation_id)
                        elif success_message == '':
                            success_message = success_message + "<br>" + "Nothing is changed in phenotypeannotation table."
                    else:
                        return HTTPBadRequest(body=json.dumps({'error': 'The group_id=' + str(group_id) + ' is not in the database for annotation_id='+str(annotation_id) + ' for gene ' + gene_name + '.'}), content_type='text/json')

                else:
                    found = 0
                    for cond in allConds:
                        if cond.group_id == group_id:
                            ## add a new paRow if there is update in the paRow
                            if len(updateParams.keys()) > 0:
                                ## add annotation 
                                [returnValue, curr_group_id, phenoAdded] = insert_phenotypeannotation(curator_session,
                                                                CREATED_BY, source_id,
                                                                paRow.dbentity_id, reference_id,
                                                                experiment_id, mutant_id,
                                                                phenotype_id, taxonomy_id,
                                                                strain_name, experiment_comment,
                                                                details, allele_id, allele_comment,
                                                                reporter_id, reporter_comment)
                                
                                  
                                if str(returnValue).isdigit():
                                    new_annotation_id = returnValue
                                    success_message = success_message + "<br>" + "A new phenotype annotation row has been added for gene " + gene_name + " and new annotation_id=" + str(new_annotation_id)
                                else:
                                    return HTTPBadRequest(body=json.dumps({'error': returnValue}), content_type='text/json')
                                
                                if curr_group_id is None:
                                    curr_group_id = 0
                                new_group_id = curr_group_id + 1
                                    
                            found = 1
                            break
                    if found == 0:
                        return HTTPBadRequest(body=json.dumps({'error': 'The group_id=' + str(group_id) + ' is not in thedatabase for annotation_id='+str(annotation_id) + '.'}), content_type='text/json')

            if new_annotation_id:
                curator_session.query(PhenotypeannotationCond).filter_by(annotation_id=annotation_id, group_id=group_id).update({'annotation_id': new_annotation_id, 'group_id': new_group_id})

            if group_id > 0:
                updated = update_all_conditions(request, curator_session, CREATED_BY, annotation_id, group_id)    
                if updated > 0:
                    success_message = success_message + "<br>" + "The phenotypeannotation_cond row(s) have been updated for gene " + gene_name + "."

        transaction.commit()
        return HTTPOk(body=json.dumps({'success': success_message, 'phenotype': "PHENOTYPE"}), content_type='text/json')
    except Exception as e:
        return HTTPBadRequest(body=json.dumps({'error': str(e)}), content_type='text/json')


def delete_phenotype_annotations(request):

    try:
        CREATED_BY = request.session['username']
        curator_session = get_curator_session(request.session['username'])

        group_id = request.params.get('group_id')
        
        gene_id_list = request.params.get('gene_id_list')
        if gene_id_list == '':
            return HTTPBadRequest(body=json.dumps({'error': "Please choose one or more genes from the pulldown menu."}), content_type='text/json')
        gene_ids = gene_id_list.split(' ')

        annotation_ids = []
        annotation_id_to_gene = {}
        for gene_id in gene_ids:
            [gene, id] = gene_id.split('|')
            annotation_id = int(id)
            annotation_ids.append(annotation_id)
            annotation_id_to_gene[annotation_id] = gene

        success_message = ''
        for annotation_id in annotation_ids:
            # if no group_id is passed in, then simply delete the annotation => it will 
            # automatically delete all associated conditions (all groups)
            #
            # if this annotation_id has no condition or has only one group of conditions and
            # group_id = the group_id that is passed in, then delete this annotation since 
            # it will delete any associated conditions too
            #
            # if this annotation_id has more than one group of condition, then keep this annotation, 
            # just delete the conditions that have the group_id = the passed in group_id
            #
            paRow = curator_session.query(Phenotypeannotation).filter_by(annotation_id=annotation_id).one_or_none()

            if paRow is None:
                return HTTPBadRequest(body=json.dumps({'error': "annotation_id="+str(annotation_id)+" is not in Phenotypeannotation table."}), content_type='text/json')

            gene_name = annotation_id_to_gene[annotation_id]

            if group_id is None:
                curator_session.delete(paRow)
                success_message = success_message + "<br>" + "The annotation has been deleted for " + gene_name + "."
                continue
            
            ####################
            allConds = curator_session.query(PhenotypeannotationCond).filter_by(annotation_id=annotation_id).all()

            ## no conditions for the given annotation_id, just delete the annotation
            if len(allConds) == 0:
                curator_session.delete(paRow)
                success_message = success_message + "<br>" + "The annotation has been deleted for " + gene_name + "."
                continue

            ## check for group_id
            if str(group_id).isdigit() is False:
                group_id == 0
            else:
                group_id = int(group_id)

            ## make sure there is a group_in passed in if there are condition(s) for 
            ## the annotation
            if len(allConds) > 0 and group_id == 0:
                return HTTPBadRequest(body=json.dumps({'error': "There are multiple condition(s) associated with " + gene_name + ". Please pass in a group_id."}), content_type='text/json')
            
            ## has condition(s) for the given annotation_id
            otherCondCount = 0
            for condRow in allConds:
                if condRow.group_id == group_id:
                    curator_session.delete(condRow)
                else:
                    otherCondCount = otherCondCount + 1

            ## if not conditions for the given group_id, give warning:
            if len(allConds) == otherCondCount:
                return HTTPBadRequest(body=json.dumps({'error': "There are multiple condition(s) associated with " + gene_name + ". Please pass in a correct group_id."}), content_type='text/json')
            elif otherCondCount == 0:
                curator_session.delete(paRow)
                success_message = success_message + "<br>" + "The annotation along with its condition(s) (group_id=" + str(group_id) + ") has been deleted for " + gene_name + "."
                
        transaction.commit()
        return HTTPOk(body=json.dumps({'success': success_message, 'phenotype': "PHENOTYPE"}), content_type='text/json')
    except Exception as e:
        return HTTPBadRequest(body=json.dumps({'error': str(e)}), content_type='text/json')

def phenotype_to_dict(row):

    dbentity = DBSession.query(Locusdbentity).filter_by(dbentity_id=row.dbentity_id).one_or_none()

    data = {}
    
    # data['annotation_identifier'] = ""
    # if dbentity.gene_name and dbentity.systematic_name.lower() != dbentity.gene_name.lower():
    #    data['annotation_identifier'] = dbentity.gene_name + "/"
    # data['annotation_identifier'] = data['annotation_identifier'] + dbentity.systematic_name + "|" + str(row.annotation_id)
    if dbentity.gene_name and dbentity.systematic_name.lower() != dbentity.gene_name.lower(): 
        data['annotation_identifier'] = dbentity.systematic_name + '/' + dbentity.gene_name +"|" + str(row.annotation_id)
    else:
        data['annotation_identifier'] = dbentity.systematic_name + "|" + str(row.annotation_id)

    data['paper'] = row.reference.display_name
    if row.reference.pmid:
        data['paper'] = data['paper'] + " PMID:" + str(row.reference.pmid)
    else:
        data['paper'] = data['paper'] + " SGD:" + row.reference.sgdid
 
    data['phenotype'] = row.phenotype.display_name
    if row.reporter_id:
        data['phenotype'] = data['phenotype'] + " Reporter: " + row.reporter.display_name

    experiment = get_apo_by_id(row.experiment_id)
    mutant = get_apo_by_id(row.mutant_id)
    data['experiment_type'] = experiment.display_name
    data['mutant_type'] = mutant.display_name
    if row.allele_id:
        data['mutant_type'] = data['mutant_type'] + " Allele: " + row.allele.display_name

    strain = get_strains_by_taxon_id(row.taxonomy_id)
    strain_obj = None
    if len(strain) == 0 or len(strain) > 1:
        data['strain_background'] = 'Other'
    else:
        data['strain_background'] = strain[0].display_name

    if row.details:
        data['note'] = row.details

    conditions = DBSession.query(PhenotypeannotationCond).filter_by(annotation_id=row.annotation_id).all()

    groups = {}

    for condition in conditions:
        if condition.group_id not in groups:
            groups[condition.group_id] = []

        groups[condition.group_id].append({
                   "condition_class": condition.condition_class,
                   "condition_name": condition.condition_name,
                   "condition_value": condition.condition_value,
                   "condition_unit": condition.condition_unit
        })

    data['groups'] = groups

    return data


def group_phenotypes(data):

    key2annotation = {}
    key2annotation_identifier_list = {}
    for d in data:
        all_conditions = d['groups']
        k = d['phenotype']+'|'+d['experiment_type']+'|'+d['mutant_type']+'|'+d['strain_background']+'|'+ d['paper']
        if len(all_conditions) == 0:
            row = {}
            row['phenotype'] = d['phenotype']
            row['experiment_type'] = d['experiment_type']
            row['mutant_type'] = d['mutant_type']
            row['strain_background'] = d['strain_background']
            row['paper'] = d['paper']
            row['note'] = d.get('note', '')
            row['details'] = row['note']
            row['group_id'] = 0
            key = k
            annotation_identifier_list = []
            if key in key2annotation:
                annotation_identifiler_list = key2annotation_identifier_list[key]
            else:
                key2annotation[key] = row
            if d['annotation_identifier'] not in annotation_identifier_list:
                annotation_identifier_list.append(d['annotation_identifier'])
            key2annotation_identifier_list[key] = annotation_identifier_list
            continue

        for group_id in sorted (all_conditions.keys()):
            row = {}
            row['phenotype'] = d['phenotype']
            row['experiment_type'] = d['experiment_type']
            row['mutant_type'] = d['mutant_type']
            row['strain_background'] = d['strain_background']
            row['paper'] = d['paper']
            row['note'] = d.get('note', '')
            row['group_id'] = group_id
            conditions = all_conditions[group_id]
            details= ""    
            for condition in conditions:
                if details:
                    details = details + ' | '
                details = details + condition['condition_class'].capitalize() + ': ' + str(condition['condition_name'])
                if condition['condition_value']:
                    details = details + ', ' + str(condition['condition_value'])
                    if condition['condition_unit']:
                        details = details + ' ' + str(condition['condition_unit'])
            if row.get('note') and details:
                details = details + ' | Details: ' + row['note']
            elif row.get('note'):
                details = 'Details: ' + row['note']
            row['details'] = details
            key = k + '|' + details
            annotation_identifier_list = []
            if key in key2annotation:
                annotation_identifier_list = key2annotation_identifier_list[key]
            else:
                key2annotation[key] = row
            if d['annotation_identifier'] not in annotation_identifier_list:
                annotation_identifier_list.append(d['annotation_identifier'])     
            key2annotation_identifier_list[key] = annotation_identifier_list

    sortedData = []
    for key in sorted (key2annotation_identifier_list.keys()):
        row = key2annotation[key]
        identifier_list = key2annotation_identifier_list[key]
        identifier_list.sort()
        row['annotation_identifier_list'] = identifier_list
        sortedData.append(row)

    return sortedData

def get_one_phenotype(request):

    annotation_id = str(request.matchdict['annotation_id'])
    group_id = str(request.matchdict['group_id'])
    
    row = DBSession.query(Phenotypeannotation).filter_by(annotation_id=int(annotation_id)).one_or_none()
    
    data = {}
    if row is not None:
        data['reference_id'] = row.reference.pmid
        if data['reference_id']:
            data['reference_id'] = 'PMID:' + str(data['reference_id'])
        else:
            data['reference_id'] ='SGD:' + row.reference.sgdid

        data['observable_id'] = row.phenotype.observable_id
        data['qualifier_id'] = row.phenotype.qualifier_id
        data['experiment_id'] = row.experiment_id
        data['mutant_id'] = row.mutant_id

        observable = get_apo_by_id(data['observable_id'])
        data['observable'] = observable.display_name

        if data['qualifier_id']:
            qualifier = get_apo_by_id(data['qualifier_id'])
            data['qualifier'] = qualifier.display_name

        data['allele_id'] = row.allele_id
        if row.allele_id:
            data['allele'] = row.allele.display_name
            data['allele_comment'] = row.allele_comment

        data['reporter_id'] = row.reporter_id
        if row.reporter_id:
            data['reporter'] = row.reporter.display_name
            data['reporter_comment'] = row.reporter_comment
        
        data['taxonomy_id'] = row.taxonomy_id

        strain = get_strains_by_taxon_id(row.taxonomy_id)
        strain_obj = None
        if len(strain) == 0 or len(strain) > 1:
            data['strain_background'] = 'Other'
        else:
            data['strain_background'] = strain[0].display_name
        data['strain_name'] = row.strain_name

        data['details'] = row.details

        data['experiment_comment'] = row.experiment_comment

        conditions = DBSession.query(PhenotypeannotationCond).filter_by(annotation_id=row.annotation_id, group_id=group_id).all()

        for condition in conditions:
            condition_name = condition.condition_name
            if condition.condition_class == "chemical":
                chebi = DBSession.query(Chebi).filter_by(display_name=condition_name).one_or_none()
                condition_name = chebi.chebiid
            name = condition.condition_class + '_name'
            value = condition.condition_class + '_value'
            unit = condition.condition_class + '_unit'
            if data.get(name):
                data[name] = data[name] + '|' + condition_name
            else:
                data[name] = condition_name

            if data.get(value):
                data[value] = data[value] + '|' + condition.condition_value
            else:
                data[value] = condition.condition_value

            if data.get(unit):
                if condition.condition_class != "temperature":
                    data[unit] = data[unit] + '|' + condition.condition_unit
            else:
                data[unit] = condition.condition_unit

    return data


def get_list_of_phenotypes(request):

    genes = str(request.matchdict['gene'])
    reference = str(request.matchdict['reference'])
    
    if genes in ['none', 'None']:
        genes = None
    if reference in ['none','None']:
        reference = None
    if genes is None and reference is None:
        return HTTPBadRequest(body=json.dumps({'error': 'No gene(s) or reference provided'}), content_type='text/json')

    gene_list = []
    if genes is not None: 
        genes = genes.replace(' ', '|')
        gene_list = genes.split("|")
    
    dbentity_id_list = []
    for gene in gene_list:
        if gene == '':
            continue
        locus_id = None
        if gene is not None:
            if gene.startswith('SGD:S') or gene.startswith('S'):
                sgdid = gene.replace('SGD:', '')
                dbentity = DBSession.query(Locusdbentity).filter_by(sgdid=sgdid).one_or_none()
            else:
                dbentity = DBSession.query(Locusdbentity).filter_by(systematic_name=gene).one_or_none()
            if dbentity is None:
                return HTTPBadRequest(body=json.dumps({'error': 'systematic_name/SGDID '+ gene + ' is not found in database'}), content_type='text/json')
            elif dbentity.dbentity_id not in dbentity_id_list:
                dbentity_id_list.append(dbentity.dbentity_id)

    reference_id = None
    if reference is not None:
        if reference.startswith('SGD:') or reference.startswith('S'):
            reference = reference.replace("SGD:", "")
            dbentity = DBSession.query(Dbentity).filter_by(sgdid=reference).one_or_none()
            if dbentity is None:
                return HTTPBadRequest(body=json.dumps({'error': "The SGDID " + reference + " is not in the database"}), content_type='text/json')
            elif dbentity.subclass != 'REFERENCE':
                return HTTPBadRequest(body=json.dumps({'error': "The SGDID " + reference + " is not for a reference"}), content_type='text/json')
            reference_id = dbentity.dbentity_id
        elif reference.startswith('PMID:'):
            reference = reference.replace('PMID:', '')
            dbentity = DBSession.query(Referencedbentity).filter_by(pmid=int(reference)).one_or_none()
            if dbentity is None:
                return HTTPBadRequest(body=json.dumps({'error': "The PMID " + reference + " is not in the database"}), content_type='text/json')
            reference_id = dbentity.dbentity_id
        else:
            dbentity = DBSession.query(Referencedbentity).filter_by(dbentity_id=int(reference)).one_or_none()
            if dbentity is None:
                return HTTPBadRequest(body=json.dumps({'error': "The reference_id " + reference + " is not in the database"}), content_type='text/json')
            reference_id = int(reference)

    phenotypes = None
    if len(dbentity_id_list) > 0 and reference_id is not None:
        phenotypes = DBSession.query(Phenotypeannotation).filter(Phenotypeannotation.dbentity_id.in_(dbentity_id_list)).filter_by(reference_id=reference_id).order_by(Phenotypeannotation.phenotype_id, Phenotypeannotation.experiment_id, Phenotypeannotation.mutant_id).all()
    elif len(dbentity_id_list) > 0:
        phenotypes = DBSession.query(Phenotypeannotation).filter(Phenotypeannotation.dbentity_id.in_(dbentity_id_list)).order_by(Phenotypeannotation.phenotype_id, Phenotypeannotation.experiment_id, Phenotypeannotation.mutant_id).all()
    else:
        phenotypes = DBSession.query(Phenotypeannotation).filter_by(reference_id=reference_id).order_by(Phenotypeannotation.phenotype_id, Phenotypeannotation.experiment_id, Phenotypeannotation.mutant_id).all()

    if phenotypes is None:
        return []

    data = []

    for row in phenotypes:
        data.append(phenotype_to_dict(row))
        
    # sortedData = None
    # if len(dbentity_id_list) == 0 and reference_id is not None and len(phenotypes) > 10: 
    #    sortedData = group_phenotypes(data)
    # else:
    #    sortedData = data

    sortedData = group_phenotypes(data) 
    
    return HTTPOk(body=json.dumps(sortedData), content_type='text/json')
    


        


    
