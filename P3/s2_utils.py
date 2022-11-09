from collections import Counter
from nltk import word_tokenize
from math import log


# Create inverted index
def S2_indexer_with_dup(test_corpus):
    index = {} # empty inverted index

    print("Creating inverted index")

    for term, docID in test_corpus:
        if term in index:
            # append docID to the existing term
            index[term].append(docID)
        else:
            index[term] = [docID] 

    print("Sorting inverted index")
    index = dict(sorted(index.items(), key=lambda x:(x[0], x[1].sort(key = lambda y: y))))

    print("--> Total number of distinct terms(type) in dictionary: " + str(len(index)))

    return index

def S2_remove_duplicates(index):
    new_index = {}
    num_postings_removed = 0
    
    print("Removing duplicates from inverted index")

    for term, postings in index.items():
        # remove duplicate docIDs by set, and sort again
        new_postings = list(set(postings))
        # count num of postings removed
        num_postings_removed += len(postings) - len(new_postings)
        # sort docIDs in postings list
        sorted_new_postings = sorted(new_postings)
        # append postings to dictionary
        new_index[term] = sorted_new_postings

    print("  - " + str(num_postings_removed) + " postings have been removed due to duplicate.")

    return new_index

def S2_get_tokens_list(text):
    # tokenize words in doc
    tokens = word_tokenize(text)
    tokens[:] = [token for token in tokens if token.isalnum()] # remove all the special characters and punctuations
    tokens[:] = [token for token in tokens if token] # remove empty tokens

    return tokens


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
def RSVd_compute(documents, index, query_terms, variables, k1=0, b=1):
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

        for term in query_terms:
            # if tftd exists (tftd != 0)
            if term in index_tftd and docID in index_tftd[term]:
                # get tftd value
                TFtd_val = index_tftd[term][docID]
                # get dft value
                DFt_val = DFt_compute(index, term)

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


# Tokenize given queries
def query_process(input_query):
    tokens = S2_get_tokens_list(input_query)

    return tokens
