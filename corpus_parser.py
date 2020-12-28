 # coding=utf-8
import os, re, pickle, subprocess
from datetime import datetime
from subprocess import PIPE

def find_concordances_from_file(filename, path, query, query_filename, batch_size):
    # Search matches using grep
    
    #Windows, Python 3.7+
    #subprocess_output = subprocess.run(['C:\\Program Files\\Git\\bin\\bash.exe', '-c',
    #    "egrep -i -ob '"+query+"' "+os.path.join(path,filename).replace("\\", "\\\\\\")+\
    #    " | grep -oE '[0-9]+'"],
    #    capture_output=True, encoding="utf-8")
        
    #Linux, Python 3.6
    subprocess_output = subprocess.run(
        "egrep -i -ob '"+query+"' "+os.path.join(path,filename)+\
        " | grep -oE '[0-9]+'",
        stdout=PIPE, encoding="utf-8", shell=True)
        
    
    # Collect character positions of the matches in the file 
    match_positions = [int(position) for position in subprocess_output.stdout.split("\n")[:-1]]

    print("Found",len(match_positions),"matches")
    file_concordances = set()
    
    with open(os.path.join(path,filename), "rb") as file:
        for position_index, position in enumerate(match_positions):
            # Search start and end of the sentence containing the match
            file.seek(position, 0)
            first_line_break_found = False
            start_of_sentence_found = False
            end_of_sentence_found = False
            sentence_start = b""
            sentence_end = b""
            offset = 0
            while not start_of_sentence_found:
                offset += batch_size
                file.seek(position-offset, 0)
                text_batch = file.read(batch_size)
                text_batch_not_broken = text_batch + sentence_start[:len(b"<sentence")]
                if b"<sentence" in text_batch_not_broken:
                    sentence_start = text_batch_not_broken.split(b"<sentence")[-1] + sentence_start[len(b"<sentence"):]
                    start_of_sentence_found = True
                else:
                    sentence_start = text_batch + sentence_start
                if not first_line_break_found:
                    if b"\n" in text_batch:
                        sentence_end = text_batch.split(b"\n")[-1] + sentence_end
                        first_line_break_found = True
                    else:
                        sentence_end = text_batch + sentence_end
                    
            # Filter out matches that are not within a sentence (e.g. matches in metadata text)
            if b"</sentence>" in sentence_start:
                continue
                
            file.seek(position, 0)
            while not end_of_sentence_found:
                text_batch = file.read(batch_size)
                text_batch_not_broken = sentence_end[-len(b"</sentence>\n"):] + text_batch
                if b"</sentence>\n" in text_batch_not_broken:
                    sentence_end = sentence_end[:-len(b"</sentence>\n")] + text_batch_not_broken.split(b"</sentence>\n")[0]
                    end_of_sentence_found = True
                else:
                    sentence_end += text_batch

            start_lines = sentence_start.decode("utf-8").split("\n")[1:-1]
            end_lines = sentence_end.decode("utf-8").split("\n")[:-1]
            sentence_lines = tuple(start_lines+end_lines)
            file_concordances.add((len(start_lines), sentence_lines))
    
    return file_concordances
                
if __name__ == '__main__':
    start_time = datetime.now()
                
    #query = "huomaavina(ni|si|an|mme|nne|nsa)[a-z\-]*"
    query = "havaitsevina(ni|si|an|mme|nne|nsa)[a-z\-]*"
    query_filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', query)
    
    path = "/scratch/project_2003685/suomi24-2001-2017-vrt-v1-1/vrt/"
    batch_size = 512
    
    concordances = set()
    
    for filename in os.listdir(path):
        print(filename)
        concordances |= find_concordances_from_file(filename, path, query, query_filename, batch_size)
        print("Concordances:", len(concordances))
        print("Elapsed time:",datetime.now()-start_time)
        
    with open("concordances_"+query_filename+".pkl", "wb") as pickle_file:
        pickle.dump(concordances, pickle_file)
    
    print("Total time elapsed:",datetime.now()-start_time)
    print(len(concordances))
    for word_index, lines in list(concordances)[:5]:
        print("word_index:",word_index)
        print(" ".join([line.split()[0] for line in lines]))
        print("---------")
