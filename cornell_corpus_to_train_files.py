# -*- coding: utf-8 -*-
import sqlite3
import re
import random

get_id_re = r"L\d+"

train_from = open("cornell_new_data/train.from", "w", encoding="utf-8")
train_to = open("cornell_new_data/train.to", "w", encoding="utf-8")

tst2012_from = open("cornell_new_data/tst2012.from", "w", encoding="utf-8")
tst2012_to = open("cornell_new_data/tst2012.to", "w", encoding="utf-8")

tst2013_from = open("cornell_new_data/tst2013.from", "w", encoding="utf-8")
tst2013_to = open("cornell_new_data/tst2013.to", "w", encoding="utf-8")

connection = sqlite3.connect('cornell_utterances.db')
c = connection.cursor()


def get_line_from_db(id):
    c.execute("SELECT line FROM cornell WHERE id = '{}'".format(id))
    result = c.fetchone()
    print(id, result)
    return result[0]


file = open("movie_conversations.txt", "r",  encoding='utf-8', errors='ignore')
file_string = file.read()
file_string = file_string.replace("\n", "-s-p-l-i-t-")
file_lines = file_string.split("-s-p-l-i-t-")

convos = []
for line in file_lines:
    convo = re.findall(get_id_re, line)
    if len(convo) > 0:
        convos.append(convo)

c_count = len(convos)
test_elements = []
for n in range(0, 200):
    test_elements.append(int(random.uniform(0, c_count)))

i = 0
for item in convos:
    pair_num = 0
    while pair_num != len(item)-1:
        try:
            question = get_line_from_db(item[pair_num])
            response = get_line_from_db(item[pair_num+1])

            if i in test_elements:
                train_from.write(question + "\n")
                train_to.write(response + "\n")
            else:
                tst2012_from.write(question + "\n")
                tst2012_to.write(response + "\n")

                tst2013_from.write(question + "\n")
                tst2013_to.write(response + "\n")
            pair_num += 1
            i += 1
        except TypeError:
            pair_num += 1
            i += 1
            continue
