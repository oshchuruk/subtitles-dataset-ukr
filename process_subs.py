import re
import os
import hashlib
import sqlite3
from progress.bar import ChargingBar
from fnmatch import filter

remove_timecodes_re = r"\d+\n\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+\n"
remove_html_tags_re = r"<\s*[^>]*>"
remove_newlines_in_one_sub_re = r"(?<=.)\n(?!\n)"

connection = sqlite3.connect('processed.db')
c = connection.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS processed_srt(id INT PRIMARY KEY, hash TEXT)")


def check_hash_exists_in_db(new_hash):
    result = c.execute("SELECT * FROM processed_srt WHERE hash = '{}'".format(new_hash))
    return bool(result.fetchall())


def add_hash_to_db(new_hash):
    c.execute("INSERT INTO processed_srt VALUES ({},'{}')".format(processed_count, new_hash))
    connection.commit()


def drop_table():
    c.execute("DROP TABLE processed_srt")


def get_max_id():
    result = c.execute("SELECT max(id) FROM processed_srt LIMIT 1")
    try:
        return int(result.fetchone()[0])
    except TypeError:
        return 0


def get_hash(file_as_string):
    hasher = hashlib.md5()
    hasher.update(file_as_string.encode("utf-8"))
    return hasher.hexdigest()


def process_srt(file_to_process):
    file_to_process = re.sub(remove_timecodes_re, "", file_to_process)
    file_to_process = re.sub(remove_newlines_in_one_sub_re, " ", file_to_process)
    file_to_process = re.sub(remove_html_tags_re, "", file_to_process)
    return file_to_process


def get_formatted_id():
    if processed_count < 10:
        return '000' + str(processed_count)
    elif processed_count < 100:
        return '00' + str(processed_count)
    elif processed_count < 1000:
        return '0' + str(processed_count)
    else:
        return str(processed_count)


def create_numbered_dir():
    if processed_count % 100 == 0:
        try:
            os.makedirs("raw/{}".format((processed_count//100) + 1))
        except FileExistsError:
            # directory already exists
            pass


def get_dir_number():
    return str((processed_count // 100) + 1)


drop_table()
create_table()

processed_count = get_max_id()
num_of_files = 0

for path, dirs, files in os.walk("processed"):
    for f in filter(files, '*.json'):
        num_of_files += 1

bar = ChargingBar("Progress", max=num_of_files)
for path, dirs, files in os.walk("unprocessed"):

    for f in filter(files, '*.srt'):
        processed_count += 1

        fullpath = os.path.abspath(os.path.join(path, f))
        file = open(fullpath, "r")
        file_contents = file.read()
        file_hash = get_hash(file_contents)
        # print(file_hash)
        if not check_hash_exists_in_db(file_hash):
            create_numbered_dir()
            new_file = open("raw/{}/{}___{}".format(get_dir_number(), get_formatted_id(), f), "w")
            new_file.write(process_srt(file_contents))
            add_hash_to_db(file_hash)
            # print(process_srt(file_contents))
        else:
            print("{} is already processed".format(f))
        bar.next()
bar.finish()
