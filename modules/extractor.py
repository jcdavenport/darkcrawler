#!/usr/bin/python3.7

import os
# import sys
# import urllib2
from urllib.request import urlopen
from modules.scrape_obj import scraper
# Input links from file and extract them into path/files


# noinspection PyUnboundLocalVariable,PyUnusedLocal
def cinex(website, inputfile, outpath):
    try:
        f = open(inputfile, 'r')
        # print f
    except Exception as e:
        # e = sys.exc_info()[0]
        print("Error: %s" % e + "\n## Can't open " + inputfile)

    for line in f:

        # Generate name for every file
        pagename = line.rsplit('/', 1)
        clpagename = str(pagename[1])
        clpagename = clpagename[:-1]
        if len(clpagename) == 0:
            outputfile = "index.htm"
        else:
            outputfile = clpagename

        # Extract page to file
        try:
            f = open(outpath + "/" + outputfile, 'w')
            f.write(urlopen(line).read())
            f.close()
            print("## File created on " + os.getcwd() +
                  "/" + outpath + "/" + outputfile)
        except Exception as e:
            # e = sys.exc_info()[0]
            print("Error: %s" % e + "\n Can't write on file " + outputfile)


# Input links from file and extract them into terminal


def intermex(inputfile):
    try:
        f = open(inputfile, 'r')
        for line in f:
            print(urlopen(line).read())
    except Exception as e:
        # e = sys.exc_info()[0]
        print("Error: %s" % e + "\n## Not valid file")


# Output webpage into a file


def outex(website, outputfile, outpath):
    # Extract page to file
    try:
        scraper()

        outputfile = outpath + "/" + outputfile
        f = open(outputfile, 'w')
        f.write(urlopen(website).read().decode('utf-8'))
        f.close()
        print("## File created on " + os.getcwd() + "/" + outputfile)

    except Exception as e:
        # e = sys.exc_info()[0]
        print("Error: %s" % e + "\n Can't write on file " + outputfile)


# Ouput webpage into terminal

def termex(website):
    try:
        print(urlopen(website).read())
    except Exception as e:
        # e = sys.exc_info()[0]
        print("Error: %s" %
              e + "\n## Not valid URL \n## Did you forget \'http://\'?")


# noinspection PyUnusedLocal
def extractor(website, crawl, outputfile, inputfile, outpath, verbose):
    if len(inputfile) > 0:
        if crawl:
            cinex(website, inputfile, outpath)
        # TODO: Extract from list into a folder
        # elif len(outputFile) > 0:
        # inoutex(website, inputFile, outputFile)
        else:
            intermex(inputfile)
    else:
        if len(outputfile) > 0:
            outex(website, outputfile, outpath)
        else:
            termex(website)

        # TODO: Return output to torcrawl.py
