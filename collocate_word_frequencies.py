import os, re, pickle, subprocess
from collections import Counter
from datetime import datetime
from subprocess import PIPE

querys = ["havaitsevina(ni|si|an|mme|nne|nsa)[a-z\-]*", 
          "huomaavina(ni|si|an|mme|nne|nsa)[a-z\-]*"]
total_collocate_counts = Counter()
for query in querys:
    query_filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', query)
    with open('total_collocate_counts_'+query_filename+'.txt',"r") as file:
        for line in file.read().split("\n")[:-1]:
            lemma, count = line.split(", ")
            total_collocate_counts[lemma] += int(count)

lemma_frequency_counts = Counter()
start_time = datetime.now()
path = "/scratch/project_2003685/suomi24-2001-2017-vrt-v1-1/vrt/"
print("Start:", start_time)
for filename in os.listdir(path):
    print(filename)
    wc_output = subprocess.run(
            "wc -l "+os.path.join(path,filename),
            stdout=PIPE, encoding="utf-8", shell=True)
    line_count = int(wc_output.stdout.split(" ")[0])
    file_start_time = datetime.now()
    with open(os.path.join(path,filename), "r", encoding="utf-8") as file:
        for line_index, line in enumerate(file):
            if line_index % 1000000 == 0:
                print("  line:",line_index+1,"/", line_count)
            if line.startswith("<"):
                continue
            lemma = line.split("\t")[2]
            if lemma in total_collocate_counts:
                lemma_frequency_counts[lemma] += 1
    print("File time:",datetime.now() - file_start_time)
    print("Total time:", datetime.now() - start_time)
    
with open("lemma_frequency_counts.pkl", "wb") as pickle_file:
    pickle.dump(lemma_frequency_counts, pickle_file)