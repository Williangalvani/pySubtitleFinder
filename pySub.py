__author__ = 'will'

import os
import legendas_downloader
import subdb_downloader
import periscope_caller

DIRECTORIES = ["/home/mari/complete", "/path/to/your/video/files2"]

MOVIE_EXTS = [".avi",".mp4",".mkv",".mpg",".mpeg",".mov",".rm",".vob",".wmv",".flv",".3gp"]
SUBS_EXTS = ['.srt', '.sub']

downloaders = [legendas_downloader,
               subdb_downloader]

languages = ['en',]

def get_movie_files(rootdir, with_subs=False):
    filelist = []
    for root, subfolders, files in os.walk(rootdir):
        for file in files:
            name, ext = os.path.splitext(file)
            if ext in MOVIE_EXTS:
                if with_subs == has_subs(root, name):
                    filelist.append(os.path.join(root, file))
    return filelist

def has_subs(root, name):
    for ext in SUBS_EXTS:
        filename = os.path.join(root, name + ext)
        if os.path.isfile(filename):
            return True
    return False


def find_all_files():
    lists = [get_movie_files(dir) for dir in DIRECTORIES]
    filelist = []
    for list in lists:
        filelist.extend(list)
    return filelist

all_files= find_all_files()
print all_files

downloaders_done = []
downloader_number = 0

while len(all_files) and len(downloaders_done) < len(downloaders):
    current_downloader = downloaders[downloader_number]
    for file in all_files:
        print "file:", file,
        if current_downloader.try_download(file, languages):
            print "Found on ", current_downloader.NAME
            all_files.remove(file)
        else:
            print "Not found on " + current_downloader.NAME
    downloader_number += 1
    downloaders_done.append(current_downloader)

