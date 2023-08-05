# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2022 Luzzi Valerio
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        s3.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     21/04/2022
# -------------------------------------------------------------------------------
import os
import hashlib
import boto3
import shutil
import requests
import datetime
from botocore.exceptions import ClientError
from .filesystem import *
from .module_log import Logger


def iss3(filename):
    """
    iss3
    """
    return filename and isinstance(filename, str) and \
        (filename.startswith("s3:/") or filename.startswith("/vsis3/"))


def isfile(filename):
    """
    isfile
    """
    if not filename:
        return False    
    elif isinstance(filename, str) and os.path.isfile(filename):
        return True
    elif iss3(filename) and s3_exists(filename):
        return True
    #test if is a http url 
    elif isinstance(filename, str) and filename.startswith("http"):
        try:
            r = requests.head(filename)
            return r.status_code == requests.codes.ok
        except Exception as ex:
            Logger.error(ex)

    return False


def get_bucket_name_key(uri):
    """
    get_bucket_name_key - get bucket name and key name from uri
    """
    bucket_name, key_name = None, None
    if not uri:
        pass
    elif uri.startswith("s3://"):
        # s3://saferplaces.co/tests/rimini/dem.tif
        _, _, bucket_name, key_name = uri.split("/", 3)
    elif uri.startswith("s3:/"):
        # s3:/saferplaces.co/tests/rimini/dem.tif
        _, bucket_name, key_name = uri.split("/", 2)
    elif uri.startswith("/vsis3/"):
        # /vsis3/saferplaces.co/tests/rimini/dem.tif
        _, _, bucket_name, key_name = uri.split("/", 3)
    elif uri.startswith("https://s3.amazonaws.com/"):
        _, _, bucket_name, key_name = uri.split("/", 3)
    else:
        bucket_name, key_name = None, uri
    return bucket_name, key_name


def get_client(client=None):
    """
    get_client
    """
    return client if client else boto3.client('s3')


def etag(filename, client=None, chunk_size=8 * 1024 * 1024):
    """
    calculates a multipart upload etag for amazon s3
    Arguments:
    filename   -- The file to calculate the etag for
    """
    if filename and os.path.isfile(filename):
        md5 = []
        with open(filename, 'rb') as fp:
            while True:
                data = fp.read(chunk_size)
                if not data:
                    break
                md5.append(hashlib.md5(data))
        if len(md5) == 1:
            return f"{md5[0].hexdigest()}"
        digests = b''.join(m.digest() for m in md5)
        digests_md5 = hashlib.md5(digests)
        return f"{digests_md5.hexdigest()}-{len(md5)}"

    elif filename and iss3(filename):
        uri = filename
        ETag = ""
        try:
            bucket_name, key_name = get_bucket_name_key(uri)
            if bucket_name and key_name:
                client = get_client(client)
                ETag = client.head_object(Bucket=bucket_name, Key=key_name)[
                    'ETag'][1:-1]
        except ClientError as ex:
            #Logger.error(ex)
            ETag = ""
        return ETag
    else:
        return ""


def s3_equals(file1, file2, client=None):
    """
    s3_equals - check if s3 object is equals to local file
    """
    etag1 = etag(file1, client)
    etag2 = etag(file2, client)
    # print(file1, etag1) 
    # print(file2, etag2)
    # print("====================================")
    if etag1 and etag2:
        return etag1 == etag2
    return False


def tempname4S3(uri):
    """
    tempname4S3
    """
    dest_folder = tempdir("s3")
    if uri.startswith("s3://"):
        tmp = uri.replace("s3://", dest_folder + "/")
    if uri.startswith("s3:/"):
        tmp = uri.replace("s3:/", dest_folder + "/")
    elif uri.startswith("/vsis3/"):
        tmp = uri.replace("/vsis3/", dest_folder + "/")
    else:
        tmp = dest_folder + "/" + uri
    return tmp


def s3_upload(filename, uri, remove_src=False, client=None):
    """
    Upload a file to an S3 bucket
    Examples: s3_upload(filename, "s3://saferplaces.co/a/rimini/lidar_rimini_building_2.tif")
    """

    # Upload the file
    try:
        bucket_name, key = get_bucket_name_key(uri)
        if bucket_name and key and filename and os.path.isfile(filename):
            client = get_client(client)
            if s3_equals(uri, filename, client):
                Logger.debug(f"file {filename} already uploaded")
            else:
                Logger.debug(
                    f"uploading {filename} into {bucket_name}/{key}...")

                extra_args = {}

                client.upload_file(Filename=filename,
                                   Bucket=bucket_name, Key=key,
                                   ExtraArgs=extra_args)
                
                
            if remove_src:
                Logger.debug(f"removing {filename}")
                os.unlink(filename)  # unlink and not ogr_remove!!!
            return True

    except ClientError as ex:
        Logger.error(ex)

    return False


