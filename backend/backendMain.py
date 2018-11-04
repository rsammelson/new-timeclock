from backend import processOptions, timeFilesManager


def initBackend():
    processOptions.loadOpts()
    timeFilesManager.load()


def initGUI():
    pass
