year=2021
gas=https://script.google.com/macros/s/AKfycbxnoyx_t15Ve7ItC8L3KspKBqOJAbYcAuqfmR6KjG7zasdGxyQ-65vhR39C6NX4xdxyxQ/exec
# python main.py ippan $year $gas
# python main.py tokutei $year $gas
python read.py ippan $year $gas
python read.py tokutei $year $gas
python combine.py ippan $year
python combine.py tokutei $year
