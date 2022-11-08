from reuters import *
from file_output import *
from s1_utils import *
from s2_utils import *


# Constants
DIRECTORY = "../reuters21578_extracted/"
OUTPUT_DIRECTORY = "outputs_test/"    


### START ###
print("\n===================== Subproject(1-A) =====================")
sgm_files = filter_files(DIRECTORY, 1)
documents = extract_documents_from_corpus(sgm_files)
term_docID_pairs = tokenize(documents)
test_corpus = make_test_corpus(term_docID_pairs, max_terms=10000)

file_output(test_corpus, 'test_corpus', OUTPUT_DIRECTORY + 'subproject1(A)/') # [DEMO] output the result
print()
index = naive_indexer(test_corpus)
file_output(index, 'naive_indexer', OUTPUT_DIRECTORY + 'subproject1(A)/') # [DEMO] output the result
print()
index = spimi_indexer(test_corpus)
file_output(index, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject1(A)/') # [DEMO] output the result
print()
S1_test_identical(OUTPUT_DIRECTORY + 'subproject1(A)/')

print("\n===================== Subproject(1-B) =====================")
sgm_files = filter_files(DIRECTORY)
documents = extract_documents_from_corpus(sgm_files)
term_docID_pairs = tokenize(documents)
test_corpus = make_test_corpus(term_docID_pairs)

file_output(test_corpus, 'test_corpus', OUTPUT_DIRECTORY + 'subproject1(B)/') # [DEMO] output the result
print()
index = naive_indexer(test_corpus)
file_output(index, 'naive_indexer', OUTPUT_DIRECTORY + 'subproject1(B)/') # [DEMO] output the result
print()
index = spimi_indexer(test_corpus)
file_output(index, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject1(B)/') # [DEMO] output the result
print()
S1_test_identical(OUTPUT_DIRECTORY + 'subproject1(B)/')

print("\n===================== Subproject(2) =====================")
# sgm_files = filter_files(DIRECTORY)
# documents = extract_documents_from_corpus(sgm_files)
# term_docID_pairs = tokenize(documents)
# test_corpus = make_test_corpus(term_docID_pairs)

# use the index from previous

index = S2_indexer(test_corpus)
index_deduplicated = S2_remove_duplicates(index)
file_output(index, 's2_indexer', OUTPUT_DIRECTORY + 'subproject2/') # [DEMO] output the result
print()
index_tftd = TFtd(index)
file_output(index_tftd, 'tftd', OUTPUT_DIRECTORY + 'subproject2/') # [DEMO] output the result