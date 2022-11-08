from collections import Counter
from nltk import word_tokenize
from math import log


# Create inverted index
def S2_indexer(test_corpus):
    index = {} # empty inverted index

    print("Creating inverted index")

    for term, docID in test_corpus:
        if term in index:
            # append docID to the existing term
            index[term].append(docID)
        else:
            index[term] = [docID] 

    print("Sorting inverted index")
    index = dict(sorted(index.items(), key=lambda x:(x[0], x[1].sort(key = lambda y: int(y)))))

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
        sorted_new_postings = sorted(new_postings, key=int)
        # append postings to dictionary
        new_index[term] = sorted_new_postings

    print("  - " + str(num_postings_removed) + " postings have been removed due to duplicate.")

    return new_index


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

# Document Length (Total number of words in document)
def LD(documents):
    dict_LD = {}

    # compute number of words in each documents (document length)
    for docID, text in documents.items():
        words = word_tokenize(text)
        num_words = len(words)
        dict_LD[docID].append(num_words)

    # return dictionary of {docID: docLength, ...}
    return dict_LD

# Average document length for the whole collection
def LDave_compute(documents):
    # total number of words in the collection
    total_num_words = 0
    # count number of all documents in the collection
    num_docs = N_compute(documents)
    # count number of words in each documents (document length)
    for document in documents.values():
        words = word_tokenize(document)
        num_words = len(words)
        # add to total number of words in the collection
        total_num_words += num_words

    # compute LD Average
    return num_docs / total_num_words

# Total number of documents in the collection
def N_compute(documents):
    return len(documents)

# Number of documents in collection that certain term occurs in
def DFt_compute(index, term):
    return len(index[term])


# idf weighting of the query term present
def iDFt_compute(N, DFt):
    return log(N/DFt)

def RSV_compute(documents, index, term):
    '''
    k1: positive tuning parameter that calibrates the document term frequency scaling
        0: binary model (no term frequency)
        large value: using raw term frequency
    '''
    k1 = 0
    '''
    b: tuning parameter determining the scaling by document length (0 <= b <= 1)
        0: no document length normalization
        1: fully scaling the term weight by the document length
    '''
    b = 0

    # get other parameters
    N = N_compute(documents)
    DFt = DFt_compute(index, term)
    TFtd_index = TFtd(index)
    LDave = LDave_compute(documents)
    LD_dict = LD(documents)

    # compute weighting
    iDFt = iDFt_compute(N, DFt)
    # k1
    # b

    return