# Copyright (c) 2018 Robert J Sammelson - All Rights Reserved

from backend import processOptions, timeFilesManager


def initBackend():
    processOptions.loadOpts()
    timeFilesManager.load()


def initGUI():
    pass
