from os import error
from PySide2.QtCore import QObject
import cryptography
import urllib
import subprocess
import json
from subprocess import Popen,PIPE
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QWidget, QDialog, QScrollArea, QVBoxLayout, QLabel
from PySide2.QtUiTools import QUiLoader
from sqlalchemy import create_engine, inspect
from datetime import datetime
from cryptography.fernet import Fernet
from urllib.request import urlopen
from sqlalchemy.orm import sessionmaker
import pandas as pd
import numpy as np
import sys
import os
import time
import pymysql
import traceback
import base64
import requests
import glob
from fontTools.ttLib import TTFont
import re

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = QUiLoader().load('main.ui', parent)

class Main(MainWindow):
    def __init__(self):
        super(Main,self).__init__()
        self.initialize_instance_variable()
        self.configure_header()
        self.configure_footer()
        self.configure_pushButtonArena()
        self.check_win()

    def initialize_instance_variable(self):
        self.pushButtonArenaList = []
        self.turnCounter = 0
        self.lastPosition = None

    def configure_header(self):
        self.ui.timeLabel.setText("Time Left: Unlimited")
        self.ui.resetButton.clicked.connect(lambda: self.reset_game())
        self.ui.mainmenuButton.clicked.connect(lambda: self.messagebox_win("test"))

    def configure_footer(self):
        self.ui.statusLabel.setText("First to Five Pair Win!")

    def configure_pushButtonArena(self):
        if not self.pushButtonArenaList_exist(): #if the button already assigned into list
            for x,y in vars(self.ui).items():
                result = re.search("^pushButton_[0-9]+_[0-9]+",x)
                if not result is None:
                    z = {}
                    z["name"] = x
                    z["object"] = y
                    self.pushButtonArenaList.append(z)
            for x,_ in enumerate(self.pushButtonArenaList):
                self.pushButtonArenaList[x]["object"].clicked.connect(lambda *args , button=self.pushButtonArenaList[x] : self.pushButtonArenaHandler(button))

    def pushButtonArenaList_exist(self):
        if self.pushButtonArenaList:
            print("buttons already assigned")
            return True
        else:
            return False
            
    def pushButtonArenaHandler(self,button):
        if not button["object"].text():
            self.turnCounter += 1
            if self.turnCounter % 2 == 0:
                button["object"].setStyleSheet(
                u"QPushButton {color:rgb(0, 255, 255);}")
                button["object"].setText("O")
                self.lastPosition = button
                self.ui.turnLabel.setText("X Player Turn's")
                self.check_win()
            else:
                button["object"].setStyleSheet(
                u"QPushButton {color:rgb(255, 255, 0);}")
                button["object"].setText("X")
                self.lastPosition = button
                self.ui.turnLabel.setText("O Player Turn's")
                self.check_win()
    
    def reset_game(self):
        for x in self.pushButtonArenaList:
            x["object"].setText("")
        self.turnCounter = 0
        self.ui.turnLabel.setText("X Player Turn's")
        self.ui.statusLabel.setText("First to Five Pair Win!")
        self.enable_arena_button()

    def disable_arena_button(self):
        for x in self.pushButtonArenaList:
            x["object"].setEnabled(False)

    def enable_arena_button(self):
        for x in self.pushButtonArenaList:
            x["object"].setEnabled(True)

    def win(self,lastWord):
        self.ui.turnLabel.setText("Game Ended!")
        self.ui.statusLabel.setText("{} PLAYER WIN!".format(lastWord))
        self.disable_arena_button()
        self.messagebox_win(lastWord)

    def check_win(self):
        def check_horizontal(lastPosition,lastWord):
            wordSum = 1
            print("check_horizontal")
            currentPosition = [x for x in lastPosition]
            print("<<< check kiri")
            for _ in range(4):
                currentPosition[0] -= 1
                if currentPosition[0] < 0:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum == 5: 
                            self.win(lastWord)
                            break
            currentPosition = [x for x in lastPosition]
            print(">>> check kanan")
            for _ in range(4):
                currentPosition[0] += 1
                if currentPosition[0] > 10:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum >= 5: 
                            self.win(lastWord)
                            break
            print("WORD SUM ",wordSum)

        def check_vertical(lastPosition,lastWord):
            wordSum = 1
            print("check_vertical")
            currentPosition = [x for x in lastPosition]
            print("<<< check bawah")
            for _ in range(4):
                currentPosition[1] -= 1
                if currentPosition[1] < 0:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum == 5: 
                            self.win(lastWord)
                            break
            currentPosition = [x for x in lastPosition]
            print(">>> check atas")
            for _ in range(4):
                currentPosition[1] += 1
                if currentPosition[1] > 10:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum >= 5: 
                            self.win(lastWord)
                            break
            print("WORD SUM ",wordSum)

        def check_northwest_southeast(lastPosition,lastWord):
            wordSum = 1
            print("check_northwest_southeast")
            currentPosition = [x for x in lastPosition]
            print("<<< check northwest")
            for _ in range(4):
                currentPosition[0] -= 1
                currentPosition[1] -= 1
                if currentPosition[0] < 0 or currentPosition[1] < 0:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum == 5: 
                            self.win(lastWord)
                            break
            currentPosition = [x for x in lastPosition]
            print(">>> check souteast")
            for _ in range(4):
                currentPosition[0] += 1
                currentPosition[1] += 1
                if currentPosition[0] > 10 or currentPosition[1] > 10:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum >= 5: 
                            self.win(lastWord)
                            break
            print("WORD SUM ",wordSum)

        def check_northeast_southwest(lastPosition,lastWord):
            wordSum = 1
            print("check_northeast_southwest")
            currentPosition = [x for x in lastPosition]
            print("<<< check northeast")
            for _ in range(4):
                currentPosition[0] += 1
                currentPosition[1] -= 1
                if currentPosition[0] > 10 or currentPosition[1] < 0:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum == 5: 
                            self.win(lastWord)
                            break
            currentPosition = [x for x in lastPosition]
            print(">>> check soutwest")
            for _ in range(4):
                currentPosition[0] -= 1
                currentPosition[1] += 1
                if currentPosition[0] < 0 or currentPosition[1] > 10:
                    break
                else:
                    print("========={}=========".format(currentPosition))
                    button = [x for x in self.pushButtonArenaList if x["name"] == "{}_{}_{}".format("pushButton",str(currentPosition[0]),str(currentPosition[1]))][0]
                    if button["object"].text() != lastWord:
                        break
                    else:
                        wordSum +=1
                        if wordSum >= 5: 
                            self.win(lastWord)
                            break
            print("WORD SUM ",wordSum)

        if self.lastPosition != None:
            lastPosition = [int(x) for x in self.lastPosition["name"].split("_")[1:]]
            lastWord = self.lastPosition["object"].text()
            check_horizontal(lastPosition,lastWord)
            check_vertical(lastPosition,lastWord)
            check_northwest_southeast(lastPosition,lastWord)
            check_northeast_southwest(lastPosition,lastWord)

    def messagebox_win(self,x=""):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setText("Player '{}' Win!".format(x))
        msg.setInformativeText("you can reset the game or go back to main menu")
        msg.setWindowTitle("Congratulation")
        msg.exec_()

class Daemon():
    def __init__(self):
        self.app = None
        self.mainWindow = None
        self.exit_code = -15123123

    def run(self):
        if not QtWidgets.QApplication.instance():
            self.app = QtWidgets.QApplication(sys.argv)
        else:
            self.app = QtWidgets.QApplication.instance() 
        self.mainWindow = Main()
        self.mainWindow.ui.show()
        self.exit_code = (self.app.exec_())
        print(self.exit_code,"EXIT_CODE_REBOOT")

    def run_ui_template_only(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.mainWindow = MainWindow()
        self.mainWindow.ui.show()
        self.exit_code = (self.app.exec_())

d = Daemon()
d.run()