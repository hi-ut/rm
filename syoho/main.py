import json
import requests
import argparse
from kanjize import int2kanji, kanji2int

def getValue(item, field):
    obj = item[field]
    return obj["ja"] if "ja" in obj else obj["en"]

def getMonth(date):
    return int(date[1]) if len(date) > 1 else 99

parser = argparse.ArgumentParser()
parser.add_argument('year', help='year, etc: 2020')

args = parser.parse_args()

targetYear = int(args.year)

with open('data/{}.json'.format(targetYear)) as f:
    df = json.load(f)

kans = '〇一二三四五六七八九'

# 関数(1)_漢数字（例：二三五六〇一）を単純変換する関数
def kan2num(text):
    for i, tmp in enumerate(kans):
        text = text.replace(tmp, str(i)) # replaceメソッドで置換
    return text

for item in df:
    if len(item["課題の概要"]) == 0:
        continue

    money = item["研究経費"]
    money = kan2num(money)

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
    

    output = '''研究課題　{title}
研究経費　{money}　
研究組織
　研究代表者　　　{main}
　所内共同研究者　{sub_in}
　所外共同研究者　{sub_out}
研究の概要
（１）課題の概要
{abst}

（２）研究の成果
{output}'''.format(**values)

    Html_file= open("{}/html/{}.txt".format(targetYear, no),"w")
    Html_file.write(output)
    Html_file.close()