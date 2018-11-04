import random

import PyQt5
import qdarkstyle
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QGridLayout,
                             QHBoxLayout, QHeaderView, QLabel, QPushButton,
                             QSizePolicy, QTableWidget, QTableWidgetItem,
                             QTabWidget, QVBoxLayout, QWidget)

import backend.processOptions as opts
import backend.timeFilesManager as timeManager

currentTable = None
lastSelectedRow = None


def initGUI():
    app = QApplication([])
    app.setStyle('Fusion')
    if opts.timeclockOpts["darkTheme"]:
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    window = QWidget()
    window.setWindowTitle(opts.timeclockOpts["title"])
    window.setWindowIcon(QtGui.QIcon(
        "../data/assets/" + opts.timeclockOpts["logo"]))
    mainLayout = QVBoxLayout()
    mainLayout.setSpacing(20)

    mainLayout.addLayout(makeTitle())
    mainLayout.addWidget(makeNameArea())
    mainLayout.addLayout(makeActions())

    window.setLayout(mainLayout)
    window.show()
    print("1024  x  768")
    print(window.width(), " x ", window.height())
    print(1024 - window.width(), "\t", 768 - window.height())
    app.exec_()


def makeTitle():
    titleLayout = QHBoxLayout()
    # titleLayout.setSpacing(42)
    titleFont = QtGui.QFont("Times", 32, QtGui.QFont.Bold)

    title = QLabel(opts.timeclockOpts["title"])
    title.setFixedWidth(820)
    title.setFont(titleFont)

    logo = QLabel()
    logoImage = QtGui.QPixmap("../data/assets/" + opts.timeclockOpts["logo"])
    logoImage = logoImage.scaled(QtCore.QSize(100, 100))
    logo.setPixmap(logoImage)
    if opts.timeclockOpts["darkTheme"]:
        logo.setStyleSheet("QLabel {background:white}")

    titleLayout.addWidget(title)
    titleLayout.addStretch()
    titleLayout.addWidget(logo)
    return titleLayout


def makeNameArea():
    tabs = QTabWidget()
    tabs.setStyleSheet(
        "QTabBar::tab {width: 110px; height:40px} QTabBar::scroller{width:50px;}")

    tab = makeNamelist(timeManager.nameList)
    global currentTable
    currentTable = tab
    tabs.addTab(tab, opts.timeclockOpts["teams"][0])
    for i in opts.timeclockOpts["teams"][1:]:
        tab = makeNamelist(timeManager.nameList)
        tabs.addTab(tab, i)

    def setCurrentTable():
        global currentTable
        global lastSelectedRow
        if lastSelectedRow != None:
            for i in range(currentTable.columnCount()):
                currentTable.item(lastSelectedRow, i).setSelected(False)
        lastSelectedRow = None
        currentTable = tabs.currentWidget()
    tabs.currentChanged.connect(setCurrentTable)

    return tabs


def makeTableItem(text):
    item = QTableWidgetItem()
    item.setText(text)
    item.setFlags(Qt.ItemIsEnabled)
    item.setFlags(Qt.ItemIsSelectable)
    return item


def makeNamelist(names):
    namesTable = QTableWidget()
    namesTable.setFixedSize(994, 450)  # 451
    namesTable.setRowCount(len(names))  # NAMES
    namesTable.setColumnCount(4)
    namesTable.setShowGrid(False)
    namesTable.verticalScrollBar().setStyleSheet(
        "QScrollBar:vertical{width: 60px;}")
    namesTable.verticalHeader().hide()
    ntPalette = namesTable.palette()
    ntPalette.setColor(QtGui.QPalette.Text, Qt.black)
    namesTable.setPalette(ntPalette)

    def setLastRow(r, *args):
        global lastSelectedRow
        for i in range(namesTable.columnCount()):
            if lastSelectedRow != None:
                namesTable.item(lastSelectedRow, i).setSelected(False)
            namesTable.item(r, i).setSelected(True)
        lastSelectedRow = r
    namesTable.cellClicked.connect(setLastRow)

    headers = ["Name", "Graph", "Hours", "I/O"]
    for header in range(len(headers)):
        headItem = QTableWidgetItem()
        headItem.setText(headers[header])
        namesTable.setHorizontalHeaderItem(header, headItem)

    for i in range(namesTable.rowCount()):
        nameItem = makeTableItem(names[i])
        namesTable.setItem(i, 0, nameItem)
        #
        graphItem = makeTableItem("█" * random.randrange(0, 25))
        graphFont = graphItem.font()
        graphFont.setStretch(25)
        graphFont.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 0)
        graphItem.setFont(graphFont)
        namesTable.setItem(i, 1, graphItem)
        #
        hoursItem = makeTableItem(str(random.randrange(0, 99999)))
        namesTable.setItem(i, 2, hoursItem)
        #
        ioItem = makeTableItem(random.choice(["i", "o", "i", "o", "a"]))
        ioFont = QtGui.QFont("Courier New", 14)
        ioFont.setBold(True)
        if ioItem.text() != "i" and ioItem.text() == "o":
            ioItem.setForeground(QtGui.QBrush(Qt.red))
        ioItem.setFont(ioFont)
        ioItem.setTextAlignment(Qt.AlignRight)
        namesTable.setItem(i, 3, ioItem)

    namesTable.setVisible(False)
    namesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    namesTable.setColumnWidth(1, 100)
    namesTable.resizeColumnToContents(2)
    namesTable.resizeColumnToContents(3)
    namesTable.setVisible(True)
    return namesTable


def makeActions():
    actionsLayout = QGridLayout()
    actionsLayout.setVerticalSpacing(5)

    actionsLayout.setRowMinimumHeight(0, 30)
    actionsLayout.setRowMinimumHeight(1, 18)
    actionsLayout.setRowMinimumHeight(2, 50)

    signI = QPushButton("IN")
    signO = QPushButton("OUT")
    signI.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    signI.setStyleSheet(
        'QPushButton {background-color: green; color: white; font-size: 28pt; font-weight: bold}')
    signO.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    signO.setStyleSheet(
        'QPushButton {background-color: red; color: white; font-size: 28pt; font-weight: bold}')

    def doIO(io):
        if currentTable != None and lastSelectedRow != None:
            timeManager.signIO(currentTable.item(
                lastSelectedRow, 0).text(), io)
        else:
            print("No item", currentTable != None, lastSelectedRow != None)

    signI.clicked.connect(lambda: doIO("i"))
    signO.clicked.connect(lambda: doIO("o"))

    more = QPushButton("More...")
    newUser = QPushButton("New User")
    graph = QPushButton("Graph")
    quit = QPushButton("Quit")
    more.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    newUser.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    graph.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    quit.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
    more.setStyleSheet('QPushButton {font-weight: bold}')
    quit.setStyleSheet('QPushButton {color: red}')

    actionsLayout.addWidget(signI, 0, 0, 3, 2)
    actionsLayout.addWidget(signO, 0, 2, 3, 2)
    actionsLayout.addWidget(more, 0, 4, 2, 1)
    actionsLayout.addWidget(newUser, 2, 4)
    actionsLayout.addWidget(graph, 0, 5)
    actionsLayout.addWidget(quit, 2, 5)
    return actionsLayout
