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
    
    if len(item["研究の概要"]) == 0:
        continue

    money = int(item["研究経費"])
    # money = int2kanji(money)
    money = str(money)+"円"

    no = item["no"]
    
    values = {
        "title": item["研究課題名"],
        "money": money,
        "main": item["研究代表者"],
        "sub_in": item["所内共同研究者"],
        "sub_out": item["所外共同研究者"],
        "abst": item["（１）課題の概要"],
        "output": item["（２）研究の成果"]
    }


    doc = docx.Document("template.docx")

    for para in doc.paragraphs:
        
        text = para.text

        for key in values:
            target = "{"+key+"}"
            if target in text:
                para.text = text.replace(target, values[key])

    doc.save("output/{}/{}.docx".format(targetYear, no))