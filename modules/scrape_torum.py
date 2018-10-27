#!/usr/bin/python3.7

"""
This script scrapes data from 
the comment section of a dark web forum:

Need to use Selenium to initially access this page,
then Selenium will back out of this page and 
click on the link to the next forum page

"""
import csv
# import re
import requests
# import pandas as pd  # need to create a csv file without the use of pandas
from bs4 import BeautifulSoup


def concatenate_list_data(list_data):
    result = ''
    for element in list_data:
        result += str(element)
    return result


# noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable
def torum():
    # parsing html from message board link location
    # page = requests.get('http://oxwugzccvk3dk6tj.onion/n/index.html')  # hard-coded url for testing only
    # soup = BeautifulSoup(page.text, 'html.parser')

    # for testing with local file
    filepath = '/home/jxdx/Development/darkcrawler/targets/torum_intel_exchange_multi_cve.html'
    soup = BeautifulSoup(open(filepath), 'html.parser')

    # try:
    #     if filepath is not None:
    #         html_page = urllib.request.urlopen(filepath)
    # except urllib.error.HTTPError as e:
    #     # print e
    #     print('The server couldn\'t fulfill the request.')
    #     print('Error code: ', e.code)

    # >>>>>>>Add some magic here to search for specific thread topics.<<<<<<<<<<

    forum_name = soup.find('h1').text
    print(forum_name)

    forum_topic = soup.find('h2', class_='topic-title').a.text
    print(forum_topic)  # test stored value

    try:
        forum_page = soup.find('li', class_='active').span.text
        print(forum_page)
    except:
        forum_page = "N/A"
        print(forum_page)

    forum_body = soup.find('div', id='page-body')

    # containers for the post thread
    forum_comments = forum_body.findAll('div', class_='postbody')  # {'id': re.compile(r'p')})

    # create list to store the scraped data
    # res = []
    # concat = " "
    # concat_ltr = " "
    block = []

    # extract the contents of each thread
    for post in forum_comments:

        comment_name = post.find('p', class_='author').text  # .label.span.text
        print(comment_name)
        # names.append(comment_name)

        comment_post = post.find('div', class_='content').text
        print(comment_post)
        # times.append(comment_post)

        # comment_number = post.find('a', class_='post_no')['id']  # , class_='post_no')  # .text
        # print(comment_number)
        #
        # post_op = post.find('div', class_='post op has-file body-not-empty').find('div', class_='body').contents
        #
        # for post_ltr in post_op:
        #     try:
        #         concat = concatenate_list_data(post_ltr.text.strip())
        #         concat_ltr = "".join(concat)
        #         print(concat_ltr)
        #     except:  # Ignore this error for now
        #         pass

        # row = [concat_ltr]
        # if row:
        #     res.append

        # data used by csv.DictWriter (easily scalable)
        block.append({
            "Forum": forum_name,
            "Topic": forum_topic,
            "Page": forum_page,
            "User_Data": comment_name.strip(),
            "Comment": comment_post.strip(),
            # "Number": comment_number,
            # "Thread_Post": concat_ltr
        })

    field_names = ["Forum", "Topic", "Page", "User_Data", "Comment"]
    with open('torum_data.csv', 'a+', newline='', encoding='utf-8') as f:
        writer1 = csv.DictWriter(f, field_names)

        writer1.writeheader()

        for dict_items in block:
            writer1.writerow(dict_items)
