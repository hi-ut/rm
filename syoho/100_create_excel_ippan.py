import json
import requests
import argparse
from kanjize import int2kanji, kanji2int
import os
import pandas as pd

types = ["ippan"] # ["ippan", "tokutei"]

targetYear = 2020

kans = '〇一二三四五六七八九'

# 関数(1)_漢数字（例：二三五六〇一）を単純変換する関数
def kan2num(text):
    for i, tmp in enumerate(kans):
        text = text.replace(tmp, str(i)) # replaceメソッドで置換
    return text

for type_ in types:

    url = "https://script.google.com/macros/s/AKfycbzOXX4-GmW1GWevQBV5R1xSxP9WAcDec4VnVfNVFbaOV4F-M1v1oV8ls9gewUxUEtc0Ew/exec?sheet={}".format("一般" if type_ == "ippan" else "特定")
    df = requests.get(url).json()

    rows = []
    row = ["no", "研究課題名","研究経費","研究代表者","所外共同研究者","所内共同研究者","研究協力者","研究の概要"]
    rows.append(row)

    for i in range(len(df)):
        item = df[i]
        
        if len(item["研究課題名"]) == 0:
            continue

        money = item["研究経費"]
        money = kan2num(money)

        abst = '''（１）課題の概要
        {}
 
（２）研究の成果
 {}'''.format(item["課題の概要"].strip(), item["研究の成果"].strip())

        row = [
            item["id"],
            item["研究課題名"],
            money,
            item["研究代表者"].strip(),
            item["所外共同研究者"].strip(),
            item["所内共同研究者"].strip(),
            "",
            abst,

        ]

        rows.append(row)
        

    opath = "{}/excel/{}.xlsx".format(targetYear, type_)


    df = pd.DataFrame(rows)
    df.to_excel(opath, index=False, header=False)