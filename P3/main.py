from reuters import *
from file_output import *
from s1_utils import *
from s2_utils import *
from queries import *


# Constants
DIRECTORY = "../reuters21578_extracted/"
OUTPUT_DIRECTORY = "outputs_test/"    


# Subproject(1-A)
def S1_A():
    print("\n===================== Subproject(1-A) =====================")
    # Read and make inverted index
    sgm_files = filter_files(DIRECTORY, 1)
    documents = extract_documents_from_corpus(sgm_files)
    term_docID_pairs = tokenize(documents)
    test_corpus = make_test_corpus(term_docID_pairs, max_terms=10000)
    print()

    # Create inverted indices
    print("Naive Indexer: ")
    index_naive, time_naive = naive_indexer(test_corpus)
    print()
    print("SPIMI Indexer: ")
    index_spimi, time_spimi = spimi_indexer(test_corpus)
    print()
    print("Naive Indexer allowing duplicate term-docID pairs: ")
    index_naive_with_dup, time_naive_with_dup = naive_indexer(test_corpus, remove_duplicate=False)
    print()
    print("SPIMI Indexer allowing duplicate term-docID pairs: ")
    index_spimi_with_dup, time_spimi_with_dup = spimi_indexer(test_corpus, remove_duplicate=False)
    print()

    # Data for indexer and elapsed time
    time_analysis = {
        "naive": time_naive, 
        "spimi": time_spimi, 
        "naive_dup": time_naive_with_dup, 
        "spimi_dup": time_spimi_with_dup
    }

    # Output
    file_output(documents, 'raw_text', OUTPUT_DIRECTORY + 'subproject(1-A)/others/') 
    file_output(test_corpus, 'test_corpus', OUTPUT_DIRECTORY + 'subproject(1-A)/others/') 
    file_output(index_naive, 'naive_indexer', OUTPUT_DIRECTORY + 'subproject(1-A)/inverted_index/')
    file_output(index_naive_with_dup, 'naive_indexer_with_dup', OUTPUT_DIRECTORY + 'subproject(1-A)/inverted_index/')
    file_output(index_spimi, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject(1-A)/inverted_index/')
    file_output(index_spimi_with_dup, 'spimi_indexer_with_dup', OUTPUT_DIRECTORY + 'subproject(1-A)/inverted_index/')
    file_output(time_analysis, 'time_analysis', OUTPUT_DIRECTORY + 'subproject(1-A)/') 

    print("Results successfully outputed.")
    print()

    # To verify both naive indexer and spimi indexer's outputs are identical
    S1_test_identical(OUTPUT_DIRECTORY + 'subproject(1-A)/inverted_index/')


# Subproject(1-B)
def S1_B():
    print("\n===================== Subproject(1-B) =====================")
    # Read and make inverted index
    sgm_files = filter_files(DIRECTORY)
    documents = extract_documents_from_corpus(sgm_files)
    term_docID_pairs = tokenize(documents)
    test_corpus = make_test_corpus(term_docID_pairs)
    print()

    # Create inverted indices
    print("Naive Indexer: ")
    index_naive, time_naive = naive_indexer(test_corpus)
    print()
    print("SPIMI Indexer: ")
    index_spimi, time_spimi = spimi_indexer(test_corpus)
    print()
    print("Naive Indexer allowing duplicate term-docID pairs: ")
    index_naive_with_dup, time_naive_with_dup = naive_indexer(test_corpus, remove_duplicate=False)
    print()
    print("SPIMI Indexer allowing duplicate term-docID pairs: ")
    index_spimi_with_dup, time_spimi_with_dup = spimi_indexer(test_corpus, remove_duplicate=False)
    print()

    # Data for indexer and elapsed time
    time_analysis = {
        "naive": time_naive, 
        "spimi": time_spimi, 
        "naive_dup": time_naive_with_dup, 
        "spimi_dup": time_spimi_with_dup
    }

    # Output
    file_output(documents, 'raw_text', OUTPUT_DIRECTORY + 'subproject(1-B)/others/') 
    file_output(test_corpus, 'test_corpus', OUTPUT_DIRECTORY + 'subproject(1-B)/others/') 
    file_output(index_naive, 'naive_indexer', OUTPUT_DIRECTORY + 'subproject(1-B)/inverted_index/')
    file_output(index_naive_with_dup, 'naive_indexer_with_dup', OUTPUT_DIRECTORY + 'subproject(1-B)/inverted_index/')
    file_output(index_spimi, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject(1-B)/inverted_index/')
    file_output(index_spimi_with_dup, 'spimi_indexer_with_dup', OUTPUT_DIRECTORY + 'subproject(1-B)/inverted_index/')
    file_output(time_analysis, 'time_analysis', OUTPUT_DIRECTORY + 'subproject(1-B)/') 

    print("Results successfully outputed.")
    print()

    # To verify both naive indexer and spimi indexer's outputs are identical
    S1_test_identical(OUTPUT_DIRECTORY + 'subproject(1-B)/inverted_index/')


# Subproject(2)-Ranked
def S2_Ranked():
    k1 = 0
    b = 1

    print("\n===================== Subproject(2-Ranked) - RSVd =====================")
    # Read and make inverted index
    sgm_files = filter_files(DIRECTORY)
    documents = extract_documents_from_corpus(sgm_files)
    term_docID_pairs = tokenize(documents)
    test_corpus = make_test_corpus(term_docID_pairs)
    print()

    # Create inverted indices
    print("S2 SPIMI Indexer: ")
    index, time = spimi_indexer(test_corpus)
    print()
    # Make an inverted index that does not omit the duplicate postings yet (to be used to calculate TFtd)
    print("S2 Indexer allowing duplicate term-docID pairs: ")
    index_with_dup = S2_indexer_with_dup(test_corpus)
    print()

    # Compute necessary variables for RSVd scores
    print('Computing tftd...')
    index_tftd = TFtd(index_with_dup)
    print('Computing Ld...')
    dict_LD = LD(documents)
    print('Computing N...')
    N_val = N_compute(documents)
    print('Computing Ldavg...')
    LD_avg_val = LD_avg_compute(documents, N_val)
    # Store these variables into dict to be used for RSVd calculation
    variables = {'tftd': index_tftd, 'Ld': dict_LD, 'N': N_val, 'Lavg': LD_avg_val}
    print()

    # Output
    file_output(index_with_dup, 'indexer_with_dup', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/inverted_index/') 
    file_output(index, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/inverted_index/') 
    file_output(index_tftd, 'tftd', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/others/') 
    file_output(dict_LD, 'Ld', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/others/') 
    file_output(N_val, 'N', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/others/') 
    file_output(N_val, 'N', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/others/') 
    file_output(LD_avg_val, 'Ld_avg', OUTPUT_DIRECTORY + 'subproject(2-Ranked)/others/') 

    # Prepare input queries
    print("Processing input queries...")
    queries = get_sample_queries()
    print()

    # Iterate every queries to calculate its ranked results
    i = 1
    for query in queries:
        # Process queries and get its tokens
        query_tokens = query_process(query)

        # Compute RSVd
        print("Computing RSVd for query(" + str(i) + ") with (k1=" + str(k1) + ", b=" + str(b) + ")...")
        RSVd_dict = RSVd_compute(documents, index, query_tokens, variables, k1, b)

        #Output
        file_output(
            RSVd_dict, 
            'ranked_query(' + str(i) + ')-k1(' + str(k1) + ')-b(' + str(b) + ')', 
            OUTPUT_DIRECTORY + 'subproject(2-Ranked)/ranked_results/', 
            {'str_query': query, 'tokens': query_tokens, 'k1': k1, 'b': b}
        )
        i += 1

    # for query in queries:
    #     if query in index:
    #         print('Postings list for "' + query + ': ' + str(index[query]))
    #     else:
    #         print('Postings list for "' + query + ': ' + "---")
    #     print()

    print()
    print("Results successfully outputed.")
    print()


# Subproject(2)-Unranked
def S2_Unranked():
    print("\n===================== Subproject(2-Unranked) - Boolean =====================")
    # Read and make inverted index
    sgm_files = filter_files(DIRECTORY)
    documents = extract_documents_from_corpus(sgm_files)
    term_docID_pairs = tokenize(documents)
    test_corpus = make_test_corpus(term_docID_pairs)
    print()

    # Create inverted indices
    print("S2 SPIMI Indexer: ")
    index, time = spimi_indexer(test_corpus)
    # Output
    file_output(index, 'spimi_indexer', OUTPUT_DIRECTORY + 'subproject(2-Unranked)/inverted_index/') 
    print()

    # Prepare input queries
    print("Processing input queries...")
    queries = get_sample_queries()
    print()

    # Iterate every queries to calculate its ranked results
    i = 1
    for query in queries:
        # Process queries and get its tokens
        query_tokens = query_process(query)

        # Compute Boolean search with Intersection
        print("Computing Boolean Search with Intersection (AND) for query(" + str(i) + ")...")
        AND_info = intersection(query_tokens, index)

        # Compute Boolean search with Intersection
        print("Computing Boolean Search with Union (OR) for query(" + str(i) + ")...")
        OR_info = union(query_tokens, index)

        #Output
        file_output(
            AND_info, 
            'AND_query(' + str(i) + ')', 
            OUTPUT_DIRECTORY + 'subproject(2-Unranked)/unranked_results/', 
            {'str_query': query, 'tokens': query_tokens}
        )
        file_output(
            OR_info, 
            'OR_query(' + str(i) + ')', 
            OUTPUT_DIRECTORY + 'subproject(2-Unranked)/unranked_results/', 
            {'str_query': query, 'tokens': query_tokens}
        )
        i += 1
    
    print()
    print("Results successfully outputed.")
    print()



### START ###
print("\n************************* P3 Assignment *************************")
print("Using \"Reuters21578\" as a corpus (set of documents) to experiment...")
print("[1] Subproject(1-A): Experiment execution time for Naive indexer and SPIMI indexer")
print("[2] Subproject(1-B): Compile an inverted index for both Naive and SPIMI indexers (without compression)")
print("[3] Subproject(2-Ranked): Create an BM25 probabilistic search engine and provide rank results based on custom input queries")
print("[4] Subproject(2-Unranked): Create an Boolean search engine and provide unranked results based on custom boolean input queries")
print("[5] Run everything on above pipelines")
print("[Q] Exit")
while True:
    choice = input(">>> Enter from option [1] to [5] or Q to exit: ")
    if choice == '1':
        S1_A()
        break
    elif choice == '2':
        S1_B()
        break
    elif choice == '3':
        S2_Ranked()
        break
    elif choice == '4':
        S2_Unranked()
        break
    elif choice == '5':
        S1_A()
        S1_B()
        S2_Ranked()
        S2_Unranked()
        break
    elif choice == 'Q' or choice == 'q':
        exit()
    else:
        print("Invalid option, enter again.")
print()