def s3_download(uri, fileout=None, remove_src=False, client=None):
    """
    Download a file from an S3 bucket
    """
    bucket_name, key = get_bucket_name_key(uri)
    if bucket_name:
        try:
            # check the cache
            client = get_client(client)

            if key and not key.endswith("/"):

                if not fileout:
                    fileout = tempname4S3(uri)

                if os.path.isdir(fileout):
                    fileout = f"{fileout}/{justfname(key)}"

                if os.path.isfile(fileout) and s3_equals(uri, fileout, client):
                    Logger.debug(f"using cached file {fileout}")
                else:
                    # Download the file
                    Logger.debug(f"downloading {uri} into {fileout}...")
                    os.makedirs(justpath(fileout), exist_ok=True)
                    client.download_file(
                        Filename=fileout, Bucket=bucket_name, Key=key)
                    if remove_src:
                        client.delete_object(Bucket=bucket_name, Key=key)
            else:
                objects = client.list_objects_v2(
                    Bucket=bucket_name, Prefix=key)['Contents']
                for obj in objects:
                    pathname = obj['Key']
                    if not pathname.endswith("/"):
                        dst = fileout
                        pathname = pathname.replace(key, "")
                        s3_download(f"{uri.rstrip('/')}/{pathname}",
                                    f"{dst}/{pathname}", client)

        except ClientError as ex:
            #Logger.error(ex)
            return None

    return fileout if os.path.isfile(fileout) else None


def s3_exists(uri, client=None):
    """
    s3_exists
    """
    res = False
    try:
        bucket_name, filepath = get_bucket_name_key(uri)
        if bucket_name and filepath:
            client = get_client(client)
            client.head_object(Bucket=bucket_name, Key=filepath)
            res = True
    except ClientError as ex:
        Logger.error(ex)
    return res


def s3_remove(uri, client=None):
    """
    s3_remove
    """
    res = False
    try:
        bucket_name, filepath = get_bucket_name_key(uri)
        if bucket_name and filepath:
            client = get_client(client)
            client.delete_object(Bucket=bucket_name, Key=filepath)
            res = True
    except ClientError as ex:
        Logger.error(ex)
    return res


def s3_copy(src, dst, client=None):
    """
    s3_copy
    """
    res = False
    try:
        src_bucket_name, src_filepath = get_bucket_name_key(src)
        dst_bucket_name, dst_filepath = get_bucket_name_key(dst)
        if src_bucket_name and src_filepath and dst_bucket_name and dst_filepath:
            client = get_client(client)
            client.copy_object(Bucket=dst_bucket_name, Key=dst_filepath,
                               CopySource={'Bucket': src_bucket_name, 'Key': src_filepath})
            res = True
    except ClientError as ex:
        Logger.error(ex)
    return res


def s3_move(src, dst, client=None):
    """
    s3_move
    """
    res = False
    try:
        src_bucket_name, src_filepath = get_bucket_name_key(src)
        dst_bucket_name, dst_filepath = get_bucket_name_key(dst)
        if src_bucket_name and src_filepath and dst_bucket_name and dst_filepath:
            client = get_client(client)
            client.copy_object(Bucket=dst_bucket_name, Key=dst_filepath,
                               CopySource={'Bucket': src_bucket_name, 'Key': src_filepath})
            client.delete_object(Bucket=src_bucket_name, Key=src_filepath)
            res = True
    except ClientError as ex:
        Logger.error(ex)
    return res


def copy(src, dst=None, client=None):
    """
    copy
    """
    dst = dst if dst else tempname4S3(src)

    if os.path.isfile(src) and iss3(dst):
        s3_upload(src, dst, client=client)
    elif iss3(src) and not iss3(dst):
        s3_download(src, dst, client=client)
    elif iss3(src) and iss3(dst):
        s3_copy(src, dst, client=client)
    elif os.path.isfile(src) and os.path.isfile(dst):
        shutil.copy2(src, dst)
    
    exts = []
    if src.endswith(".shp"):
        exts = ["shx", "dbf", "prj", "cpg", "mta"]
    elif src.endswith(".tif"):
        exts = [] #["tfw", "jpw", "prj", "aux.xml"]
        
    for ext in exts:
        copy(forceext(src,ext), forceext(dst,ext), client=client)

    return dst

def move(src, dst, client=None):
    """
    move
    """
    dst = dst if dst else tempname4S3(src)

    if os.path.isfile(src) and iss3(dst):
        s3_upload(src, dst, remove_src=True, client=client)
    elif iss3(src) and not iss3(dst):
        s3_download(src, dst, remove_src=True, client=client)
    elif iss3(src) and iss3(dst):
        s3_move(src, dst, client=client)
    elif os.path.isfile(src) and os.path.isfile(dst):
        shutil.move(src, dst)
    
    exts = []
    if src.endswith(".shp"):
        exts = ["shx", "dbf", "prj", "cpg", "mta"]
    elif src.endswith(".tif"):
        exts = ["tfw", "jpw", "prj", "aux.xml"]
        
    for ext in exts:
        move(forceext(src,ext), forceext(dst,ext), client=client)

    return dst