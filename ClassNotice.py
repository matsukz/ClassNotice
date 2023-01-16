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

dList = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri"
]

SearchDate = dList[dt.weekday()]

print(SearchDate)
#print(impjson[str(dt.weekday())]["10:50"])