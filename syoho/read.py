import docx
import argparse
import json
import os
import requests

parser = argparse.ArgumentParser()
parser.add_argument('type', help='type, etc: tokutei')
parser.add_argument('year', help='year, etc: 2020')

args = parser.parse_args()

type_ = args.type
targetYear = int(args.year)

url = "https://script.google.com/macros/s/AKfycbzOXX4-GmW1GWevQBV5R1xSxP9WAcDec4VnVfNVFbaOV4F-M1v1oV8ls9gewUxUEtc0Ew/exec?sheet={}".format("一般" if type_ == "ippan" else "特定")
df = requests.get(url).json()

for i in range(len(df)):
    item = df[i]
    
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

    opath = "{}/{}/所報/{}_{}.docx".format(targetYear, type_, str(i+1).zfill(2), no)
    os.makedirs(os.path.dirname(opath), exist_ok=True)
    doc.save(opath)