import json
import os


# P3 result output function
def file_output(result, subproj_step, output_directory):
    # create directory first
    try:
        os.makedirs(output_directory)
        print("Output directory created.")
    except FileExistsError:
        pass

    # create and open file
    output_filename = os.path.join(output_directory, subproj_step + ".txt")
    output_file = open(output_filename, "w")

    # append data to file
    if subproj_step == 'test_corpus':
        output_file.write("(term: documentID)\n")
        output_file.write("--------------------\n")
        for term_docId in result:
            output_file.write(str(term_docId[0]) + ": " + str(term_docId[1]) + "\n")

    elif subproj_step.endswith('indexer'):
        output_file.write("{dictionary: posting lists}\n")
        output_file.write("--------------------\n")
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

    else:
        output_file.write(json.dumps(result, indent=4))

    output_file.close()