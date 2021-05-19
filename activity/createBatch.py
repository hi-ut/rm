import json
import requests

gyosekiList = requests.get("https://hi-ut.github.io/assets/json/faculty/gyosekiList.json").json()

map = {}

targetYear = 2020

for item in gyosekiList:
    id = item["label"]
    value = item["value"]
    gyoseki = {}
    for obj in value:
        label = obj["項目"]
        desc = obj["内容"]

        if label == "【URL】" and "researchmap" in desc:
            map[id] = desc.split("/")[3]

rows = []
for id in map:
    rows.append("python main.py {} {} {}\n".format(id, map[id], targetYear))

f = open('batch.sh', 'w') # 書き込みモードで開く
f.writelines(rows) # シーケンスが引数。
f.close()