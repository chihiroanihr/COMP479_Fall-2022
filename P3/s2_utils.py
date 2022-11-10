from math import log
from collections import Counter
from nltk import word_tokenize
from nltk.corpus import stopwords


# Create inverted index
def S2_indexer_with_dup(test_corpus):
    index = {} # empty inverted index

    print("* Creating inverted index with duplicates...")
    for term, docID in test_corpus:
        if term in index:
            # append docID to the existing term
            index[term].append(docID)
        else:
            index[term] = [docID] 

    print("* Sorting inverted index...")
    index = dict(sorted(index.items(), key=lambda x:(x[0], x[1].sort(key = lambda y: y))))

    print("--> Total number of distinct terms(type) in dictionary: " + str(len(index)))

    return index

# def S2_remove_duplicates(index):
#     new_index = {}
#     num_postings_removed = 0
    
#     print("Removing duplicates from inverted index")

#     for term, postings in index.items():
#         # remove duplicate docIDs by set, and sort again
#         new_postings = list(set(postings))
#         # count num of postings removed
#         num_postings_removed += len(postings) - len(new_postings)
#         # sort docIDs in postings list
#         sorted_new_postings = sorted(new_postings)
#         # append postings to dictionary
#         new_index[term] = sorted_new_postings

#     print("  - " + str(num_postings_removed) + " postings have been removed due to duplicate.")

#     return new_index

def S2_get_tokens_list(text):
    # tokenize words in doc
    tokens = word_tokenize(text)
    tokens[:] = [token for token in tokens if token.isalnum()] # remove all the special characters and punctuations
    tokens[:] = [token for token in tokens if token] # remove empty tokens

    return tokens


# ------------------------- Subproject(2)-Ranked ------------------------- #

# Number of terms t in each documents d
def TFtd(index):
    index_TFtd = {}

    for term, postings in index.items():
        '''
        examle:
        if {term1: 12 -> 12 -> 134 -> 156 -> 167 -> 167 -> 167}
        then
            term_freq_dict = {12: 2, 134: 1, 156: 1, 167: 3}
        '''
        term_freq_dict = dict(Counter(postings))

        # sort by docIDs
        sorted_term_freq_dict = dict(sorted(term_freq_dict.items(), key=lambda t: t[0]))

        # append to index
        index_TFtd[term] = sorted_term_freq_dict
    
    # sort by terms
    index_TFtd = dict(sorted(index_TFtd.items(), key=lambda x: x[0]))

    # return dictionary of {term: {docID1: term_freq, docID2: term_freq, ...}, ...}
    return index_TFtd

def get_TFtd_val(index, docID, input_term):
    TFtd_val = 0

    for term, postings in index.items():
        if term == input_term:
            tf_dict = dict(Counter(postings))
            if docID in tf_dict:
                TFtd_val = tf_dict[docID]

    return TFtd_val

# Document Length (Total number of words in document)
def LD(documents):
    dict_LD = {}

    # compute number of words in each documents (document length)
    for docID, text in documents.items():
        # get tokens
        tokens = S2_get_tokens_list(text)
        # assign freq tokens to docID
        dict_LD[docID] = len(tokens)

    # sort by docIDs
    dict_LD = dict(sorted(dict_LD.items(), key=lambda x: x[0]))

    # return dictionary of {docID: docLength, ...}
    return dict_LD

def get_LD_val(documents, input_docID):
    LD_val = 0

    for docID, text in documents.items():
        # compute number of words in given document ID (document length)
        if docID == input_docID:
            # get tokens
            tokens = S2_get_tokens_list(text)
            # get freq of tokens val
            LD_val = len(tokens)
    
    return LD_val

# Average document length for the whole collection
def LD_avg_compute(documents, N):
    # total number of words in the collection
    total_num_words = 0

    # count number of words in each documents (document length)
    for text in documents.values():
        # get tokens
        tokens = S2_get_tokens_list(text)
        # add to total number of words in the collection
        total_num_words += len(tokens)

    # compute LD Average
    return total_num_words / N

# Total number of documents in the collection
def N_compute(documents):
    return len(documents)

# Number of documents in collection that certain term occurs in
def DFt_compute(index, term):
    DFt_val = 0

    if term in index:
        DFt_val = len(index[term])
    
    return DFt_val

# idf weighting of the query term present
def iDFt_compute(N, DFt):
    return log(N/DFt)

