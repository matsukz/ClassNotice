import json

OpenJson = open(
    "Class.json",
    "r",
    encoding="utf-8"
)

impJson = json.load(OpenJson)

ClassNo = 1
Send = "本日の授業は\n"

for item in impJson["Mon"].values():
    if item["Class"] == "Finish":
        Send += "です。"
    elif item["Class"] == "END":
        Send = Send.rstrip(Send)
    elif item["Class"] is None:
        Send += (str(ClassNo) + "限目：空きコマ\n")
    else:
        Send += (str(ClassNo) + "限目：" + item["Class"] + "（" + item["Room"] + "）\n")
    ClassNo += 1

print(Send)