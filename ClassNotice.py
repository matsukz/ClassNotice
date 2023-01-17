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
    "Fri"
]

SearchDate = Week[dt.weekday()]

print(impjson[list(impjson.keys())[dt.weekday()]]["1"]["Class"])

#print(SearchDate)

#while key == SearchDate:

#print(key)

#print(impjson[str(dt.weekday())]["10:50"])
