import docx
import argparse
import json


parser = argparse.ArgumentParser()
parser.add_argument('year', help='year, etc: 2020')

args = parser.parse_args()

targetYear = int(args.year)

with open('data/{}.json'.format(targetYear)) as f:
    df = json.load(f)

for item in df:
    
    if len(item["課題の概要"]) == 0:
        continue

    money = item["研究経費"] # str(money)

    no = item["id"]
    
    values = {
        "title": item["研究課題名"].strip(),
        "money": money.strip(),
        "main": item["研究代表者"].strip(),
        "sub_in": item["所内共同研究者"].strip(),
        "sub_out": item["所外共同研究者"].strip(),
        "abst": item["課題の概要"].strip(),
        "output": item["研究の成果"].strip()
    }


    doc = docx.Document("template.docx")

    for para in doc.paragraphs:
        
        text = para.text

        for key in values:
            target = "{"+key+"}"
            if target in text:
                para.text = text.replace(target, values[key])

    doc.save("{}/所報/{}.docx".format(targetYear, no))