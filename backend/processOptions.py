import os

loadOptions = True

try:
    import rapidjson
except ImportError as e:
    print("Please install the rapidjson library so the so the options file can be loaded.")
    loadOptions = False

defaultOptions = {"title": "Timeclock", "logo": "time.png", "darkTheme": False, "addHoursBeforeSignout": True,
                  "pathTime": "./times/", "autoClockoutTime": "04:00:00", "adminPass": "",
                  "seasons": {"Build": {"start": "2020.01.04 00:00:00", "end": "2020.02.20 23:59:59", "hoursPerWeek": 0},
                              "Competition": {"start": "2020.02.20 23:59:59", "end": "2020.04.14 23:59:59", "hoursPerWeek": 0}},
                  "positions": ["Student", "Mentor", "Parent", "Other"],
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

    optsDir = os.path.split(jsonFile)[0]
    if not os.path.exists(optsDir):
        os.mkdir(optsDir)

    with open(jsonFile, "w") as optsFile:
        rapidjson.dump(defaultOptions, optsFile, indent=2)
