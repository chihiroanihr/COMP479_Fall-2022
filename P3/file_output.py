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
            output_file.write(str(term_docId[0]) + ": " + term_docId[1] + "\n")

    elif subproj_step.endswith('indexer'):
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
    
    elif subproj_step == 'tftd':
        output_file.write("{dictionary: ALL[documentID, term frequency]}\n")
        output_file.write("--------------------\n")
        for term, tftd in result.items():
            output_file.write(term + ": ")
            output_file.write(str(tftd))
            output_file.write("\n")

    else:
        output_file.write(str(result))

    output_file.close()