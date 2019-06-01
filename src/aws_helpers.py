# author: fgondwe
import os
from glob import glob
import logging

import pdb

VOLUME_PATH = '/genomes'


def get_volume_files(path):
    return os.path.expanduser(path)


def get_all_file_paths_by_extension(extension, path_str=VOLUME_PATH):
    """ get all files with README extension
 
    Parameters
    ----------
    extension: str
    path_str: str
            optional, defaults to VOLUME_PATH='~/genomes'

    Returns
    -------
    list: list of file location paths
    """

    try:
        result = []
        ext_str = '*.' + extension
        gen_path = os.path.expanduser(path_str)
        for x_path in os.walk(gen_path):
            for y_path in glob(os.path.join(x_path[0], ext_str)):
                result.append(y_path)

        return result
    except Exception as e:
        logging.error(e)
        return None


def get_zip_files():
    """ gets all files with .zip extension """

    file_paths = get_all_file_paths_by_extension('zip')
    return file_paths


def get_sra_files():
    """ gets all files wih .sra extension """

    file_paths = get_all_file_paths_by_extension('sra')


def get_readme_files():
    """ gets all files wih .sra extension """

    file_paths = get_all_file_paths_by_extension('README')
    return file_paths


def get_file_path_helper(lst, name):
    """ get file path from list of file paths """

    if lst:
        for item in lst:
            temp_1 = item.split('/')[-1]
            if temp_1.lower() == name.lower():
                return item
    return None

def get_file_from_path_collection(key, name):
    f_path = None

    obj ={
        'readme': get_readme_files(),
        'zip': get_zip_files(),
        'sra': get_sra_files()
    }
    for k, val in obj.iteritems():
        if k.lower() == key.lower():
            # loop through the array
            f_path = get_file_path_helper(val, name)
    
    return f_path
            





def update_s3_readmefile():
    # TODO: connect to s3, get_readmefile=x
    # TODO: get list of files connected to x from db, retreive s3_urls
    # TODO: update the readme with list of s3_urls
    # TODO: upload the updated file to s3
    # TODO: update db s3_url with the newly updated file and checksum
    return


def modify_reame_file(s3_file, content):
    # TODO: append content to s3_file
    # TODO: upload file to s3, get s3_url and checksum
    # TODO: return obj{url,checksum,name}
    return


def update_readme_file_db(obj_with_changes):
    # TODO: update db with the changes
    return