# Given the document, how relevant the term is
def RSVd_compute(documents, index, query_tokens, variables, k1=0, b=1):
    '''
    k1: positive tuning parameter that calibrates the document term frequency scaling
        0: binary model (no term frequency)
        large value: using raw term frequency
    '''

    '''
    b: tuning parameter determining the scaling by document length (0 <= b <= 1)
        0: no document length normalization
        1: fully scaling the term weight by the document length
    '''
    RSVd_val = 0
    RSVd_dict = {}

    # get all necessary variables
    N_val = variables['N']
    LD_avg_val = variables['Lavg']
    dict_LD = variables['Ld']
    index_tftd = variables['tftd']

    for docID in documents:
        # get Ld value
        LD_val = dict_LD[docID]

        for token in query_tokens:
            # if tftd exists (tftd != 0)
            if token in index_tftd and docID in index_tftd[token]:
                # get tftd value
                TFtd_val = index_tftd[token][docID]
                # get dft value
                DFt_val = DFt_compute(index, token)

                # compute weighting
                iDFt = iDFt_compute(N_val, DFt_val)
                x = (k1 + 1) * TFtd_val
                y = k1 * ((1 - b) + b * (LD_val / LD_avg_val)) + TFtd_val

                RSVd_val += log(iDFt) * (x / y)
        
        # collect RSVd scores into dictionary
        RSVd_dict[docID] = RSVd_val
        RSVd_val = 0 # initialize

    # Sort the result from highest rank
    RSVd_dict = dict(sorted(RSVd_dict.items(), key=lambda x: (x[1], x[0]), reverse=True))

    return RSVd_dict


# ------------------------- Subproject(2)-Unranked ------------------------- #

# Boolean search (AND)
def intersection(query_tokens, index):
    postings_total = []
    common_postings = []
    message = ""

    if len(query_tokens) >= 2:
        # Get postings list for every tokens first
        for token in query_tokens:
            if token in index:
                postings = index[token]
                postings_total.append(postings)
        
        # Get Intersection
        common_postings = sorted(list(set.intersection(*[set(postings) for postings in postings_total])))

        # If intersection postings found
        if common_postings:
            # output
            message = str(len(common_postings)) + " intersection postings (AND) found."
            print(" - " + message)

        else:
            # Output
            message = "0 intersection postings (AND) found."
            print(" - " + message)

    else:
        message = "There are not enough query tokens to perform boolean intersection."
        print(" - " + message)

    # make dictionary to store info
    AND_info = {'postings': common_postings, 'message': message}

    return AND_info

# Boolean search (OR)
def union(query_tokens, index):
    postings_total = []
    union_postings = []
    union_postings_ranked = {}
    message = ""

    # If enough query tokens exist
    if len(query_tokens) >= 2:
        # Get postings list for every tokens first
        for token in query_tokens:
            if token in index:
                postings = index[token]
                postings_total.append(postings)
        
        # Get Union
        union_postings = sorted(list(set.union(*[set(postings) for postings in postings_total])))
        
        # If union postings found
        if union_postings:
            # Compute rank of how many keywords union docs contain
            for docID in union_postings:
                freq_docID = sum(postings.count(docID) for postings in postings_total)
                union_postings_ranked[docID] = freq_docID

            # Get Union Rank
            union_postings_ranked = dict(sorted(union_postings_ranked.items(), key=lambda x:x[1], reverse=True))

            # Output
            message = str(len(union_postings)) + " union postings (OR) found."
            print(" - " + message)

        else:
            # Output
            message = "0 union postings (OR) found."
            print(" - " + message)

    else:
        message = "There are not enough query tokens to perform boolean union."
        print(" - " + message)

    # make dictionary to store info
    OR_info = {'postings': union_postings, 'ranked_postings': union_postings_ranked, 'message': message}
    
    return OR_info


# ---------------------------- Sample Queries ---------------------------- #

# Tokenize and remove stop words from given queries
def query_process(input_query):
    # Tokenize
    tokens = S2_get_tokens_list(input_query)

    # Remove stopwords from queries
    stop_words = list(set(stopwords.words('english')))
    tokens[:] = [token for token in tokens if token not in stop_words]

    return tokens




# ************************** Testing ************************** #
if __name__ == "__main__":

    sample_queries1 = "America"
    sample_queries2 = "population"
    sample_queries3 = "South Korea and Japan"
    sample_queries4 = "Democrats' welfare and healthcare reform policies"
    sample_queries5 = "Drug company bankruptcies"
    sample_queries6 = "George Bush"

    stop_words = list(set(stopwords.words('english')))
    print("Stopwords: " + str(stop_words) + "\n")

    tokens1 = query_process(sample_queries1)
    tokens2 = query_process(sample_queries2)
    tokens3 = query_process(sample_queries3)
    tokens4 = query_process(sample_queries4)
    tokens5 = query_process(sample_queries5)
    tokens6 = query_process(sample_queries6)
    print("Tokens 1: " + str(tokens1))
    print("Tokens 2: " + str(tokens2))
    print("Tokens 3: " + str(tokens3))
    print("Tokens 4: " + str(tokens4))
    print("Tokens 5: " + str(tokens5))
    print("Tokens 5: " + str(tokens6))