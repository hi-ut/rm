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

for item in df:
    if len(item["研究の概要"]) == 0:
        continue

    money = int(item["研究経費"])
    # money = int2kanji(money)
    money = str(money)+"円"
    
    values = {
        "title": item["研究課題名"],
        "money": money,
        "main": item["研究代表者"],
        "sub_in": item["所内共同研究者"],
        "sub_out": item["所外共同研究者"],
        "abst": item["（１）課題の概要"],
        "output": item["（２）研究の成果"]
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

    print(output)



'''
for key in out_activity:
    if len(out_activity[key]) > 0:
        rows.append("〔{}〕{}\n".format(key, "／".join(out_activity[key])))

f = open("{}_{}.txt".format(id, targetYear), 'w') # 書き込みモードで開く
f.writelines(rows) # シーケンスが引数。
f.close()

'''