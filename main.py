import json
import requests
import argparse

def getValue(item, field):
    obj = item[field]
    return obj["ja"] if "ja" in obj else obj["en"]

def getMonth(date):
    return int(date[1]) if len(date) > 1 else 99

parser = argparse.ArgumentParser()
parser.add_argument('id', help='research mapのid')
parser.add_argument('year', help='year, etc: 2020')

args = parser.parse_args()

id = args.id
targetYear = int(args.year)

df = requests.get("https://api.researchmap.jp/" + id).json()

graphs = df["@graph"]

result = {}

for graph in graphs:
    type_ = graph["@type"]

    items = graph["items"]

    if type_ == "published_papers":

        rows = []
        result[type_] = rows

        for item in items:
            # print(item)

            date = item["publication_date"].split("-")

            year = int(date[0])

            month = int(date[1]) if len(date) > 1 else 99

            if (targetYear == year and month >= 4) or (targetYear + 1 == year and (month == 99 or month < 4)):

                
                title = getValue(item, "paper_title")

                authors = getValue(item, "authors")
                
                author = []

                for a in authors:
                    author.append(a["name"])

                publication_name = getValue(item, "publication_name")

                vol = ""
                if "volume" in item:
                    vol = "、Vol." + item["volume"]

                no = ""
                if "number" in item:
                    no = "、No." + item["number"]

                pp = ""
                if "starting_page" in item:
                    pp += item["starting_page"]
                if "ending_page" in item:
                    pp += "-"+item["ending_page"]

                if pp != "":
                    pp = "、pp." + pp

                referee = ""
                if "referee" in item and item["referee"]:
                    referee = "（査読有）"

                invited = ""
                if "invited" in item and item["invited"]:
                    invited = "（招待有）"

                row = "{}「{}」{}{}{}{}、{}年{}{}".format("・".join(author), title, publication_name, vol, no, pp, year, referee, invited)

                rows.append(row)

    elif type_ == "presentations":

        rows = []
        result[type_] = rows

        for item in items:
            # print(item)

            date = item["publication_date"].split("-")

            year = int(date[0])
            month = int(date[1])

            if (targetYear == year and month >= 4) or (targetYear + 1 == year and month < 4):

                title = item["presentation_title"]["ja"]

                authors = item["presenters"]["ja"]
                
                author = []

                for a in authors:
                    author.append(a["name"])

                publication_name = item["event"]["ja"]

                vol = ""
                if "volume" in item:
                    vol = "、Vol." + item["volume"]

                no = ""
                if "number" in item:
                    no = "、No." + item["number"]

                pp = ""
                if "starting_page" in item:
                    pp += item["starting_page"]
                if "ending_page" in item:
                    pp += "-"+item["ending_page"]

                if pp != "":
                    pp = "、pp." + pp

                referee = ""
                if "referee" in item and item["referee"]:
                    referee = "（査読有）"

                invited = ""
                if "invited" in item and item["invited"]:
                    invited = "（招待有）"

                row = "{}「{}」{}{}{}{}、{}年{}{}".format("・".join(author), title, publication_name, vol, no, pp, year, referee, invited)

                rows.append(row)

    elif type_ == "misc":

        rows = []
        result[type_] = rows

        for item in items:
            # print(item)

            date = item["publication_date"].split("-")

            year = int(date[0])
            month = getMonth(date)

            if (targetYear == year and month >= 4) or (targetYear + 1 == year and month < 4):

                title = item["paper_title"]["ja"]

                authors = item["authors"]["ja"]
                
                author = []

                for a in authors:
                    author.append(a["name"])

                publication_name = item["publication_name"]["ja"]

                vol = ""
                if "volume" in item:
                    vol = "、Vol." + item["volume"]

                no = ""
                if "number" in item:
                    no = "、No." + item["number"]

                pp = ""
                if "starting_page" in item:
                    pp += item["starting_page"]
                if "ending_page" in item:
                    pp += "-"+item["ending_page"]

                if pp != "":
                    pp = "、pp." + pp

                referee = ""
                if "referee" in item and item["referee"]:
                    referee = "（査読有）"

                invited = ""
                if "invited" in item and item["invited"]:
                    invited = "（招待有）"

                row = "{}「{}」{}{}{}{}{}{}、{}".format("・".join(author), title, publication_name, vol, no, pp, referee, invited, year)

                rows.append(row)

    elif type_ == "books_etc":

        rows = []
        result[type_] = rows

        for item in items:
            # print(item)

            date = item["publication_date"].split("-")

            year = int(date[0])
            
            month = int(date[1]) if len(date) > 1 else 99

            if (targetYear == year and month >= 4) or (targetYear + 1 == year and (month == 99 or month < 4)):

                title = item["book_title"]["ja"]

                authors = getValue(item, "authors")
                
                author = []

                for a in authors:
                    author.append(a["name"])

                publication_name = getValue(item, "publisher")

                total_page = ""
                if "total_page" in item:
                    total_page = "、" + item["total_page"]

                row = "{}「{}」{}{}、{}年".format("・".join(author), title, publication_name, total_page, year)

                rows.append(row)

    elif type_ == "research_projects":

        rows = []
        result[type_] = rows

        for item in items:

            from_date = item["from_date"].split("-")
            to_date = item["to_date"].split("-")

            from_year = int(from_date[0])
            to_year = int(to_date[0])

            if (targetYear >= from_year) or (targetYear < to_year):

                title = item["research_project_title"]["ja"]

                authors = item["investigators"]["ja"]
                
                author = []

                for a in authors:
                    author.append(a["name"])

                main_author = author[0]

                category = ""
                if "category" in item:
                    category = item["category"]["ja"]

                role = ""
                if "research_project_owner_role" in item and item["research_project_owner_role"] == "coinvestigator":
                    role = "研究分担者"

                row = "{}「{}」（研究代表者 {}）{}".format(category, title, main_author, role)

                rows.append(row)

    elif type_ == "committee_memberships":

        rows = []
        result[type_] = rows

        for item in items:

            from_date = item["from_date"].split("-")
            to_date = item["to_date"].split("-")

            from_year = int(from_date[0])
            from_month = int(from_date[1])
            to_year = int(to_date[0])
            to_month = int(to_date[1]) if len(to_date) > 1 else 99

            if (targetYear >= from_year and from_month >= 4) and (targetYear < to_year and (to_month < 4 or to_month == 99)):
                association = ""
                if "association" in item:
                    association = item["association"]["ja"]

                committee_name = item["committee_name"]["ja"]
            

                row = "{} {}".format(association, committee_name)

                rows.append(row)

