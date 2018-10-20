#!/usr/bin/python3.7

"""
This script scrapes data from 
the comment section of a dark web forum:

Need to use Selenium to initially access this page,
then Selenium will back out of this page and 
click on the link to the next forum page

"""
import csv
# import requests
# import pandas as pd  # need to create a csv file without the use of pandas
from bs4 import BeautifulSoup


# noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable
def scraper():
    # parsing html from message board link location
    # page = requests.get('http://oxwugzccvk3dk6tj.onion/tech/index.html')  # hard-coded url for testing only
    # soup = BeautifulSoup(page.text, 'html.parser')

    filepath = '/home/jxdx/Development/darkcrawler/tech.html'
    soup = BeautifulSoup(open(filepath), 'html.parser')

    # try:
    #     if filepath is not None:
    #         html_page = urllib.request.urlopen(filepath)
    # except urllib.error.HTTPError as e:
    #     # print e
    #     print('The server couldn\'t fulfill the request.')
    #     print('Error code: ', e.code)

    # get the title of the message board
    # board_title = soup.head.title.text

    # find the body of the message forum
    # forum_body = soup.find('body', class_='8chan is-not-moderator active-index').find('form', name_='postcontrols')

    thread_topic = soup.find('input')['value']  # WORKS!
    print(thread_topic)  # test stored value

    # containers for the post thread
    comment_board = soup.findAll('div', class_='thread')

    # post_block = comment_board.find('div', class_='post reply body-not-empty')

    # create list to store the scraped data
    # res = []
    block = []
    # names = []
    # times = []
    # numbers = []
    # comments = []

    # extract the contents of each thread
    for post in comment_board:

        comment_name = post.find('span', class_='name').text  # .label.span.text
        print(comment_name)
        # names.append(comment_name)

        comment_time = post.find('time').text
        print(comment_time)
        # times.append(comment_time)

        comment_number = post.find('a', class_='post_no')['id']  # , class_='post_no')  # .text
        print(comment_number)
        # numbers.append(comment_number)

        comment_text = post.find('p', class_='body-line ltr ').text.strip("\n")
        print(comment_text)
        # comments.append(comment_text)

        # data used by csv.DictWriter
        block.append({
                "Topic": thread_topic,
                "Name": comment_name,
                "Time": comment_time,
                "Number": comment_number,
                "Text": comment_text
            })

        # for lines in thread_body:
        #     comment_text = lines.p.text

        # row = [block]
        #
        # if row:
        #     res.append(row)

    field_names = ["Topic", "Name", "Time", "Number", "Text"]
    with open('testout.csv', 'a+', encoding='utf-8') as f:
        writer = csv.DictWriter(f, field_names)

        writer.writeheader()

        for dict_items in block:
            writer.writerow(dict_items)
