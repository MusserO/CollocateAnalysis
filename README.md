# CollocateAnalysis
Python scripts for performing collocate analysis on a corpus. These scripts were created for collocate analysis on The Suomi24 Corpus 2001-2017, VRT version 1.1: http://urn.fi/urn:nbn:fi:lb-2020021801. The scripts will not work as is for corpora in other formats than VRT.

- Use corpus_parser.py to find concordances of a query.
- Use word_counts.py to count the number of words in the corpus that include at least one ascii letter a-z, number, or one of the letters å, ä, ö.
- Use collocate_counts.py to count and store the collocates of the query in the concordances created by corpus_parser.py
- Use collocate_word_frequencies.py to count how many times each collocate word appears in the corpus.
- Use statistical_tests.py to compute t-test and MI scores for the collocates.
