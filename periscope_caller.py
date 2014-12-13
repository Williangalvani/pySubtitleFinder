__author__ = 'will'
try:
    from periscope import periscope
except:
    print """could not call periscope, please download it on the root folder doing "git clone https://github.com/patrickdessalle/periscope.git"""
import sys


def try_download(filepath, languages):
    for language in languages:
        sys.argv = "periscope -l {0}".format(language).split(' ')
        periscope.

