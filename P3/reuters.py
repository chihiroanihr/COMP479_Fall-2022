import os
from bs4 import BeautifulSoup
from nltk import word_tokenize


# Retrieve only sgm files from the corpus
def filter_files(directory, max_sgm_files=-1):
    NUM_SGM_FILES = 0  # number of sgm files read from reuters21578
    sgm_files = []

    print("(1) Collecting Reuters files...")

    # iterate all the files inside the folder
    for file in os.listdir(directory):
        # [DEMO] numeber of maximum files to be retrived is set for testing purpose
        if NUM_SGM_FILES == max_sgm_files:
            break

        # if not sgm file then skip
        if not file.endswith(".sgm"):
            continue
        # if sgm file, count sgm files
        NUM_SGM_FILES += 1

        filename = os.path.join(directory, file)
        sgm_files.append(filename)
    
    return sgm_files


# Extract raw texts from corpus
def extract_documents_from_corpus(sgm_files):
    documents = {}  # list of documents extracted
    NUM_DOCUMENTS = 0  # total number of documents in corpus (from all the sgm files)

    print("(2) Reading and extracting documents from Reuters files...")

    # iterate all the files inside the folder
    for filename in sgm_files:
        # open the file to be read
        sgm_file = open(filename, 'r', encoding='utf-8', errors='ignore') # avoid UnicodeDecodeError with 'r'
        print(" * Reading " + filename + " *")

        # pass the file to BeautifulSoup
        soup = BeautifulSoup(sgm_file, 'html.parser')
        # find all content with <REUTERS> tag (returns a list of each doc/article)
        file_contents = soup.find_all("reuters") # not get confused with "Reuter"

        # extracrt all documents(articles) from the file
        for content in file_contents:
            docID = int(content['newid'])
            title = content.find("title")
            title = title.text if title else ""
            body = content.find("body")
            body = body.text if body else ""
            # form a text
            text = title + " " + body

            # assign document ID and make a dictionary of documents
            documents[docID] = text

            # count number of docs
            NUM_DOCUMENTS += 1

    print('  - ' + str(NUM_DOCUMENTS) + ' documents have been successfully extracted.')

    return documents


# Tokenize and generate list of term-docID pairs
def tokenize(documents):
    term_docID_pairs = []
    
    print("(3) Tokenizing all documents...")

    for docId, text in documents.items():
        for token in word_tokenize(text):
            # remove all the special characters and punctuations
            token = ''.join(e for e in token if token.isalnum())
            # remove empty tokens
            if not token:
                continue
            # generate docId-term pairs
            term_docID_pairs.append((token, docId))
    
    print('  - Number of term-docId pairs: ' + str(len(term_docID_pairs)))

    return term_docID_pairs


# Make test corpus to be used for indexing
def make_test_corpus(term_docId_pairs, max_terms=0):

    # [DEMO] Use only 10K terms for testing purpose
    if max_terms:
        print("(4) Reduced the number of terms in test corpus to " + str(max_terms) + ".")
        return term_docId_pairs[:max_terms]
    else:
        return term_docId_pairs