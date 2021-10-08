set -e

# ウェブサイトに反映するためのexcelを作成する

python 100_create_excel_ippan.py
python 101_create_excel_tokutei.py