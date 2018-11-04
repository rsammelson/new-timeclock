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
    for i in opts.timeclockOpts["teams"]:
        tab = makeNamelist(timeManager.nameList)
        tabs.addTab(tab, i)
    return tabs


def makeNamelist(names):
    table = QTableWidget()
    table.setFixedSize(994, 450)  # 451
    table.setRowCount(len(names))  # NAMES
    table.setColumnCount(4)
    table.setShowGrid(False)
    table.verticalScrollBar().setStyleSheet(
        "QScrollBar:vertical{width: 60px;}")
    table.verticalHeader().hide()
    headers = ["Name", "Graph", "Hours", "I/O"]
    for header in range(len(headers)):
        headItem = QTableWidgetItem()
        headItem.setText(headers[header])
        table.setHorizontalHeaderItem(header, headItem)
    for i in range(table.rowCount()):
        nameItem = QTableWidgetItem()
        nameItem.setText(names[i])
        nameItem.setFlags(Qt.ItemIsEnabled)
        table.setItem(i, 0, nameItem)
        #
        graphItem = QTableWidgetItem()
        graphItem.setText("█" * random.randrange(0, 25))
        graphItem.setFlags(Qt.ItemIsEnabled)
        graphFont = graphItem.font()
        # graphFont.setPointSize(3.5)
        graphFont.setStretch(25)
        graphFont.setLetterSpacing(QtGui.QFont.AbsoluteSpacing, 0)
        graphItem.setFont(graphFont)
        table.setItem(i, 1, graphItem)
        #
        hoursItem = QTableWidgetItem()
        hoursItem.setText(str(random.randrange(10000, 99999)))
        hoursItem.setFlags(Qt.ItemIsEnabled)
        table.setItem(i, 2, hoursItem)
        #
        ioItem = QTableWidgetItem()
        ioItem.setText(random.choice(["i", "o"]))
        ioItem.setFlags(Qt.ItemIsEnabled)
        ioItem.setTextAlignment(Qt.AlignRight)
        table.setItem(i, 3, ioItem)
    table.setVisible(False)
    table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    table.setColumnWidth(1, 100)
    table.resizeColumnToContents(2)
    table.resizeColumnToContents(3)
    table.setVisible(True)
    return table


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
