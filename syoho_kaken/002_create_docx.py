import json
import argparse
import os
from docx import Document
from docxcompose.composer import Composer
import glob
import docx

parser = argparse.ArgumentParser()
parser.add_argument('--year', help='year, etc: 2020')

args = parser.parse_args()
targetYear = int(args.year) if args.year else "*"

files = glob.glob("data/json/{}_*.json".format(targetYear))

for file in files:

    item = json.load(open(file))
    doc = docx.Document("template.docx")

    for para in doc.paragraphs:
        text = para.text
        for key in item:
            target = "{"+key+"}"
            if target in text:
                text = text.replace(target, item[key])

        para.text = text

    opath = file.replace("json", "docx")
    os.makedirs(os.path.dirname(opath), exist_ok=True)
    doc.save(opath)