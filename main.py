#!/usr/bin/env python2
import sys
import random
import requests
import markovify
from bs4 import BeautifulSoup
from yourewinner import Forum

MODES = ("markov", "laughingcolour")

forum = Forum()
forum.login("b", "123456")

if not forum.logged_in:
    print "b was unable to login!"
    sys.exit(1)

mode = random.choice(MODES)
if mode == "markov":
    # choose a random board to get data from
    boards = []
    for cat in forum.get_board_index():
        boards.extend([f["forum_id"] for f in cat["child"]])
    board = random.choice(boards)

    # collect data from 1000 topics
    text = ""
    for b in forum.get_board(board, page=1, page_size=1000):
        t = forum.get_topic(b["topic_id"])
        for p in t["posts"]:
            text += p["post_content"].data + "\n"

    m = markovify.Text(text)
    message = ""
    for i in range(2):
        message += m.make_sentence(tries=100) + " "
elif mode == "laughingcolour":
    url = "http://laughingcolours.com/page/%s" % random.randint(1, 100)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    section = random.choice(soup.find_all("div", class_="section-heading"))
    title = section.h2.a.string
    img = "[img]" + section.find(class_="img-thumbnail")["src"] + "[/img]"
    #translation = "\n\n".join(s.string for s in section.find_all(class_="margint10"))
    message = "\n\n".join([title, img]).encode("utf-8")
else:
    sys.exit(1)

# choose a topic to reply to
topic = random.choice(forum.get_recent())
print topic["forum_id"], topic["topic_id"], topic["topic_title"]
print message
forum.reply(topic["forum_id"], topic["topic_id"], topic["topic_title"].data, message)
