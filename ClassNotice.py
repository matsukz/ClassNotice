import json
import datetime
import schedule
import time

print("===DAYSTART===")
print(datetime.datetime.now())

NowDate = datetime.date.today()
loadjson = open(
        "classcopy.json",
        "r",
        encoding="utf-8"
    )

impjson = json.load(loadjson)
        

print("DB:IMPJSON")
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
print(Today)

loadjson.close()

global ClassNo
ClassNo = 1
global StopFlag
StopFlag = 0

def CheckTime():
    global ClassNo
    global StopFlag
    print("===== " + str(ClassNo) + " =====")
    Now = datetime.datetime.now().strftime("%H%M")
    print("NowTime = " + Now)
    try:
        if impjson[Today][str(ClassNo)]["Time"] == "END":
            print("END")
            StopFlag = 1
                
        elif impjson[Today][str(ClassNo)]["Time"] == Now:
            print(impjson[Today][str(ClassNo)]["Class"])
            ClassNo = ClassNo + 1

        else:
            print("NOT MATCH")

    except TypeError:
        print("SKIP NULL")
        ClassNo = ClassNo + 1

schedule.every(1).minutes.do(CheckTime)

while StopFlag == 0:
    schedule.run_pending()
    time.sleep(1)       
#schedule.every().day.at("00:05").do(DAY)

#while DayLoop == True:
#    schedule.run_pending()
#    time.sleep(1)
