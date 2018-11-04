import rapidjson
from rapidjson import DM_ISO8601


def load():
    global nameList
    nameList = ["User " + str(i + 1) for i in range(15)]
    nameList.append(
        "User 11 who has an extremely long name that overfills the cell by a super large amount and whose name goes on and on")


def signIO(user, io):
    print(user, ":", io)
