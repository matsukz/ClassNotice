import json
import datetime

dt = datetime.date.today()

impjson = json.load(
    open(
        "class.json",
        "r",
        encoding="utf-8"
    )
)
Week = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]

# 今日の曜日からJsonから引用するデータの位置を決める
i = 0
while not list(impjson.keys())[i] == Week[dt.weekday()]:
    i = i + 1
Today = list(impjson.keys())[i]

print(impjson[Today])
