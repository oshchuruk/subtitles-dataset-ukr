# -*- coding: utf-8 -*-

import json
import os
import random
from progress.bar import ChargingBar
from fnmatch import filter

# processed_count = 0
# num_of_files = 0
#
# for path, dirs, files in os.walk("processed"):
#     for f in filter(files, '*.json'):
#         num_of_files += 1
#
# train_from = open("new_data/train.from", "w", encoding="utf-8")
# train_to = open("new_data/train.to", "w", encoding="utf-8")
#
# tst2012_from = open("new_data/tst2012.from", "w", encoding="utf-8")
# tst2012_to = open("new_data/tst2012.to", "w", encoding="utf-8")
#
# tst2013_from = open("new_data/tst2013.from", "w", encoding="utf-8")
# tst2013_to = open("new_data/tst2013.to", "w", encoding="utf-8")

# bar = ChargingBar("Progress", max=num_of_files)
for path, dirs, files in os.walk("processed"):

    for f in filter(files, '*.json'):
        # processed_count += 1

        fullpath = os.path.abspath(os.path.join(path, f))
        file = open(fullpath, "r")
        file_string = file.read()
        file_convos = json.loads(file_string.encode("utf-8"))

        total_length = len(file_convos["conversations"])

        newfile = open("new_data/15/{}".format(fullpath[fullpath.rfind("/")+1:]), "w", encoding="utf-8")

        previous_element = ""
        for element in file_convos["conversations"]:

            if previous_element != "":
                if previous_element["to"] != element["from"]:
                    newfile.write(element["from"] + "\n")

            newfile.write(element["to"] + "\n")


            previous_element = element

                # train_to.write(element["to"] + "\n")
            # else:
            #     tst2012_from.write(element["from"] + "\n")
            #     tst2012_to.write(element["to"] + "\n")
            #
            #     tst2013_from.write(element["from"] + "\n")
            #     tst2013_to.write(element["to"] + "\n")


#         bar.next()
# bar.finish()
