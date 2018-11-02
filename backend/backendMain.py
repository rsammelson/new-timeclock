import backend.processOptions


def initBackend():
    global timeclockOpts
    timeclockOpts = backend.processOptions.loadOpts()
