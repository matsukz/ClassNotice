import json
import datetime
import schedule

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

i = 0
while not list(impjson.keys())[i] == Week[dt.weekday()]:
    i = i + 1
Today = list(impjson.keys())[i]

i = 1
print("===START===")
while not impjson[Today][str(i)]["Class"] == "END":
    print(impjson[Today][str(i)]["Class"])
    i = i + 1
print("===END===")
