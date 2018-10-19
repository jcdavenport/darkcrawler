#!/usr/bin/python3.7

import os
import sys
# import urllib2
from urllib.request import Request, urlopen
from modules.scrape_obj import scraper
# Input links from file and extract them into path/files


def cinex(website, inputfile, outpath):
    try:
        f = open(inputfile, 'r')
        # print f
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e + "\n## Can't open " + inputfile)

    for line in f:

        # Generate name for every file
        pagename = line.rsplit('/', 1)
        clpagename = str(pagename[1])
        clpagename = clpagename[:-1]
        if len(clpagename) == 0:
            outputFile = "index.htm"
        else:
            outputFile = clpagename

        # Extract page to file
        try:
            f = open(outpath + "/" + outputFile, 'w')
            f.write(urlopen(line).read())
            f.close()
            print("## File created on " + os.getcwd() +
                  "/" + outpath + "/" + outputFile)
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e + "\n Can't write on file " + outputFile)


# Input links from file and extract them into terminal


def intermex(inputFile):
    try:
        f = open(inputFile, 'r')
        for line in f:
            print(urlopen(line).read())
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e + "\n## Not valid file")


# Output webpage into a file


def outex(website, outputFile, outpath):
    # Extract page to file
    try:
        scraper()

        outputFile = outpath + "/" + outputFile
        f = open(outputFile, 'w')
        f.write(urlopen(website).read().decode('utf-8'))
        f.close()
        print("## File created on " + os.getcwd() + "/" + outputFile)

    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e + "\n Can't write on file " + outputFile)


# Ouput webpage into terminal

def termex(website):
    try:
        print(urlopen(website).read())
    except:
        e = sys.exc_info()[0]
        print("Error: %s" %
              e + "\n## Not valid URL \n## Did you forget \'http://\'?")


def extractor(website, crawl, outputFile, inputFile, outpath, verbose):
    if len(inputFile) > 0:
        if crawl:
            cinex(website, inputFile, outpath)
        # TODO: Extract from list into a folder
        # elif len(outputFile) > 0:
        # inoutex(website, inputFile, outputFile)
        else:
            intermex(inputFile)
    else:
        if len(outputFile) > 0:
            outex(website, outputFile, outpath)
        else:
            termex(website)

        # TODO: Return output to torcrawl.py
