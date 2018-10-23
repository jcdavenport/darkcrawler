#!/usr/bin/python3.7

"""
This script scrapes data from 
the comment section of a dark web forum:

Need to use Selenium to initially access this page,
then Selenium will back out of this page and 
click on the link to the next forum page

ONLY RETURNS 1 PAGE OF COMMENTS (15 lines)

"""
import csv
import requests
# import pandas as pd  # need to create a csv file without the use of pandas
from bs4 import BeautifulSoup


def concatenate_list_data(list_data):
    result = ''
    for element in list_data:
        result += str(element)
    return result


# noinspection PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable,PyUnboundLocalVariable
def scraper():
    # parsing html from message board link location
    # page = requests.get('http://oxwugzccvk3dk6tj.onion/n/index.html')  # hard-coded url for testing only
    # soup = BeautifulSoup(page.text, 'html.parser')

    # for testing with local file
    filepath = '/home/jxdx/Development/darkcrawler/tech.html'
    soup = BeautifulSoup(open(filepath), 'html.parser')

    # try:
    #     if filepath is not None:
    #         html_page = urllib.request.urlopen(filepath)
    # except urllib.error.HTTPError as e:
    #     # print e
    #     print('The server couldn\'t fulfill the request.')
    #     print('Error code: ', e.code)

    # >>>>>>>Add some magic here to search for specific thread topics.<<<<<<<<<<

    thread_topic = soup.find('input')['value']
    print(thread_topic)  # test stored value

    # containers for the post thread
    comment_thread = soup.findAll('div', class_='thread')

    # create list to store the scraped data
    # res = []
    # concat = " "
    concat_ltr = " "
    block = []

    # extract the contents of each thread
    for post in comment_thread:

        comment_name = post.find('span', class_='name').text  # .label.span.text
        print(comment_name)
        # names.append(comment_name)

        comment_time = post.find('time').text
        print(comment_time)
        # times.append(comment_time)

        comment_number = post.find('a', class_='post_no')['id']  # , class_='post_no')  # .text
        print(comment_number)

        post_op = post.find('div', class_='post op has-file body-not-empty').find('div', class_='body').contents

        for post_ltr in post_op:
            try:
                concat = concatenate_list_data(post_ltr.text.strip())
                concat_ltr = "".join(concat)
                print(concat_ltr)
            except:  # Ignore this error for now
                pass

            # row = [concat_ltr]
            # if row:
            #     res.append

        # data used by csv.DictWriter (easily scalable)
        block.append({
            "Topic": thread_topic,
            "Name": comment_name,
            "Time": comment_time,
            "Number": comment_number,
            "Thread_Post": concat_ltr
        })

    field_names = ["Topic", "Name", "Time", "Number", "Thread_Post"]
    with open('tester.csv', 'w+', encoding='utf-8') as f:  # testout.csv, a+
        writer1 = csv.DictWriter(f, field_names)

        writer1.writeheader()

        for dict_items in block:
            writer1.writerow(dict_items)
