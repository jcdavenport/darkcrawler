#!/usr/bin/python3.7

# import os
import sys
import re
# import urllib2
import urllib.request
import urllib.error
# import time
# from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd  # added


# Exclude links that we dont need
def excludes(link, website, outpath):
    # BUG: For NoneType Exceptions, got to find a solution here
    if link is None:
        return True
    # #links
    elif '#' in link:
        return True
    # External links
    elif link.startswith('http') and not link.startswith(website):
        lstfile = open(outpath + '/extlinks.txt', 'w+')
        lstfile.write(link + "\n")
        lstfile.close()
        return True
    # Telephone Number
    elif link.startswith('tel:'):
        lstfile = open(outpath + '/telephones.txt', 'w+')
        lstfile.write(link.encode('utf-8') + "\n")
        lstfile.close()
        return True
    # Mails
    elif link.startswith('mailto:'):
        lstfile = open(outpath + '/mails.txt', 'w+')
        lstfile.write(link + "\n")
        lstfile.close()
        return True
    # Type of files
    elif re.search('^.*\.(pdf|jpg|jpeg|png|gif|doc)$', link, re.IGNORECASE):
        return True


# Canonization of the link
def canonical(link, website):
    # Already formatted
    if link.startswith(website):
        return link
    # For relative paths with / infront
    elif link.startswith('/'):
        if website[-1] == '/':
            final_link = website[:-1] + link
        else:
            final_link = website + link
        return final_link
    # For relative paths without /
    elif re.search('^.*\.(html|htm|aspx|php|doc|css|js|less)$', link, re.IGNORECASE):
        # Pass to
        if website[-1] == '/':
            final_link = website + link
        else:
            final_link = website + "/" + link
        return final_link
        # Clean links from '?page=' arguments


# Core of crawler
# noinspection PyUnboundLocalVariable
def crawler(website, cdepth, cpause, outpath, logs, verbose):
    lst = set()
    ordlst = []
    ordlst.insert(0, website)
    ordlstind = 0
    # idx = 0

    if logs is True:
        logfile = open(outpath + '/log.txt', 'w+')

    print("## Crawler Started from " + website + " with step " + str(cdepth) + " and wait " + str(cpause))

    # Depth
    for x in range(0, int(cdepth)):

        # For every element of list
        for item in ordlst:

            # Check if is the first element
            if ordlstind > 0:
                try:
                    if item is not None:
                        html_page = urllib.request.urlopen(item)
                except urllib.error.HTTPError as e:
                    # print e
                    print('The server couldn\'t fulfill the request.')
                    print('Error code: ', e.code)
            else:
                html_page = urllib.request.urlopen(website)
                ordlstind += 1

            soup = BeautifulSoup(html_page, "html5lib")

            table = soup.find('table', {'class': 'board-list-table'})
            table_rows = table.find_all('tr')

            res = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [tr.text.strip() for tr in td if tr.text.strip()]
                if row:
                    res.append(row)

            df = pd.DataFrame(res, columns=["uri", "title", "pph", "active", "tags", "posts_total"])
            print(df)

            # For each <a href=""> tag
            for link in soup.findAll('a'):
                link = link.get('href')

                if excludes(link, website, outpath):
                    continue

                verlink = canonical(link, website)
                lst.add(verlink)

            # TODO: For each <img src="">
            # for img in soup.findAll('img')
            #   img = link.get('src')
            #   if imgexludes(link, website)
            #     continue
            #
            #   verlink = imgcanonical(link, website)
            #   lst.add(verlink)

            # TODO: For each <script src="">
            # for link in soup.findAll('script'):
            #   link = link.get('src')
            #
            #   if screxcludes(link, website):
            #     continue
            #
            #   verlink = scrcanonical(link, website)
            #   lst.add(verlink)

            # Pass new on list and re-set it to delete duplicates
            ordlst = ordlst + list(set(lst))
            ordlst = list(set(ordlst))

            if verbose is True:
                sys.stdout.write("-- Results: " + str(len(ordlst)) + "\r")
                sys.stdout.flush()

            # Pause time
            """
            if (ordlst.index(item) != len(ordlst)-1) and cpause > 0:
              time.sleep(float(cpause))
            """

            # Keeps logs for every webpage visited
            if logs is True:
                logfile.write("%s\n" % item)

        print("## Step " + str(x + 1) + " completed with: " + str(len(ordlst)) + " results")

    if logs is True:
        logfile.close()

    ordlst.sort()
    return ordlst
