#!/usr/bin/env python2
import sys
from markovify import Text
from random import choice
from yourewinner import Forum

forum = Forum()
forum.login("b", "123456")

if not forum.logged_in:
    print "b was unable to login!"
    sys.exit(1)

# choose a random board to get data from
boards = []
for cat in forum.get_board_index():
    boards.extend([f["forum_id"] for f in cat["child"]])
board = choice(boards)

# collect data from 500 topics
text = ""
for b in forum.get_board(board, page=1, page_size=1000):
    t = forum.get_topic(b["topic_id"])
    for p in t["posts"]:
        text += p["post_content"].data + "\n"

m = Text(text)
message = ""
for i in range(2):
    message += m.make_sentence(tries=100)

# choose a topic to reply to
topic = choice(forum.get_recent())
print topic["forum_id"], topic["topic_id"], topic["topic_title"]
print message
forum.reply(topic["forum_id"], topic["topic_id"], topic["topic_title"].data, message)
