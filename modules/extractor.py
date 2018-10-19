#!/usr/bin/python3.7

import os
import sys
# import urllib2
import requests  # added
import pandas as pd  # added
import csv  # added
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


# Input links from file and extract them into path/files


def cinex(website, inputFile, outpath):
    try:
        f = open(inputFile, 'r')
        # print f
    except:
        e = sys.exc_info()[0]
        print("Error: %s" % e + "\n## Can't open " + inputFile)

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
    # START TEST BLOCK
    # parsing html from message board link location
    # don't use hard-coded url(just for testing)
    page = requests.get('http://oxwugzccvk3dk6tj.onion/tech/index.html')

    soup = BeautifulSoup(page.text, 'html.parser')

    # get the title of the message board
    board_title = soup.find('header').find('h1')

    # Method1: Create a file to write to, add headers row
    f_test1 = csv.writer(open('/home/jxdx/working/test_data.csv', 'w'))
    # f.writerow([board_title])
    f_test1.writerow(['Thread Data' + board_title])

    # find the body of the message forum
    # .find('form', name='postcontrols')  #('class="8chan is-not-moderator active-index')
    forum_body = soup.find('body', attrs={
        'class': '8chan is-not-moderator active-index'}).find('form', attrs={'name': 'postcontrols'})

    # the important data is within the thread class
    message_board = forum_body.find_all(
        'div', attrs={'class': 'thread'})  # class_='thread')

    res = []

    # extract the contents of each thread
    for thread in message_board:
        thread_data = thread.find_all('p', attrs={'class': 'intro'})  # contents[0]
        comment_name = thread_data.find(
            'span', attr={'class': 'name'}).text.strip()
        comment_time = thread_data.find('time').text.strip()
        comment_number = thread_data.find(
            'a', attr={'class': 'post_no'}).text.strip()
        thread_body = thread.find('div', attrs={'class': 'body'}).contents[0]
        row = [thread]
        if row:
            res.append(row)

    df = pd.DataFrame(res, columns=[comment_name, comment_time, comment_number, thread_body])

    # export to csv file: method 1
    f_test1.writerow(df)

    # export to csv file: method 2
    export_csv = df.to_csv(
        r'/home/jxdx/working/export_df.csv', index=None, header=True)

    export_csv

    # output the data frame to terminal
    # print (df)


 # END TEST BLOCK

    # Extract page to file
    try:
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
