from p2_utils import *
from prettytable import PrettyTable

# Constants
DIRECTORY = "../reuters21578_extracted/"
OUTPUT_DIRECTORY = "outputs_test/"
MAX_SGM_FILES = 5  # [DEMO] for testing purpose
SAMPLE_QUERIES = ["copper", "Samjens", "Carmark", "Bundesbank"]


########## Prior to Subprojects ##########
def P1_review(sgm_files):
    F = []  # we will call postings list as "F" as in the instruction

    print("[P1] Extracting, Tokenizing, and creating term-documentID pairs from Reuter's collection: ")
    # iterate all the files inside the folder
    for filename in sgm_files:
        # open the file to be read
        sgm_file = open(filename, 'r', encoding='utf-8', errors='ignore') # avoid UnicodeDecodeError with 'r'
        print(" * Reading " + filename + " *")

        # Read Reuter's collection, extract the raw text of each article from the corpus
        documents = extract_documents_from_corpus(sgm_file)
        # Tokenize each article
        postings = tokenize(documents)
        # Append postings to F
        F.extend(postings)

    return F


########## Subproject 1 ##########
def S1_naive_indexer(F):
    # ******** P2 [1-1]: Create term-documentID pairs ********
    print("[P2_1-1]: Create term-documentID pairs")
    SUBPROJ_STEP = 'P2_1-1'
    file_output(F, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject1/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))
    print()

    # ******** P2 [1-2]: Sort list F and remove duplicates ********
    print("[P2_1-2]: Sort list F and remove duplicates")
    # *** [1-2_1] Sort Postings
    SUBPROJ_STEP = 'P2_1-2_(1)sorted'
    F = sort_postings(F)
    file_output(F, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject1/') # [DEMO] output the result
    # *** [1-2_2] Remove duplicates from Postings
    SUBPROJ_STEP = 'P2_1-2_(2)dup-removed'
    F = remove_duplicates(F)
    # [DEMO] output the result
    file_output(F, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject1/')
    print("--> Total number of postings in F: " + str(len(F)))
    print()

    # ******** P2 [1-3]: Complete inverted index ********
    print("[P2_1-3]: Complete inverted index via dictionary and pointer of postings")
    SUBPROJ_STEP = 'P2_1-3'
    index = inverted_index(F)
    file_output(index, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject1/') # [DEMO] output the result
    print("--> Total number of distinct terms(type) in dictionary: " + str(len(index)))
    print("--> Total number of postings in F: " + str(len(F)))

    return index


########## Subproject 2 ##########
def S2_naive_query_search(index):
    result = ''

    # *********** P2 [2-1]: Single Term Query Processing *********** #
    print("[P2_2-1]: Sample single term query search using naive index")
    SUBPROJ_STEP = 'P2_2-1'

    # Without lowercasing queries
    result += ("\nAll queries are NOT lowercased: \n")
    for query in SAMPLE_QUERIES:
        result += ('* Searching for query "' + query + '" *\n')
        # do query search
        postings, num_postings = query_search(query, index)

        # if query exists in postings
        if postings:
            result += '  Documents mentioning "' + query + '" exists based on the index.'
            result += "\n  - Document position: "
            for posting in postings:
                result += posting + " "
            result += "\n  - Term frequency: " + str(num_postings) + "\n"
        # if no queries in postings
        else:
            result += '  No document mentioning "' + query + '" has found based on the index.\n'

    # With lowercasing queries
    result += ("\nAll queries are lowercased: \n")
    for query in SAMPLE_QUERIES:
        if query.isalpha:
            query = query.lower()

        result += ('* Searching for query "' + query + '" *\n')
        # do query search
        postings, num_postings = query_search(query, index)

        # if query exists in postings
        if postings:
            result += '  Documents mentioning "' + query + '" exists based on the index.'
            result += "\n  - Document position: "
            for posting in postings:
                result += posting + " "
            result += "\n  - Term frequency: " + str(num_postings) + "\n"
        # if no queries in postings
        else:
            result += '  No document mentioning "' + query + '" has found based on the index.\n'

    # [DEMO] output the result
    file_output(result, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject2/')
    print(result)

    # *********** P2 [2-2]: Validate search return for sample queries *********** #
    print("[P2_2-2]: Validate search return for sample queries")
    SUBPROJ_STEP = 'P2_2-2'


########## Subproject 3 ##########
def ver_default(F):
    index = inverted_index(F)
    num_terms = compute_distinct_terms(index)
    num_postings = compute_nonpositional_postings(index)

    return F, num_terms, num_postings, index

def ver_no_numbers(F):
    F = remove_numbers(F)

    index = inverted_index(F)
    num_terms= compute_distinct_terms(index)
    num_postings = compute_nonpositional_postings(index)

    return F, num_terms, num_postings, index

def ver_case_folding(F):
    F = lowercase(F)

    index = inverted_index(F)
    num_terms= compute_distinct_terms(index)
    num_postings = compute_nonpositional_postings(index)

    return F, num_terms, num_postings, index

def ver_30_stop_words(F):
    stop_words = create_stop_words_list(30)
    F = remove_stop_words(F, stop_words)

    index = inverted_index(F)
    num_terms= compute_distinct_terms(index)
    num_postings = compute_nonpositional_postings(index)

    return F, num_terms, num_postings, index
    
def ver_150_stop_words(F):
    stop_words = create_stop_words_list(150)
    F = remove_stop_words(F, stop_words)

    index = inverted_index(F)
    num_terms= compute_distinct_terms(index)
    num_postings = compute_nonpositional_postings(index)

    return F, num_terms, num_postings, index

def ver_stemmer(F):
    F = porter_stemmer(F)

    index = inverted_index(F)
    num_terms= compute_distinct_terms(index)
    num_postings = compute_nonpositional_postings(index)

    return F, num_terms, num_postings, index

def compute_distinct_terms(index):
    num_terms = len(index)
    return num_terms

def compute_nonpositional_postings(index):
    num_postings = 0
    for postings in index.values():
        num_postings += len(postings)

    return num_postings

def compute_reduction(start, final):
    # Reduction = (Starting value − Final value) / (Starting value) × 100
    return round((start - final) / start * 100, 2)

def S3_compressed_indexer(F):
    # *********** P2 [3-1]: Implement Lossy dictionary Compression *********** #
    print("[P2_3-1]: Implement Lossy Dictionary Compression techniques")
    
    print("\n(1) Sort list F")
    F = sort_postings(F)
    print("--> Total number of postings in F: " + str(len(F)))

    print("\n(2) Remove duplicates from F")
    F = remove_duplicates(F)
    print("--> Total number of postings in F: " + str(len(F)))

    print("\n(3) Complete inverted index via dictionary and pointer of postings")
    # *** unfiltered
    print("(DEFAULT)")
    F, num_terms_default, num_postings_default, index = ver_default(F)
    file_output(index, 'P2_3-1_(1)index-default', OUTPUT_DIRECTORY + 'subproject3/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))

    # *** remove numbers
    print("(NO NUMBERS)")
    F, num_terms_no_numbers, num_postings_no_numbers, index = ver_no_numbers(F)
    file_output(index, 'P2_3-1_(2)index-no-numbers', OUTPUT_DIRECTORY + 'subproject3/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))

    # *** case folding
    print("(LOWERCASE)")
    F, num_terms_lowercase, num_postings_lowercase, index = ver_case_folding(F)
    file_output(index, 'P2_3-1_(3)index-lowercase', OUTPUT_DIRECTORY + 'subproject3/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))

    # *** 30 stop words
    print("(30 STOPWORDS)")
    F, num_terms_30_stopwords, num_postings_30_stopwords, index = ver_30_stop_words(F)
    file_output(index, 'P2_3-1_(4)index-stopwords-30', OUTPUT_DIRECTORY + 'subproject3/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))

    # *** 150 stop words
    print("(150 STOPWORDS)")
    F, num_terms_150_stopwords, num_postings_150_stopwords, index = ver_150_stop_words(F)
    file_output(index, 'P2_3-1_(5)index-stopwords-50', OUTPUT_DIRECTORY + 'subproject3/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))

    # *** porter stemming
    print("(PORTER STEMMER)")
    F, num_terms_stemmer, num_postings_stemmer, index = ver_stemmer(F)
    file_output(index, 'P2_3-1_(6)index-stemmer', OUTPUT_DIRECTORY + 'subproject3/') # [DEMO] output the result
    print("--> Total number of postings in F: " + str(len(F)))

    # Creating table for stats
    print("\n(4) Statistics: ")
    t = PrettyTable()
    t.field_names = [
        ' ', 
        '(Distinct) Terms', 
        'Δ% Terms', 'T% Terms', 
        'Nonpositional Postings', 
        'Δ% Postings', 
        'T% Postings'
    ]
    t.add_row([
        'unfiltered', 
        num_terms_default, 
        '--', 
        '--', 
        num_postings_default, 
        '--', 
        '--'
    ])
    t.add_row([
        'no numbers', 
        num_terms_no_numbers, 
        compute_reduction(num_terms_default, num_terms_no_numbers),
        compute_reduction(num_terms_default, num_terms_no_numbers),  
        num_postings_no_numbers,
        compute_reduction(num_postings_default, num_postings_no_numbers),
        compute_reduction(num_postings_default, num_postings_no_numbers),
    ])
    t.add_row([
        'case folding', 
        num_terms_lowercase,
        compute_reduction(num_terms_no_numbers, num_terms_lowercase),
        compute_reduction(num_terms_default, num_terms_lowercase), 
        num_postings_default,
        compute_reduction(num_postings_no_numbers, num_postings_lowercase),
        compute_reduction(num_postings_default, num_postings_lowercase)
    ])
    t.add_row([
        '30 stop words (*)', 
        num_terms_30_stopwords,
        compute_reduction(num_terms_lowercase, num_terms_30_stopwords),
        compute_reduction(num_terms_default, num_terms_30_stopwords),
        num_postings_30_stopwords,
        compute_reduction(num_postings_lowercase, num_postings_30_stopwords),
        compute_reduction(num_postings_default, num_postings_30_stopwords),
    ])
    t.add_row([
        '150 stop words (*)', 
        num_terms_150_stopwords,
        compute_reduction(num_terms_lowercase, num_terms_150_stopwords),
        compute_reduction(num_terms_default, num_terms_150_stopwords), 
        num_postings_150_stopwords,
        compute_reduction(num_postings_lowercase, num_postings_150_stopwords),
        compute_reduction(num_postings_default, num_postings_150_stopwords)
    ])
    t.add_row([
        'stemming', 
        num_terms_stemmer, 
        compute_reduction(num_terms_150_stopwords, num_terms_stemmer),
        compute_reduction(num_terms_default, num_terms_stemmer),
        num_postings_stemmer,
        compute_reduction(num_postings_150_stopwords, num_postings_stemmer),
        compute_reduction(num_postings_default, num_postings_stemmer),
    ])

    t = str(t)
    t += "\n[References]: "
    t += "\n - (Distinct) Terms: Number of distinct terms in dictionary"
    t += "\n - Nonpositional Postings: Number of nonpositional postings (total postings)"
    t += "\n - ∆%: reduction in size from the previous"
    t += "\n - T%: culmulative (total) reduction from unfiltered"
    t += "\n   (*) 30 stoop words and 150 stop words both use case folding as their reference line"

    # [DEMO] output the result
    SUBPROJ_STEP = 'P2_3-1'
    file_output(t, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject3/')
    print(t)
    print()

    return index


def S3_compressed_query_search(index):
    result = ''

    # *********** P2 [3-2]: Single Term Query Processing *********** #
    print("[P2_3-2]: Sample single term query search using compressed index")
    SUBPROJ_STEP = 'P2_3-2'

    # Without lowercasing queries
    result += ("\nAll queries are NOT lowercased: \n")
    for query in SAMPLE_QUERIES:
        result += ('* Searching for query "' + query + '" *\n')
        # do query search
        postings, num_postings = query_search(query, index)
        # if query exists in postings
        if postings:
            result += '  Documents mentioning "' + query + '" exists based on the index.'
            result += "\n  - Document position: "
            for posting in postings:
                result += posting + " "
            result += "\n  - Term frequency: " + str(num_postings) + "\n"
        # if no queries in postings
        else:
            result += '  No document mentioning "' + query + '" has found based on the index.\n'

    # With lowercasing queries
    result += ("\nAll queries are lowercased: \n")
    for query in SAMPLE_QUERIES:
        if query.isalpha:
            query = query.lower()

        result += ('* Searching for query "' + query + '" *\n')
        # do query search
        postings, num_postings = query_search(query, index)
        # if query exists in postings
        if postings:
            result += '  Documents mentioning "' + query + '" exists based on the index.'
            result += "\n  - Document position: "
            for posting in postings:
                result += posting + " "
            result += "\n  - Term frequency: " + str(num_postings) + "\n"
        # if no queries in postings
        else:
            result += '  No document mentioning "' + query + '" has found based on the index.\n'

    # [DEMO] output the result
    file_output(result, SUBPROJ_STEP, OUTPUT_DIRECTORY + 'subproject3/')
    print(result)



### START ###
print("\n===================== Pre processing =====================\n")
#sgm_files = filter_corpus(DIRECTORY, MAX_SGM_FILES) # for testing purpose, limit number of files
sgm_files = filter_corpus(DIRECTORY) # if default num files
F = P1_review(sgm_files)
# Subproject 1
print("\n\n\n===================== Subproject 1 =====================\n")
index = S1_naive_indexer(F)
# Subproject 2
print("\n\n\n===================== Subproject 2 =====================\n")
S2_naive_query_search(index)
# Subproject 3
print("\n\n\n===================== Subproject 3 =====================\n")
index = S3_compressed_indexer(F)
S3_compressed_query_search(index)