for key in result:
    print("〔{}〕{}\n".format(key, "／".join(result[key])))

'''
f2 = open("test.json", 'w')
json.dump(result, f2, ensure_ascii=False, indent=4,sort_keys=True, separators=(',', ': '))
'''

text = ""

name = "中村覚"
org = "附属前近代日本史情報国際センター"
pos = "助教"
theme = "多様な情報の関連付けによる史料活用と研究環境の高度化に関する研究"

rows = []
rows.append("{}　{}　{}\n".format(name, org, pos))
rows.append("【研究活動】\n")
rows.append("研究テーマ　{}\n".format(theme))

if len(result["published_papers"]) > 0:
    rows.append("〔論文〕{}\n".format("／".join(result["published_papers"])))

if len(result["misc"]) > 0:
    rows.append("〔MISC〕{}\n".format("／".join(result["misc"])))

if len(result["books_etc"]) > 0:
    rows.append("〔書籍等出版物〕{}\n".format("／".join(result["books_etc"])))

if len(result["presentations"]) > 0:
    rows.append("〔講演・口頭発表等〕{}\n".format("／".join(result["presentations"])))

if len(result["research_projects"]) > 0:
    rows.append("〔科学研究費補助金による研究〕{}\n".format("／".join(result["research_projects"])))

rows.append("【所・学内業務】\n")

in_1 = {
    "史料採訪" : ["松尾大社での調査・撮影"],
}

for key in in_1:
    if len(in_1[key]) > 0:
        rows.append("〔{}〕{}\n".format(key, "／".join(in_1[key])))

rows.append("【所・学内行政】\n")

in_2 = {
    "学内" : ["情報基盤センター", "学術資産アーカイブ化推進室"],
    "所内" : ["前近代日本史情報国際センター運営委員会", "電子計算機緊急対応チーム", "情報支援室"]
}

for key in in_2:
    if len(in_2[key]) > 0:
        rows.append("〔{}〕{}\n".format(key, "／".join(in_2[key])))

rows.append("【学外活動】\n")

out_activity = {
    "教育" : [],
    "委員会" : result["committee_memberships"],
    "共同研究員" : ["国立歴史民俗学博物館", "東京外国語大学 アジア・アフリカ言語文化研究所", "国立国会図書館"]
}

for key in out_activity:
    if len(out_activity[key]) > 0:
        rows.append("〔{}〕{}\n".format(key, "／".join(out_activity[key])))

f = open("{}_{}.txt".format(id, targetYear), 'w') # 書き込みモードで開く
f.writelines(rows) # シーケンスが引数。
f.close()

