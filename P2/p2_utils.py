import os
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# Beginning: retrieve only sgm files from the corpus
def filter_corpus(directory, max_sgm_files=-1):
    NUM_SGM_FILES = 0  # number of sgm files read from reuters21578
    sgm_files = []

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


# [P1_1]: read all sgm data files
def extract_documents_from_corpus(sgm_file, filename=''):
    documents = {}  # list of documents extracted
    NUM_DOCUMENTS = 0  # total number of documents in corpus (from all the sgm files)

    # pass the file to BeautifulSoup
    soup = BeautifulSoup(sgm_file, 'html.parser')
    # find all content with <REUTERS> tag (returns a list of each doc/article)
    file_contents = soup.find_all("reuters") # not get confused with "Reuter"

    # extracrt all documents(articles) from the file
    for content in file_contents:
        docID = content['newid']
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

    if filename:
        print('  - ' + str(NUM_DOCUMENTS) + ' documents have been successfully extracted from file "' + filename + '".')
    else:
        print('  - ' + str(NUM_DOCUMENTS) + ' documents have been successfully extracted.')

    return documents


# [P1_2]: tokenize and generate postings
def tokenize(documents, filename=''):
    postings = []
    
    for doc_id, text in documents.items():
        for token in word_tokenize(text):
            # remove all the special characters and punctuations
            token = ''.join(e for e in token if token.isalnum())
            # remove empty tokens
            if not token:
                continue
            # generate postings
            postings.append((doc_id, token))
    
    if filename:
        print('  - Number of postings in file "' + filename + '": ' + str(len(postings)))
    else:
        print('  - Number of postings: ' + str(len(postings)))

    return postings


# [P1_3]: make all texts lowercase in the postings, and update / re-assign the postings list
def lowercase(postings, filename=''):
    n_postings = [] # new postings list

    for doc_id, word in postings:
        if isinstance(word, str):
            word = word.lower()
        n_postings.append((doc_id, word))

    if filename:
        print('  - Number of postings in file "' + filename + '": ' + str(len(n_postings)))

    return n_postings


# [P1_4]: apply porter stemmer on postings
def porter_stemmer(postings, filename=''):
    stemmer = PorterStemmer()
    n_postings = []

    for doc_id, word in postings:
        word = stemmer.stem(word)
        n_postings.append((doc_id, word))

    if filename:
        print('  - Number of postings in file "' + filename + '": ' + str(len(n_postings)))

    return n_postings


# [P1_5]: give a list of stop words and remove those from the text
def remove_stop_words(postings, used_stop_words, filename=''):
    n_postings = []
    num_postings_removed = 0
    
    for doc_id, word in postings:
        if word in used_stop_words:
            num_postings_removed += 1
            continue
        
        n_postings.append((doc_id, word))

    print("  - " + str(num_postings_removed) + " postings have been removed due to stop words.")
    if filename:
        print('  - Number of postings in file "' + filename + '": ' + str(len(n_postings)))

    return n_postings

# create stop words list to be used for pipeline[5]
def create_stop_words_list(required_length=''):
    used_stop_words = []
    default_stop_words = list(set(stopwords.words('english')))

    if required_length:
        used_stop_words = default_stop_words[:required_length]
    else:
        used_stop_words = default_stop_words
    
    # record list of stopwords used for reference
    file_output_used_stopwords(default_stop_words, used_stop_words, required_length)

    return used_stop_words

# output used stop words in file for reference
def file_output_used_stopwords(default_stop_words, used_stop_words, required_length):
    dir_name = "stopwords_list/"
    filename = "stopwords_list_" + str(required_length) if required_length else "default_stop_words_list"
    path = os.path.join(dir_name, filename + ".txt")

    try:
        os.makedirs(dir_name)
    except FileExistsError:
        pass

    with open(path + ".txt", "w") as file:
        file.write("*** Default stop words offered by NLTK library ***\n")
        file.write("--------------------------------------------------\n")
        file.write('\n'.join(default_stop_words))
        file.write("\n\n")
        if required_length:
            file.write("*** " + str(required_length) + " stop words used from the library ***\n")
            file.write("--------------------------------------------\n")
            file.write('\n'.join(used_stop_words))


# [P2_1-2]: Sort list F and remove duplicates
def sort_postings(postings_list):
    # sort listings based on the term in ascending alphabetical order
    postings_list.sort(key = lambda posting: posting[1])

    return postings_list

def remove_duplicates(postings_list):
    # remove duplicates
    new_postings_list = list(set(postings_list))

    num_postings_removed = len(postings_list) - len(new_postings_list)
    print("  - " + str(num_postings_removed) + " postings have been removed due to duplicate.")

    # sort again since list got messy after removing duplicates
    new_postings_list = sort_postings(new_postings_list)

    return new_postings_list


# [P2_1-3]: Complete inverted index by splitting F into dictionary and pointer of postings
def inverted_index(postings_list):
    inverted_index = {} # empty inverted index

    for docID, term in postings_list:
        if term in inverted_index:
            # append docID to the existing term
            inverted_index[term].append(docID)
        else:
            inverted_index[term] = [docID]

    return inverted_index


# [P2_2-1]: Query search for sample queries in naive index
def query_search(query, inverted_index):
    # default search reseult is 0
    postings = []
    num_postings = 0
    # if query exist in the inverted index
    if query in inverted_index:
        postings = inverted_index[query]
        num_postings = len(postings)
    
    return (postings, num_postings)


# [P2_3-1]: Remove numbers from postings
def remove_numbers(postings, filename=''):
    n_postings = []
    num_postings_removed = 0
    
    for doc_id, word in postings:
        if word.isnumeric():
            num_postings_removed += 1
            continue
        
        n_postings.append((doc_id, word))

    print("  - " + str(num_postings_removed) + " postings have been removed due to numeric value.")
    if filename:
        print('  - Number of postings in file "' + filename + '": ' + str(len(n_postings)))

    return n_postings


# P2 result output function
def file_output(result, subproj_step, output_directory):
    try:
        os.makedirs(output_directory)
        print("Output directory created.")
    except FileExistsError:
        pass

    output_filename = os.path.join(output_directory, subproj_step + ".txt")
    output_file = open(output_filename, "w")

    # output [P2_1-1], [P2_1-2...]
    if subproj_step == 'P2_1-1' or 'P2_1-2' in subproj_step:
        output_file.write("(term: documentID)\n")
        output_file.write("--------------------\n")
        for posting in result:
            output_file.write(str(posting[1]) + ": " + posting[0] + "\n")

    # output [P2_2-1], [P2_3-1], [P2_3-2]
    elif subproj_step == 'P2_2-1' or subproj_step == 'P2_3-1' or subproj_step == 'P2_3-2':
        output_file.write(result)
    
    # output [P2_1-3], [P2_3-1_...]
    else:
        output_file.write("{dictionary: posting lists}\n")
        output_file.write("--------------------\n")
        for term, postings in result.items():
            output_file.write(term + ": ")
            count_posting = len(postings)
            for posting in postings:
                if count_posting == 1:
                    output_file.write(posting)
                else:
                    output_file.write(posting + " -> ")
                count_posting -= 1
            output_file.write("\n")

    output_file.close()