__author__ = 'will'
import os
import hashlib
import urllib2


NAME = "SubDB"

def get_hash(name):
    readsize = 64 * 1024
    with open(name, 'rb') as f:
        size = os.path.getsize(name)
        data = f.read(readsize)
        f.seek(-readsize, os.SEEK_END)
        data += f.read(readsize)
    return hashlib.md5(data).hexdigest()


def try_download(fileName,languages):
    # Put the code in a try catch block in order to continue for other video files, if it fails during execution
    for language in languages:
        try:
            hash = get_hash(fileName)

            headers = { 'User-Agent' : 'SubDB/1.0 (subtitle-downloader/1.0; https://github.com/Williangalvani/PyLTVdownloader)' }
            url = "http://api.thesubdb.com/?action=download&hash=" + hash + "&language={0}".format(language)
            req = urllib2.Request(url, '', headers)
            response = urllib2.urlopen(req).read()

            with open (fileName + ".srt", "wb" ) as subtitle:
                subtitle.write(response)
            print "got subtitle: lang: " + language
            return True
        except:
            pass
    return False