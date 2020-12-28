import os, subprocess
from datetime import datetime
from subprocess import PIPE

small_letters = list(map(chr, range(ord('a'), ord('z')+1))) + ['å','ä','ö']
big_letters = list(map(chr, range(ord('A'), ord('Z')+1))) + ['Å','Ä','Ö']
digits = list(map(chr, range(ord('0'), ord('9')+1)))
symbols = small_letters + big_letters + digits

start_time = datetime.now()
path = "/scratch/project_2003685/suomi24-2001-2017-vrt-v1-1/vrt/"
print("Start:", start_time)
total_word_count = 0
for filename in os.listdir(path):
    file_word_count = 0
    print(filename)
    wc_output = subprocess.run(
            "wc -l "+os.path.join(path,filename),
            stdout=PIPE, encoding="utf-8", shell=True)
    line_count = int(wc_output.stdout.split(" ")[0])
    file_start_time = datetime.now()
    with open(os.path.join(path,filename), "r", encoding="utf-8") as file:
        for line_index, line in enumerate(file):
            if line_index % 10000000 == 0:
                print("  line:",line_index+1,"/", line_count)
            if line.startswith("<"):
                continue
            word = line.split("\t")[0]
            if any(symbol in word for symbol in symbols):
                file_word_count += 1
    total_word_count += file_word_count
    print("File time:",datetime.now() - file_start_time, "word count:",file_word_count)
    print("Total time:", datetime.now() - start_time, "total word count:",total_word_count)
    