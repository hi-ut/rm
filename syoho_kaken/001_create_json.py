import docx
import json
import os
import requests
from kanjize import int2kanji, kanji2int

url = "https://script.google.com/macros/s/AKfycbz3sM-WB7c4CoQfNPeTCS1a6lZp-GZxYmD803gUj5nYRrt8b8bl-v_62RgYIo-gSHo2/exec"

df = requests.get(url).json()

kans = '〇一二三四五六七八九'

def int2kan(text):
    text = str(text)
    conv_text = ""
    for i in range(len(text)):
        word = text[i:i+1]
        try:
            num = int(word)
            conv_text += kans[num:num+1]
        except:
            conv_text += word
    return conv_text

for i in range(len(df)):
    item = df[i]

    value = {
        "research_title" : item["タイトル"],
        "research_category" : item["研究費種目"],
        "project_number" : int2kan(item["課題番号"]),
        "period_start": int2kan(item["開始"]),
        "period_end": int2kan(item["終了"]),
        "direct_cost": int2kanji(int(item["直接経費"])),
        "indirect_cost": int2kanji(int(item["間接経費"])),
        "principal_investigator": item["研究代表者"],
        "outline": item["研究の概要"].replace("\r\n", "").replace("\r", "").replace("\n", ""),
    }

    year = item["年度"]

    opath = "data/json/{}_{}_{}.json".format(year, item["課題番号"], item["研究代表者"].replace(" ", "").replace("　", ""))

    os.makedirs(os.path.dirname(opath), exist_ok=True)

    with open(opath, 'w') as outfile:
        json.dump(value,  outfile, ensure_ascii=False,
        indent=4, sort_keys=True, separators=(',', ': '))