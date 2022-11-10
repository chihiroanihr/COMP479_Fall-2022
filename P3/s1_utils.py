import time
import filecmp


def remove_list_duplicates(postings):
    # remove duplicate docIDs by set, and sort again
    new_postings = list(set(postings))
    # count num of postings removed
    num_postings_removed = len(postings) - len(new_postings)

    print("  - " + str(num_postings_removed) + " postings have been removed due to duplicate.")

    return new_postings

def remove_index_duplicates(index):
    new_index = {}
    num_postings_removed = 0

    for term, postings in index.items():
        # remove duplicate docIDs by set, and sort again
        new_postings = list(set(postings)).sort(key = lambda i: i)
        new_index[term] = new_postings
        # count num of postings removed
        num_postings_removed += len(postings) - len(new_postings)

    print("  - " + str(num_postings_removed) + " postings have been removed due to duplicate.")

    return new_index

def create_inverted_index(test_corpus):
    index = {} # empty inverted index

    for term, docID in test_corpus:
        if term in index:
            # append docID to the existing term
            index[term].append(docID)
        else:
            index[term] = [docID] 

    return index


def naive_indexer(test_corpus, remove_duplicate=True):  
    startTime = time.time()

    # Remove duplicates
    if remove_duplicate:
        print("* Removing duplicates...")
        test_corpus = remove_list_duplicates(test_corpus)

    # Sort (based on the term in ascending alphabetical order and docID in ascending order)
    print("* Sorting list of term-docId pairs...")
    test_corpus.sort(key=lambda posting: (posting[0], posting[1]))

    # make inverted index
    print("* Creating inverted index...")
    index = create_inverted_index(test_corpus)

    endTime = time.time()
    elapsedTime = endTime - startTime

    print("--> Total number of distinct terms(type) in dictionary: " + str(len(index)))
    print("==> Execution Time: " + str(elapsedTime))

    return index, elapsedTime


def spimi_indexer(test_corpus, remove_duplicate=True):
    startTime = time.time()

    # Remove duplicates
    if remove_duplicate:
        print("* Removing duplicates...")
        test_corpus = remove_list_duplicates(test_corpus)

    # make inverted index
    print("* Creating inverted index...")
    index = create_inverted_index(test_corpus)
    
    # Sort (based on the term in ascending alphabetical order and docID in ascending order)
    print("* Sorting inverted index hash-table...")
    index = dict(sorted(index.items(), key=lambda x:(x[0], x[1].sort(key = lambda y: y))))

    endTime = time.time()
    elapsedTime = endTime - startTime

    print("--> Total number of distinct terms(type) in dictionary: " + str(len(index)))
    print("==> Execution Time: " + str(elapsedTime))

    return index, elapsedTime


def S1_test_identical(dir_name):
    if filecmp.cmp(dir_name + 'naive_indexer.txt', dir_name + 'spimi_indexer.txt'):
        print("Both Naive Indexer and Spimi Indexer results are identical.")
    else:
        print("Naive Indexer and Spimi Indexer results are NOT identical.")
