import json
import os
import random
from progress.bar import ChargingBar
from fnmatch import filter

processed_count = 0
num_of_files = 0

for path, dirs, files in os.walk("processed"):
    for f in filter(files, '*.json'):
        num_of_files += 1

bar = ChargingBar("Progress", max=num_of_files)
for path, dirs, files in os.walk("processed"):

    for f in filter(files, '*.json'):
        processed_count += 1

        fullpath = os.path.abspath(os.path.join(path, f))
        file = open(fullpath, "r")
        file_string = file.read()
        file_convos = json.loads(file_string.encode("utf-8"))

        train_from = open("new_data/train.from", "w")
        train_to = open("new_data/train.to", "w")

        tst2012_from = open("new_data/tst2012.from", "w")
        tst2012_to = open("new_data/tst2012.to", "w")

        tst2013_from = open("new_data/tst2013.from", "w")
        tst2013_to = open("new_data/tst2013.to", "w")

        total_length = len(file_convos["conversations"])

        test_elements = []
        if int(total_length*0.001) < 10:
            for n in range(0, 10):
                test_elements.append(int(random.uniform(0, total_length)))
        else:
            for n in range(0, int(total_length*0.001)):
                test_elements.append(int(random.uniform(0, total_length)))
        elements_read = 0
        for element in file_convos["conversations"]:
            if elements_read not in test_elements:
                train_from.write(element["from"] + "\n")
                train_to.write(element["to"] + "\n")
            else:
                tst2012_from.write(element["from"] + "\n")
                tst2012_to.write(element["to"] + "\n")

                tst2013_from.write(element["from"] + "\n")
                tst2013_to.write(element["to"] + "\n")

            elements_read += 1

        bar.next()
bar.finish()
