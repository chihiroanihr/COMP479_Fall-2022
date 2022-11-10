import json
import os


# P3 result output function
def file_output(result, subproj_step, output_directory, query_dict={}):
    # create directory first
    try:
        os.makedirs(output_directory)
    except FileExistsError:
        pass

    # create and open file
    output_filename = os.path.join(output_directory, subproj_step + ".txt")
    output_file = open(output_filename, "w")

    # append data to file
    if subproj_step == 'test_corpus':
        output_file.write("(term: documentID)\n")
        output_file.write("------------------\n")
        for term_docId in result:
            output_file.write(str(term_docId[0]) + ": " + str(term_docId[1]) + "\n")

    elif subproj_step.endswith('indexer') or subproj_step.endswith('indexer_with_dup'):
        output_file.write("{dictionary: posting lists}\n")
        output_file.write("---------------------------\n")
        for term, postings in result.items():
            output_file.write(term + ": ")
            count_posting = len(postings)
            for posting in postings:
                if count_posting == 1:
                    output_file.write(str(posting))
                else:
                    output_file.write(str(posting) + " -> ")
                count_posting -= 1
            output_file.write("\n")
    
    elif subproj_step == 'time_analysis':
        output_file.write("Execution time for Naive indexer and SPIMI indexer\n\n")
        output_file.write("Naive Indexer: " + str(result['naive']) + " seconds\n")
        output_file.write("SPIMI Indexer: " + str(result['spimi']) + " seconds\n")
        output_file.write("\n")
        output_file.write("Naive Indexer allowing duplicate term-docID pairs: " + str(result['naive_dup']) + " seconds\n")
        output_file.write("SPIMI Indexer allowing duplicate term-docID pairs: " + str(result['spimi_dup']) + " seconds\n")

    elif subproj_step.startswith('ranked_query'):
        output_file.write("Query Search:\n")
        output_file.write(str(query_dict['str_query']) + "\n\n")
        output_file.write("Query Tokens:\n")
        output_file.write(str(query_dict['tokens']) + "\n\n")
        output_file.write("\n")
        output_file.write("k1 = " + str(query_dict['k1']) + "\n")
        output_file.write("b = " + str(query_dict['b']) + "\n\n")
        output_file.write("{documentID: score}\n")
        output_file.write("-------------------\n")
        for docID, score in result.items():
            output_file.write(str(docID) + ": " + str(score) + "\n")

    elif subproj_step.startswith('AND_query'):
        output_file.write("Query Search:\n")
        output_file.write(str(query_dict['str_query']) + "\n\n")
        output_file.write("Query Tokens:\n")
        output_file.write(str(query_dict['tokens']) + "\n\n")
        output_file.write("\n")
        output_file.write(str(result['message']) + "\n\n")
        output_file.write("List of retrieved documentIDs: \n")
        output_file.write("-----------------------------\n")
        output_file.write(json.dumps(result['postings'], indent=4))
        # for docID in result['postings']:
        #     output_file.write(str(docID) + "\n")

    elif subproj_step.startswith('OR_query'):
        output_file.write("Query Search:\n")
        output_file.write(str(query_dict['str_query']) + "\n\n")
        output_file.write("Query Tokens:\n")
        output_file.write(str(query_dict['tokens']) + "\n\n")
        output_file.write("\n")
        output_file.write(str(result['message']) + "\n\n")
        output_file.write("Ranked list of retrieved documentIDs: \n")
        output_file.write("{documentID: # queries found}\n")
        output_file.write("-----------------------------\n")
        output_file.write(json.dumps(result['ranked_postings'], indent=4))
        # for docID, num_queries in result['ranked_postings'].items():
        #     output_file.write(str(docID) + ": " + str(num_queries) + "\n")

        # output_file.write("\n")
        # output_file.write("List of retrieved documentIDs: \n")
        # output_file.write("--------------------\n")
        # for docID in result['postings']:
        #     output_file.write(str(docID) + "\n")

    else:
        output_file.write(json.dumps(result, indent=4))

    output_file.close()