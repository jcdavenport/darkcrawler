#!/usr/bin/python3.7

"""
This script scrapes data from 
the comment section of a dark web forum:

header->h1 gets the topic of the forum page


Need to use Selenium to initially access this page,
then Selenium will back out of this page and 
click on the link to the next forum page

"""

import csv
import requests
# import pandas as pd  # need to create a csv file without the use of pandas
from bs4 import BeautifulSoup


# noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable
def scraper():
    # parsing html from message board link location
    page = requests.get('http://oxwugzccvk3dk6tj.onion/tech/index.html')  # hard-coded url for testing only
    soup = BeautifulSoup(page.text, 'html.parser')

    # get the title of the message board
    board_title = soup.find('header').find('h1')

    # Create a file to write to, add headers row
    f = csv.writer(open('test_data.csv', 'w'))
    # f.writerow([board_title])
    f.writerow(['Thread', 'Name', 'Time', 'Number', 'Comment'])

    # find the body of the message forum
    # forum_body = soup.find('body', class_='8chan is-not-moderator active-index').find('form', name_='postcontrols')

    # containers for the post thread
    comment_board = soup.find_all('div', class_='thread')

    post_block = comment_board.find('div', class_='post reply body-not-empty')

    # List to store the scraped data in
    block = []
    # names = []
    # times = []
    # numbers = []
    # comments = []

    # extract the contents of each thread
    for post in post_block:

        comment_name = post.p.label.span.text
        # names.append(comment_name)

        comment_time = post.p.label.time.text
        # times.append(comment_time)

        comment_number = post.p.find('a', class_='post_no').text
        # numbers.append(comment_number)

        comment_text = post.find('div', class_='body').p.text  # .contents[0]
        # comments.append(comment_text)

        # used for writing data in csv.Dict format (not regular csv)
        block.append({
                "Thread": board_title,
                "Name": comment_name,
                "Time": comment_time,
                "Number": comment_number,
                "Text": comment_text
            })

        # for lines in thread_body:
        #     comment_text = lines.p.text

        # row = [thread]
        #
        # if row:
        #     res.append(row)

    field_names = ["Thread", "Name", "Time", "Number", "Text"]
    with open('~/Desktop/testout.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, field_names)

        writer.writeheader()
        writer.writerows(block)

        # Write a header row (dict format)
        # writer.writerow({x: x for x in field_names})
        #
        # for item_property_dict in comment_block:
        #     writer.writerow(item_property_dict)
