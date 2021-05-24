from docx import Document
from docxcompose.composer import Composer
import glob
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('type', help='type, etc: tokutei')
parser.add_argument('year', help='year, etc: 2020')

args = parser.parse_args()

type_ = args.type
targetYear = int(args.year)

files = glob.glob("{}/{}/所報/*.docx".format(targetYear, type_))

files = sorted(files)

for i in range(len(files)):
    file = files[i]
    if i == 0:
        master = Document(file)
        composer = Composer(master)
    else:
        doc1 = Document(file)
        composer.append(doc1)

master.save('{}/{}.docx'.format(targetYear, type_))