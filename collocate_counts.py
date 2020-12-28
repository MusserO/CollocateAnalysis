import os, re, pickle
from collections import Counter

query = "havaitsevina(ni|si|an|mme|nne|nsa)[a-z\-]*"
#query = "huomaavina(ni|si|an|mme|nne|nsa)[a-z\-]*"
query_filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', query)

with open("concordances_"+query_filename+".pkl", "rb") as pickle_file:
    concordances = pickle.load(pickle_file)
    
contexts = set()
    
for match_index, concordance_lines in concordances:
    left_collocate_lemmas = []
    right_collocate_lemmas = []
    left_collocate_words = []
    right_collocate_words = []
    for line_index, line in enumerate(concordance_lines):
        items = line.split("\t")
        word, _, lemma = items[:3]
        if line_index < match_index:
            left_collocate_lemmas.append(lemma)
            left_collocate_words.append(word)
        elif line_index > match_index:
            right_collocate_lemmas.append(lemma)
            right_collocate_words.append(word)
        else:
            match = word

    contexts.add((tuple(left_collocate_lemmas), tuple(right_collocate_lemmas), match,
                    tuple(left_collocate_words), tuple(right_collocate_words)))

print("Alussa:",len(concordances),"virkettä - duplikaattien poiston jälkeen:", len(contexts), "esiintymää.")

with open("contexts_"+query_filename+".txt","w+", encoding="utf-8") as file:
    file.write("\n".join(["    ".join([" ".join(part) for part in context]) for context in contexts]))

small_letters = list(map(chr, range(ord('a'), ord('z')+1))) + ['å','ä','ö']
big_letters = list(map(chr, range(ord('A'), ord('Z')+1))) + ['Å','Ä','Ö']
digits = list(map(chr, range(ord('0'), ord('9')+1)))
symbols = small_letters + big_letters + digits

left_collocate_counts = Counter()
right_collocate_counts = Counter()
total_collocate_counts = Counter()
collocate_window_span_left = 4
collocate_window_span_right = 4
for left, right, _, _, _ in contexts:
    left_words = [word for word in left if any(symbol in word for symbol in symbols)]
    right_words = [word for word in right if any(symbol in word for symbol in symbols)]
    left_collocates = left_words[-collocate_window_span_left:]
    right_collocates = right_words[:collocate_window_span_right]
    for word in left_collocates:
        left_collocate_counts[word] += 1
        total_collocate_counts[word] += 1
    for word in right_collocates:
        right_collocate_counts[word] += 1
        total_collocate_counts[word] += 1
        
print("Vasempana kollokaattina:", sum(left_collocate_counts.values()), "sanetta")
print("Oikeana kollokaattina:", sum(right_collocate_counts.values()), "sanetta")
print("Kollokaatteina yhteensä:", sum(total_collocate_counts.values()), "sanetta")

with open('left_collocate_counts_'+query_filename+'.txt',"w+") as file:
    for lemma, count in sorted(left_collocate_counts.items(), key=lambda x: (x[1], x[0]), reverse=True):
        file.write("{}, {}\n".format(lemma, count))
with open('right_collocate_counts_'+query_filename+'.txt',"w+") as file:
    for lemma, count in sorted(right_collocate_counts.items(), key=lambda x: (x[1], x[0]), reverse=True):
        file.write("{}, {}\n".format(lemma, count))
with open('total_collocate_counts_'+query_filename+'.txt',"w+") as file:
    for lemma, count in sorted(total_collocate_counts.items(), key=lambda x: (x[1], x[0]), reverse=True):
        file.write("{}, {}\n".format(lemma, count))
