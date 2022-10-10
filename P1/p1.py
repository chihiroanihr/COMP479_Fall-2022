import os
import json
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords


# Pipeline[1]: read all sgm data files
def extract_documents_from_corpus(sgm_file):
    documents = {}  # list of documents extracted
    NUM_DOCUMENTS = 0  # total number of documents in corpus (from all the sgm files)

    # pass the file to BeautifulSoup
    soup = BeautifulSoup(sgm_file, 'html.parser')
    # find all content with <REUTERS> tag (returns a list of each doc/article)
    file_contents = soup.find_all("reuters") # not get confused with "Reuter"

    # extracrt all documents(articles) from the file
    for content in file_contents:
        title = content.find("title")
        title = title.text if title else ""
        body = content.find("body")
        body = body.text if body else ""
        # form a text
        text = title + " " + body

        # assign document ID and make a dictionary of documents
        documents[NUM_DOCUMENTS] = text

        # count number of docs
        NUM_DOCUMENTS += 1

    print(str(NUM_DOCUMENTS) + " documents have been successfully extracted.")

    return documents


# Pipeline[2]: tokenize and generate postings
def tokenize(documents, filename):
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
    
    print("Current number of postings in file " + filename + ": " + str(len(n_postings)))

    return postings


# Pipeline[3]: make all texts lowercase in the postings, and update / re-assign the postings list
def lowercase(postings, filename):
    n_postings = [] # new postings list

    for doc_id, word in postings:
        if isinstance(word, str):
            word = word.lower()
        n_postings.append((doc_id, word))

    print("Current number of postings in file " + filename + ": " + str(len(n_postings)))

    return n_postings


# Pipeline[4]: apply porter stemmer on postings
def porter_stemmer(postings, filename):
    stemmer = PorterStemmer()
    n_postings = []

    for doc_id, word in postings:
        word = stemmer.stem(word)
        n_postings.append((doc_id, word))

    print("Current number of postings in file " + filename + ": " + str(len(n_postings)))

    return n_postings


# Pipeline[5]: give a list of stop words and remove those from the text
def remove_stop_words(postings, stop_words, filename):
    n_postings = []
    num_postings_removed = 0
    
    for doc_id, word in postings:
        if word in stop_words:
            num_postings_removed += 1
            continue
        
        n_postings.append((doc_id, word))

    print(str(num_postings_removed) + " postings have been removed.")
    print("Current number of postings in file " + filename + ": " + str(len(n_postings)))

    return n_postings


# document result output function
def file_output(documents, num_sgm_files, pipeline_step, output_directory):
    try:
        os.makedirs(output_directory)
        print("Output directory created.")
    except FileExistsError:
        pass

    output_filename = os.path.join(output_directory, "pipeline" + str(pipeline_step) + "_file(" + str(num_sgm_files)+").txt")
    output_file = open(output_filename, "w")

    if pipeline_step == 1:
        output_file.write(json.dumps(documents, indent=4))
    else:
        for posting in documents:
            output_file.write(str(posting) + "\n")

    output_file.close()


# create stop words list to be used for pipeline[5]
def create_stop_words_list():
    STOP_WORDS = []
    print("Default stop words offered by NLTK library: \n" + str(set(stopwords.words('english'))))
    # input validation & decide stop words
    while True:
        option = input("\nYou can use either:\n\t(1) Default stop words offered by NLTK libray, or\n\t(2) Enter stop words manually\nEnter the option number: ")
        try:
            value = int(option)
        except ValueError:
            print("ERROR! Enter valid option number again.")
            continue
        if value == 1:
            STOP_WORDS = set(stopwords.words('english'))
            break
        elif value == 2:
            words = input("Enter stop words separated by spaces: ")
            STOP_WORDS = words.split(" ")
            print("Stop words entered are: \n" + str(STOP_WORDS))
            break
        else:
            print("ERROR! Enter valid option number again.")
    
    return STOP_WORDS


# pipline function
def pipeline(directory, output_directory='', test=False, max_sgm_files=-1):
    PIPELINE_STEP = 0  # pipeline step number requied for output file name
    NUM_SGM_FILES = 0  # number of sgm files read from reuters21578

    # first, decide list of stop words to be used for all documents
    stop_words = create_stop_words_list()

    # iterate all the files inside the folder
    for file in os.listdir(directory):
        # [DEMO] numeber of maximum files to be retrived is set for testing purpose
        if test and NUM_SGM_FILES == max_sgm_files:
            break

        # if not sgm file then skip
        if not file.endswith(".sgm"):
            continue
        # if sgm file, count sgm files
        NUM_SGM_FILES += 1

        # open the file to be read
        filename = os.path.join(directory, file)
        sgm_file = open(filename, 'r', encoding='utf-8', errors='ignore') # avoid UnicodeDecodeError with 'r'

        # start the pipeline step
        print("\nFile #(" + str(NUM_SGM_FILES) + ")")
        print("* * * * * * * * * * * * * * * *  Pipeline [1]  * * * * * * * * * * * * * * * *")
        print("Description: Read Reuter's collection, extract the raw text of each article from the corpus")
        PIPELINE_STEP = 1
        documents = extract_documents_from_corpus(sgm_file, filename)
        # [DEMO] output the result
        if test and output_directory:
            file_output(documents, NUM_SGM_FILES, PIPELINE_STEP, OUTPUT_DIRECTORY)

        print("* * * * * * * * * * * * * * * *  Pipeline [2]  * * * * * * * * * * * * * * * *")
        print("Description: Tokenize each article")
        PIPELINE_STEP = 2
        postings = tokenize(documents, filename)
        # [DEMO] output the result
        if test and output_directory:
            file_output(postings, NUM_SGM_FILES, PIPELINE_STEP, OUTPUT_DIRECTORY)

        print("* * * * * * * * * * * * * * * *  Pipeline [3]  * * * * * * * * * * * * * * * *")
        print("Description: Make all text loewrcase")
        PIPELINE_STEP = 3
        postings = lowercase(postings, filename)
        # [DEMO] output the result
        if test and output_directory:
            file_output(postings, NUM_SGM_FILES, PIPELINE_STEP, OUTPUT_DIRECTORY)

        print("* * * * * * * * * * * * * * * *  Pipeline [4]  * * * * * * * * * * * * * * * *")
        print("Description: Apply Porter Stemmer")
        PIPELINE_STEP = 4
        postings = porter_stemmer(postings, filename)
        # [DEMO] output the result
        if test and output_directory:
            file_output(postings, NUM_SGM_FILES, PIPELINE_STEP, OUTPUT_DIRECTORY)

        print("* * * * * * * * * * * * * * * *  Pipeline [5]  * * * * * * * * * * * * * * * *")
        print("Description: Given a list of stop words, remove those from the texts")
        PIPELINE_STEP = 5
        postings = remove_stop_words(postings, stop_words, filename)
        # [DEMO] output the result
        if test and output_directory:
            file_output(postings, NUM_SGM_FILES, PIPELINE_STEP, OUTPUT_DIRECTORY)



### FOR TESTING PURPOSE ###
DIRECTORY = "../reuters21578_extracted/"
OUTPUT_DIRECTORY = "outputs_test/"
MAX_SGM_FILES = 5  # [DEMO] for testing purpose
pipeline(DIRECTORY, OUTPUT_DIRECTORY, True, MAX_SGM_FILES)

### DEFAULT START ###
'''
DIRECTORY = "../reuters21578_extracted/"
OUTPUT_DIRECTORY = "outputs_default/"
pipeline(DIRECTORY)
'''