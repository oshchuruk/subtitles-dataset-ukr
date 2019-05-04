import sqlite3
import re

get_line_re = r"(?:[A-Z]+ \+\+\+\$\+\+\+ )(.*)"
get_id_re = r"(L\d+)(?= \+\+\+\$\+\+\+ )"

connection = sqlite3.connect('cornell_utterances.db')
c = connection.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS cornell(id TEXT PRIMARY KEY, line TEXT)")


def add_line_to_db(id, line):
    c.execute("INSERT INTO cornell VALUES ('{}',{})".format(id, '"'+line+'"'))

create_table()

file = open("movie_lines.txt", "r",  encoding='utf-8', errors='ignore')
file_string = file.read()
file_string = file_string.replace("\"", "'")
file_string = file_string.replace("\n", "-s-p-l-i-t-")
file_lines = file_string.split("-s-p-l-i-t-")

i=0
for line in file_lines:
    if len(re.findall(get_id_re, line)) > 0 and len(re.findall(get_line_re, line)) > 0:
        line_id = re.findall(get_id_re, line)[0]
        value = re.findall(get_line_re, line)[0]
        add_line_to_db(line_id, value)
        i+=1
        if i % 100 == 0:
            print(str(i) + "\n")
            connection.commit()

connection.close()