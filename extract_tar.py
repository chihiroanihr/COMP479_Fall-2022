import os
import tarfile

TAR_NAME = 'reuters21578'
TAR_NAME_EXTRACTED = TAR_NAME + '_extracted'

# if extracted directory already exists (folder was already extracted)
if not os.path.isdir(TAR_NAME_EXTRACTED):

    # open file
    file = tarfile.open(TAR_NAME + '.tar.gz')

    # extracting file to the given folder
    file.extractall('./' + TAR_NAME_EXTRACTED)

    file.close()

print('"' + TAR_NAME + '"' + " corpus is now available.")