# author: fgondwe
import os
from glob import glob
import logging
import boto
from boto.s3.key import Key
import pdb
import hashlib
import functools
import multiprocessing
from multiprocessing.pool import IMapIterator
from optparse import OptionParser
import subprocess
import contextlib


VOLUME_PATH = '/genomes'
S3_ACCESS_KEY = os.environ['S3_ACCESS_KEY']
S3_SECRET_KEY = os.environ['S3_SECRET_KEY']
S3_BUCKET = os.environ['S3_BUCKET']


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
    return file_paths


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
            

def update_s3_readmefile(s3_urls, dbentity_id, sgdid, readme_name, s3_bucket):
    """ Add s3_urls to readme_file on s3 """
    try:
        obj = {}
        s3_str = '## S3 URL(S) ' + '\n'
        s3_file_path = './scripts/loading/data/s3_readme_file_' + sgdid + '.README'
        file_name = sgdid + '/' + readme_name
        if s3_urls:
            for item in s3_urls:
                s3_str += item + '\n'
        
        s3_conn = boto.connect_s3(S3_ACCESS_KEY, S3_SECRET_KEY)
        bucket = s3_conn.get_bucket(s3_bucket)
        key_item = Key(bucket)
        key_item.key = file_name
        file_s3 = bucket.get_key(file_name)
        key_item.get_contents_to_filename(s3_file_path)
        with open(s3_file_path, 'a+') as mod_file:
            mod_file.write(s3_str)

        with open(s3_file_path, 'r') as updated_file:
            key_item.set_contents_from_filename(s3_file_path)
            key_item.make_public()
            etag_md5_s3 = file_s3.etag.strip('"').strip("'")
            hash_md5 = hashlib.md5()
            updated_file.seek(0)
            for chunk in iter(lambda: updated_file.read(4096), b""):
                    hash_md5.update(chunk)
            local_md5sum = hash_md5.hexdigest()
            updated_s3_url = file_s3.generate_url(expires_in=0, query_auth=False)
            obj["md5sum"] = etag_md5_s3
            obj["s3_url"] = updated_s3_url
            obj["sgdid"] = sgdid
            obj["readme_name"] = readme_name
            obj["dbentity_id"] = dbentity_id
            obj["file_size"] = updated_file.tell()
        
        if os.apth.exists(s3_file_path):
            os.remove(s3_file_path)
        else:
            logging.error('file: ' + s3_file_path + ' not found')
        
        return obj
    except Exception as e:
        logging.error(e)
        return None


def multi_part_upload_s3(file_path, bucket_name, s3_key_name=None, use_rr=True, make_public=True):
    """ upload file of any size in chuncks 
    
    Notes
    -----
    S3 only supports 5GB files for uploading directly
    For larger files use multi-part file support

    """

    # connect to s3
    s3_connection = boto.connect_s3(S3_ACCESS_KEY, S3_SECRET_KEY)
    s3_bucket = s3_connection.get_bucket(bucket_name)
    if s3_key_name is None:
        s3_key_name = os.path.basename(file_path)

    # get file size
    file_size_MB = os.path.getsize(file_path) / 1e6
    
    if file_size_MB < 60:
        standard_s3_file_transfer(
            s3_bucket, s3_key_name, file_path, file_size_MB, use_rr)
    
    else:
        multipart_s3_file_transfer(
            s3_bucket, s3_key_name, file_path, file_size_MB, use_rr)
    
    s3_key = s3_bucket.get_key(s3_key_name)
    if make_public:
        s3_key.set_acl("public-read")


def upload_cb(complete, total):
    logging.info("Uploaded")
    print("uploaded:" + str(total))


def standard_s3_file_transfer(bucket, s3_key_name, transfer_file, file_size_MB, use_rr):
    """ file transer under 5GB to s3 """

    new_s3_file = bucket.new_key(s3_key_name)
    new_s3_file.set_contents_from_filename(
        transfer_file, reduced_redundancy=use_rr, cb=upload_cb, num_cb=10)
    
    return new_s3_file


def multipart_s3_file_transfer(bucket, s3_key_name, tarball, mb_size, use_rr=True):
    """ file transfer above 5GB to s3 """
    cores = multiprocessing.cpu_count()
    import pdb; pdb.set_trace()
    def split_file(in_file, mb_size, split_num=5):
        prefix = os.path.join(os.path.dirname(in_file), '%sS3PART' % (os.path.basename(s3_key_name)))
        split_size = int(min(mb_size / (split_num * 2.0), 250))

        if not os.path.exists('%saa' % prefix):
            temp = ['split', '-b%sm' % split_size, in_file, prefix]
            subprocess.check_call(temp)
        return sorted(glob('%s*' % prefix))
    
    # part file
    multi_part_file = bucket.initiate_multipart_upload(
        s3_key_name, reduced_redundancy=use_rr)
    with multimap(cores) as pmap:
        for _ in pmap(transfer_part, ((multi_part_file.id, multi_part_file.key_name, multi_part_file.bucket_name, i, part) for (i, part) in enumerate(split_file(tarball, mb_size, cores)))):
            pass
    
    multi_part_file.complete_upload()


def map_wrap(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return apply(f, *args, **kwargs)
    return wrapper


def mp_from_ids(mp_id, mp_keyname, mp_bucketname):
    """Get the multipart upload from the bucket and multipart IDs.
    This allows us to reconstitute a connection to the upload
    from within multiprocessing functions.
    """
    conn = boto.connect_s3()
    bucket = conn.lookup(mp_bucketname)
    mp = boto.s3.multipart.MultiPartUpload(bucket)
    mp.key_name = mp_keyname
    mp.id = mp_id
    return mp


@map_wrap
def transfer_part(mp_id, mp_keyname, mp_bucketname, i, part):
    """Transfer a part of a multipart upload. Designed to be run in parallel.
    """
    mp = mp_from_ids(mp_id, mp_keyname, mp_bucketname)
    print " Transferring", i, part
    with open(part) as t_handle:
        mp.upload_part_from_file(t_handle, i+1)
    os.remove(part)


@contextlib.contextmanager
def multimap(cores=None):
    """Provide multiprocessing imap like function.
    The context manager handles setting up the pool, worked around interrupt issues
    and terminating the pool on completion.
    """
    if cores is None:
        cores = max(multiprocessing.cpu_count() - 1, 1)

    def wrapper(func):
        def wrap(self, timeout=None):
            return func(self, timeout=timeout if timeout is not None else 1e100)
        return wrap
    IMapIterator.next = wrapper(IMapIterator.next)
    pool = multiprocessing.Pool(cores)
    yield pool.imap
    pool.terminate()
