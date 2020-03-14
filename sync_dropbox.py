###syncs files with dropbox


"""Upload the contents of your Downloads folder to Dropbox.
This is an example app for API v2.
"""

from __future__ import print_function
from stopwatch import stopwatch

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import dropbox


if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression



# OAuth2 access token.  Gotten from https://www.dropbox.com/developers/apps/
#TOKEN = '46VewxPM5dAAAAAAAAABOsYwQr91IXUUrML0TuFHuiBUUF8RfzIOFV_wZ9ZObekq'

# Get directory the python script is in
dir_path = os.path.dirname(os.path.realpath(__file__))

#these are variables named
#can be called later with args = parser.parse_args()
#then args.folder for example
parser = argparse.ArgumentParser(description='Sync /videos to Dropbox')
parser.add_argument('folder', nargs='?', default='Videos', #folder in dropbox wanted to download into 
                    help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default=dir_path,
                    help='Local directory to upload')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')

def main(TOKEN):
    """Main program.
    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    args = parser.parse_args()
    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    #if an access token doesn't exist, say it's needed
    if not TOKEN:
        print('--token is mandatory')
        sys.exit(2)

    folder = args.folder #in this case, Video
    rootdir = os.path.expanduser(args.rootdir)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a folder on your filesystem')
        sys.exit(1)
    
    #this is the access key
    dbx = dropbox.Dropbox(TOKEN, timeout = None)
    #this is for combined videos: they'll be skippped
    #combined_vids = ["_FF","_CH","_CB","_SL","_FT"]
    #walks down 
    for dn, dirs, files in os.walk(rootdir):
    #for folder in os.listdir(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files.
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
                #if it's not an instance, instantiate name.decode as name of the file
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            #these are the skipped files with comments: temp files, generated files, python scripts, combined videos
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            elif name.endswith('.py'): 
                print('Skipping python script:', name)
            #skip the larger videos, otherwise you get requests.exceptions.ConnectionError: ('Connection aborted.', timeout('The write operation timed out',))
##            elif name.endswith(("_FF.mp4","_CH.mp4","_CB.mp4","_SL.mp4","_FT.mp4", "_FF_1.mp4","_CH_1.mp4","_CB_1.mp4","_SL_1.mp4","_FT_1.mp4")):
##                print('Skipping combined video:', name)
                
            #this part is for getting the last time the file was modified and if it needs changing or not
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname) #last time the file was modified
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                #this was where downloading functionality was in case you want to download vids you don't have from dropbox. Can be added again later
                else:
                    print(name, 'has changed since last sync')
                    #if yesno('Refresh %s' % name, False, args):
                    upload(dbx, fullname, folder, subfolder, name,
                           overwrite=True)
            ####This is the key to uplaoding file by file or all at once
            #elif yesno('Upload %s' % name, True, args): comment this back in if you want to be able to pick individual files you want
            elif name.endswith(".mp4"):
                upload(dbx, fullname, folder, subfolder, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            #these two elif and else need to be ammended if you don't want to stop for a y/n at every directory
                #comment these back in if you want to select which directories you want
            #elif yesno('Descend into %s' % name, True, args):
                #keep.append(name)
                #print('Keeping directory:', name)
            else:
                keep.append(name)
            #else:
                #print('OK, skipping directory:', name)
        #creates shallow copy of keep; or maybe it applies keep to directories?
        dirs[:] = keep

def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('listing %s' % subfolder, "listed folder"):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv
    
#download fucntionality not used in this script
def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('downloading', "download"):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data

def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname) # used to get the time of last modification of the specified path
    #opens file in rb mode
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('uploading %s' % name,'upload %d bytes' % len(data)):
        try:
            #uploads data file to path
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res





##if __name__ == '__main__':
##    main(TOKEN)
##    

