import json
import datetime
import schedule
import time

print("===START===")
print(datetime.datetime.now())
print("\n")

NowDate = datetime.date.today()

impjson = json.load(
    open(
        "classcopy.json",
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
while not list(impjson.keys())[i] == Week[NowDate.weekday()]:
    i = i + 1
Today = list(impjson.keys())[i]

i = 1

def CheckTime():
    global i
    print("===== " + str(i) + " =====")

    Now = datetime.datetime.now()
    NowTime = str(Now.hour) + str(Now.minute)
    print("NowTime = " + NowTime)

    try:
        print("JSON DATE Time = " + impjson[Today][str(i)]["Time"])

        if impjson[Today][str(i)]["Time"] == "END":
            print("END")
            print("====END====")
            exit()

        elif impjson[Today][str(i)]["Time"] == NowTime:
            print(impjson[Today][str(i)]["Class"])
            i = i + 1
            print("===Next " + str(i) + " ===")

        else:
            print("NOT MATCH")

    except TypeError:
        print("SKIP NULL")
        i = i + 1
        print("==============")
    
    print("\n")

schedule.every(1).minutes.do(CheckTime)

while True:
    schedule.run_pending()
    time.sleep(1)
