#!/usr/bin/python3.7

import sys
import re
import subprocess
import os
from urllib.request import urlopen
# from urllib.error import URLError
from json import load


# Canonicalization of URL
def urlcanon(website, verbose):
    if not website.startswith("http"):
        if not website.startswith("www."):
            website = "www." + website
            if verbose:
                print("## URL fixed: " + website)
        website = "http://" + website
        if verbose:
            print("## URL fixed: " + website)
    return website


# Create output path
# noinspection PyUnusedLocal
def folder(website, verbose):
    if website.startswith('http'):
        outpath = website.replace("http://", "")
    if website.startswith('https'):
        outpath = website.replace("https://", "")
    else:
        outpath = website
    if outpath.endswith('/'):
        outpath = outpath[:-1]
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    if verbose:
        print("## Folder created: " + outpath)
    return outpath


# Check if TOR service is running
# noinspection PyShadowingNames
def check_tor(verbose):
    check_tor = subprocess.check_output(['ps', '-e'])

    def find_whole_word(w):
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

    if find_whole_word('tor')(check_tor.decode('utf-8')):
        if verbose:
            print("## TOR is ready!")
    else:
        print("## TOR is NOT running!")
        print('## Enable tor with \'service tor start\' or add -w argument')
        sys.exit(2)


# Check your IP from external website
# noinspection PyPep8Naming,PyUnboundLocalVariable
def checkIP():
    try:
        web_ip_check = 'https://api.ipify.org/?format=json'
        my_ip = load(urlopen(web_ip_check))['ip']
        print('## Your IP: ' + my_ip)
    except Exception as e:
        # e = sys.exc_info()[0]
        print("Error: %s" % e + "\n## IP can't obtain \n## Is " + web_ip_check + "up?")
