# Copyright (c) 2018 Robert J Sammelson - All Rights Reserved

import os

loadOptions = True

try:
    import rapidjson
except ImportError as e:
    print("Please install the rapidjson library so the so the options file can be loaded.")
    loadOptions = False

defaultOptions = {"title": "Timeclock", "logo": "time.png", "darkTheme": False, "addHoursBeforeSignout": True,
                  "ioForm": "%H:%M:%S %d.%m.%Y", "pathTime": "./times/", "autoClockOut": "00:00:00",
                  "autoClockLim": "04:30:00", "usernameFile": "usernameFile.txt", "adminPass": "",
                  "seasons": {"Build": {"start": "00:00:00 06.01.2018", "end": "23:59:59 20.02.2018", "hoursPerWeek": 0},
                              "Competition": {"start": "00:00:00 21.03.2018", "end": "23:59:59 14.04.2018", "hoursPerWeek": 0}},
                  "positions": ["Student", "Mentor", "Adult", "Other"],
                  "teams": ["Programming", "Mechanical", "Media", "Woodworking", "Mentors", "Other"]}

jsonFile = "../data/opts.json"


def loadOpts():
    opts = {}
    if loadOptions:
        os.chdir(os.path.dirname(__file__))
        if not os.path.exists(jsonFile):
            generateDefaultOpts()
        with open(jsonFile) as optsFile:  # load options
            opts = rapidjson.load(optsFile)
    else:
        opts = defaultOptions

    global timeclockOpts
    timeclockOpts = opts


def generateDefaultOpts():
    print("generated opts")

    os.chdir(os.path.dirname(__file__))
    with open(jsonFile, "w") as optsFile:
        rapidjson.dump(defaultOptions, optsFile, indent=2)
