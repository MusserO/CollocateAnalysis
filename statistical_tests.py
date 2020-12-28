import os, re, pickle, math
from collections import Counter

queries = ["havaitsevina(ni|si|an|mme|nne|nsa)[a-z\-]*", 
          "huomaavina(ni|si|an|mme|nne|nsa)[a-z\-]*"]
          
with open("lemma_frequency_counts.pkl", "rb") as pickle_file:
    lemma_frequency_counts = pickle.load(pickle_file)
    
n_total_words = 3470785562
          
for query in queries:
    query_filename = re.sub('[^-a-zA-Z0-9_.() ]+', '', query)
    
    for context in ["left", "right", "total"]:
        collocate_counts = Counter()
        with open(context+'_collocate_counts_'+query_filename+'.txt',"r") as file:
            for line in file.read().split("\n")[:-1]:
                lemma, count = line.split(", ")
                collocate_counts[lemma] += int(count)
            
        n_collocate_words = sum(collocate_counts.values())
        
        t_test_scores = dict()
        MI_scores = dict()
        for lemma in collocate_counts:
            t_test_mean = collocate_counts[lemma]/n_total_words
            t_test_variance = t_test_mean*(1-t_test_mean)
            t_test_expected_mean = (lemma_frequency_counts[lemma] / n_total_words) * (n_collocate_words / n_total_words)
            t_test_scores[lemma] = (t_test_mean - t_test_expected_mean)/math.sqrt(t_test_variance/n_total_words)
            MI_scores[lemma] = math.log((n_total_words*collocate_counts[lemma]/\
                                        (n_collocate_words*lemma_frequency_counts[lemma])),2)
                                        
        min_count = 5
        with open(context+'_t-test_'+query_filename+'.txt',"w+") as file:
            for lemma, count in sorted(collocate_counts.items(), key=lambda x: (t_test_scores[x[0]], x[1], x[0]), reverse=True):
                if count >= min_count:
                    file.write("{}, {}, {}, {}, {}\n".format(lemma, count, lemma_frequency_counts[lemma], t_test_scores[lemma], MI_scores[lemma]))
        with open(context+'_MI_'+query_filename+'.txt',"w+") as file:
            for lemma, count in sorted(collocate_counts.items(), key=lambda x: (MI_scores[x[0]], x[1], x[0]), reverse=True):
                if count >= min_count:
                    file.write("{}, {}, {}, {}, {}\n".format(lemma, count, lemma_frequency_counts[lemma], t_test_scores[lemma], MI_scores[lemma]))
