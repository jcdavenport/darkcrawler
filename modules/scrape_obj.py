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


def scraper():
    # parsing html from message board link location
    page = requests.get('http://oxwugzccvk3dk6tj.onion/tech/index.html')  # don't use hard-coded url
    soup = BeautifulSoup(page.text, 'html.parser')

    # get the title of the message board
    board_title = soup.find('header').find('h1')

    # Create a file to write to, add headers row
    f = csv.writer(open('test_data.csv', 'w'))
    # f.writerow([board_title])
    f.writerow(['Thread Data' + board_title])

    # find the body of the message forum
    forum_body = soup.find('body', attrs={'class': '8chan is-not-moderator active-index'}).find('form', attrs={
        'name': 'postcontrols'})  # .find('form', name='postcontrols')  #('class="8chan is-not-moderator active-index')

    # the important data is within the thread class
    message_board = forum_body.find_all('div', attrs={'class': 'thread'})  # class_='thread')

    res = []

    # extract the contents of each thread
    for thread in message_board:
        thread_data = thread.find_all('p', attrs={'class': 'intro'})
        comment_name = thread_data.find('span', attr={'class': 'name'}).text.strip()
        comment_time = thread_data.find('time').text.strip()
        comment_number = thread_data.find('a', attr={'class': 'post_no'}).text.strip()
        thread_body = thread.find('div', attrs={'class': 'body'}).contents[0]
        row = [thread]
        if row:
            res.append(row)

    field_names = ["Name", "Time", "Number", "Text"]
    with open("~/Desktop/testout.csv", "w") as f:
        writer = csv.DictWriter(f, field_names)

        comment_block = [
            {
                "Name": "comment_name",
                "Time": "comment_time",
                "Number": "comment_number",
                "Text": "thread_body"
            },
            ...
        ]

        # Write a header row
        writer.writerow({x: x for x in field_names})

        for item_property_dict in comment_block:
            writer.writerow(item_property_dict)

    # df = pd.DataFrame(res, columns=["Name", "Time", "Number", "Comment"])

    # # export to csv file: method 1
    # f.writerow(df)

    # # export to csv file: method 2
    # export_csv = df.to_csv(r'/home/jxdx/working/export_df.csv', index=None, header=True)

    # # output the data frame to terminal
    # print(df)

    """
      comment_name = comment_block.find('span', class_='name').text
      comment_time = comment_block.find('time').text.strip()
      comment_number = comment_block.find('a', class_='post_no').text.strip()
      comment_body = comment_block.find_all('p', class_='body-line ltr ').text
    
    
    
    field_names = ["Name", "Time", "Number", "Text"]
    with open("~/Desktop/testout.csv", "w") as f:
        writer = csv.DictWriter(f, field_names)
    
        # comment_block = [
        #   {
        #       "Name": "comment_name",
        #       "Time": "comment_time",
        #       "Number": "comment_number",
        #       "Text": "comment_body"
        #   },
        #   ...
        # ]
    
        # Write a header row
        writer.writerow({x: x for x in field_names})
    
        for item_property_dict in comment_block:
            writer.writerow(item_property_dict)
    """