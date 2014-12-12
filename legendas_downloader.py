#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import sys
import requests
import os
import shutil
import rarfile

LEGENDAS_SEARCH_PAGE = "http://legendas.tv/util/carrega_legendas_busca/"
LEGENDAS_LOGIN_PAGE = "http://legendas.tv/login"
LEGENDAS_MAIN = "http://legendas.tv"
NAME = "Legendas.tv"

def read_filename(argv):
    if not isinstance(argv,basestring):
        if not argv:
            print "did not get filename!\n" \
                  "Example usage: python legendas_downloader.py American.Dad.S11E02.HDTV.x264-LOL.mp4"
            return
        filename = argv[0]
    else:
        filename = argv
    return os.path.splitext(filename)[0] #removing extension


def read_username_and_password():
    credentials = None
    try:
        with open('passwordLegendasTV.dat') as f:
            credentials = [x.strip().split(':') for x in f.readlines()]
            credentials = credentials[0]
    except:
        with open("passwordLegendasTV.dat", "w") as text_file:
            text_file.write("username:password")
            print "Could not find credentials for legendasTV: make sure there's a file called password.dat and it's contents are right" \
                  "\n The file has now been created automatically."

    if not credentials or credentials[0] == 'username':
        raise Exception("Please fiz user and password!")
    return credentials


def get_download_page(data):
    soup = BeautifulSoup(data)
    divs = soup.find_all('div', {'class': 'f_left'})
    #print "found {0} results".format(len(divs))
    if not len(divs):
        #print "couldn't find anything, aborting"
        raise Exception("Nothing found!")
    #print "using first result"
    url = divs[0].find('a')
    return LEGENDAS_MAIN + url['href']


def get_download_url(data):
    soup = BeautifulSoup(data)
    button = soup.find("button", {'class': 'icon_arrow'})
    js= button['onclick']
    url = js.split("('")[1].split("',")[0]
    download_url = LEGENDAS_MAIN + url
    return download_url


def download_file(url, session, filename):
    response = session.get(url, stream=True)
    with open('{0}.rar'.format(filename), 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


def extract(filename, path):
    rf = rarfile.RarFile(filename+'.rar')
    for f in rf.infolist():
        if filename in f.filename:
            if path:
                rf.extract(f, path)
            else:
                rf.extract(f, filename)

    os.remove(filename+'.rar')


def find_subtitle(argv):
    filepath = read_filename(argv)
    path, filename = os.path.split(filepath)
    username, password = read_username_and_password()

   ## login
    with requests.Session() as s:
        payload = {'data[User][username]': username, 'data[User][password]': password}
        s.post("http://legendas.tv/login", data=payload)

    ### busca:
        req = s.get(LEGENDAS_SEARCH_PAGE + filename)
        url = get_download_page(req.text.encode('utf8'))
        req = s.get(url)
        download_url =get_download_url(req.text)
        download_file(download_url, s, filename)
        extract(filename,path)

def try_download(name, languages):
    try:
        find_subtitle(name)
        return True
    except:
        return False

if __name__ == "__main__":
   find_subtitle(sys.argv[1:])



