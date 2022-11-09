from reuters import *
from file_output import *
from s1_utils import *
from s2_utils import *
from sample_queries import *


# Constants
DIRECTORY = "../reuters21578_extracted/"
OUTPUT_DIRECTORY = "outputs_test/"    


### START ###
print("\n===================== Subproject(1-A) =====================")
# Read and make inverted index
sgm_files = filter_files(DIRECTORY, 1)
documents = extract_documents_from_corpus(sgm_files)
term_docID_pairs = tokenize(documents)
test_corpus = make_test_corpus(term_docID_pairs, max_terms=10000)
print()
index = naive_indexer(test_corpus)
print()
index = spimi_indexer(test_corpus)
print()

# Output
file_output(documents, 'raw_text', OUTPUT_DIRECTORY + 'subproject1(A)/others/') # [DEMO] output the result
file_output(test_corpus, 'test_corpus', OUTPUT_DIRECTORY + 'subproject1(A)/others/') # [DEMO] output the result
file_output(index, 'naive_indexer', OUTPUT_DIRECTORY + 'subproject1(A)/') # [DEMO] output the result
file_output(index, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject1(A)/') # [DEMO] output the result

# To verify both naive indexer and spimi indexer's outputs are identical
S1_test_identical(OUTPUT_DIRECTORY + 'subproject1(A)/')


print("\n===================== Subproject(1-B) =====================")
# Read and make inverted index
sgm_files = filter_files(DIRECTORY)
documents = extract_documents_from_corpus(sgm_files)
term_docID_pairs = tokenize(documents)
test_corpus = make_test_corpus(term_docID_pairs)
print()
index = naive_indexer(test_corpus)
print()
index = spimi_indexer(test_corpus)
print()

# Output
file_output(documents, 'raw_text', OUTPUT_DIRECTORY + 'subproject1(B)/others/') # [DEMO] output the result
file_output(test_corpus, 'test_corpus', OUTPUT_DIRECTORY + 'subproject1(B)/others/') # [DEMO] output the result
file_output(index, 'naive_indexer', OUTPUT_DIRECTORY + 'subproject1(B)/') # [DEMO] output the result
file_output(index, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject1(B)/') # [DEMO] output the result

# To verify both naive indexer and spimi indexer's outputs are identical
S1_test_identical(OUTPUT_DIRECTORY + 'subproject1(B)/')


print("\n===================== Subproject(2) =====================")
# sgm_files = filter_files(DIRECTORY)
# documents = extract_documents_from_corpus(sgm_files)
# term_docID_pairs = tokenize(documents)
# test_corpus = make_test_corpus(term_docID_pairs)

# ****** use the index from previous ******

# Make an inverted index that does not omit the duplicate postings yet (to be used to calculate TFtd)
index_with_dup = S2_indexer_with_dup(test_corpus)
file_output(index_with_dup, 'indexer_with_dup', OUTPUT_DIRECTORY + 'subproject2/') # [DEMO] output the result
print()

# Compute necessary variables for RSVd scores
print('Computing tftd...')
index_tftd = TFtd(index_with_dup)
file_output(index_tftd, 'tftd', OUTPUT_DIRECTORY + 'subproject2/others/') # [DEMO] output the result

print('Computing Ld...')
dict_LD = LD(documents)
file_output(dict_LD, 'Ld', OUTPUT_DIRECTORY + 'subproject2/others/') # [DEMO] output the result

print('Computing N...')
N_val = N_compute(documents)
file_output(N_val, 'N', OUTPUT_DIRECTORY + 'subproject2/others/') # [DEMO] output the result

print('Computing Ldavg...')
LD_avg_val = LD_avg_compute(documents, N_val)
file_output(LD_avg_val, 'Ld_avg', OUTPUT_DIRECTORY + 'subproject2/others/') # [DEMO] output the result

# Store these variables into dict to be used for RSVd calculation
variables = {'tftd': index_tftd, 'Ld': dict_LD, 'N': N_val, 'Lavg': LD_avg_val}
print()


print("Processing input queries")
queries = get_sample_queries()

for query in queries:
    i = 0
    # Get query tokens
    query_tokens = S2_get_tokens_list(query)
    # Compute RSVd
    print("Computing RSVd...")
    RSVd_dict = RSVd_compute(documents, index, query_tokens, variables, k1=0, b=0)
    file_output(RSVd_dict, 'RSVd_result(' + i + ')', OUTPUT_DIRECTORY + 'subproject2/') # [DEMO] output the result

    i+=1

# for query in queries:
#     if query in index:
#         print('Postings list for "' + query + ': ' + str(index[query]))
#     else:
#         print('Postings list for "' + query + ': ' + "---")
