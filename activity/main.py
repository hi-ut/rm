import json
import requests
import argparse
import docx
import os

def getValue(item, field):
    if field not in item:
        return []
    obj = item[field]
    return obj["ja"] if "ja" in obj else obj["en"]

def getMonth(date):
    return int(date[1]) if len(date) > 1 else 99

def join(arr):
    return "／".join(arr)

parser = argparse.ArgumentParser()
parser.add_argument('hi_id', help='編纂所のid, etc: nakamura')
parser.add_argument('rm_id', help='research mapのid, etc: nakamura.satoru')
parser.add_argument('year', help='year, etc: 2020')

args = parser.parse_args()

rm_id = args.rm_id
hi_id = args.hi_id
targetYear = int(args.year)

df = requests.get("https://api.researchmap.jp/" + rm_id).json()

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

                authors = getValue(item, "authors")
                
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

            #要チェック
            if "from_date" not in item:
                continue

            from_date = item["from_date"].split("-")
            to_date = item["to_date"].split("-")

            from_year = int(from_date[0])
            to_year = int(to_date[0])

            if (targetYear >= from_year) or (targetYear < to_year):

                title = getValue(item, "research_project_title")

                authors = getValue(item, "investigators")
                
                author = []

                for a in authors:
                    author.append(a["name"])

                main_author = author[0] if len(author) > 0 else ""

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
            from_month = getMonth(from_date)
            to_year = int(to_date[0])
            to_month = int(to_date[1]) if len(to_date) > 1 else 99

            if (targetYear >= from_year and (from_month == 99 or from_month >= 4)) and (targetYear < to_year and (to_month < 4 or to_month == 99)):
                association = ""
                if "association" in item:
                    association = item["association"]["ja"]

                committee_name = item["committee_name"]["ja"]
            

                row = "{} {}".format(association, committee_name)

                rows.append(row)

gyosekiList = requests.get("https://hi-ut.github.io/assets/json/faculty/gyosekiList.json").json()
for item in gyosekiList:
    if item["label"] == hi_id:
        value = item["value"]
        gyoseki = {}
        for obj in value:
            label = obj["項目"]
            desc = obj["内容"]
            if label not in gyoseki:
                gyoseki[label] = []
            gyoseki[label].append(desc)

result["name"] = gyoseki["【氏名】"]
result["department"] = gyoseki["【所属】"]
result["position"] = gyoseki["【職位】"]
result["theme"] = gyoseki["【研究テーマ】"]
result["saiho"] = ["松尾大社での調査・撮影"]
result["gakunai"] = ["情報基盤センター", "学術資産アーカイブ化推進室"]
result["syonai"] = ["前近代日本史情報国際センター運営委員会", "電子計算機緊急対応チーム", "情報支援室"]
result["job"] = ["国立歴史民俗学博物館", "東京外国語大学 アジア・アフリカ言語文化研究所", "国立国会図書館"]

doc = docx.Document("template.docx")

for para in doc.paragraphs:
    text = para.text

    for key in result:
        target = "{"+key+"}"
        if target in text:
            text = text.replace(target, join(result[key]))

    para.text = text

opath = "data/{}/{}.docx".format(targetYear, hi_id)
os.makedirs(os.path.dirname(opath), exist_ok=True)
doc.save(opath)