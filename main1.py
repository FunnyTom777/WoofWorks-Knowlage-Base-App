# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
from datetime import datetime

# ------------------- Main Window -------------------
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WoofWorks Knowledge Base")
        self.resize(594, 330)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Label
        self.label = QtWidgets.QLabel("WoofWorks Knowledge Base (Powered By Uranium)", self.centralwidget)
        self.label.setGeometry(60, 10, 441, 31)
        font = QtGui.QFont("FiraCode Nerd Font Mono Med", 12)
        self.label.setFont(font)

        # Buttons
        self.pushButton = QtWidgets.QPushButton("New Entry", self.centralwidget)
        self.pushButton.setGeometry(90, 80, 121, 131)
        self.pushButton.clicked.connect(self.open_new_entry)

        self.pushButton_2 = QtWidgets.QPushButton("View Entries", self.centralwidget)
        self.pushButton_2.setGeometry(220, 80, 121, 131)
        self.pushButton_2.clicked.connect(self.open_view_entries)

        self.pushButton_3 = QtWidgets.QPushButton("Quit", self.centralwidget)
        self.pushButton_3.setGeometry(350, 80, 121, 131)
        self.pushButton_3.clicked.connect(self.close)

    def open_new_entry(self):
        self.new_entry_window = NewEntryWindow()
        self.new_entry_window.show()

    def open_view_entries(self):
        self.view_entries_window = ViewEntriesWindow()
        self.view_entries_window.show()


# ------------------- New Entry Window -------------------
class NewEntryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("New Entry")
        self.resize(557, 605)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Labels
        font = QtGui.QFont("FiraCode Nerd Font", 12, QtGui.QFont.Bold)
        self.label = QtWidgets.QLabel("Entry Name:", self.centralwidget)
        self.label.setGeometry(20, 80, 131, 16)
        self.label.setFont(font)

        self.label_2 = QtWidgets.QLabel("Entry Date:", self.centralwidget)
        self.label_2.setGeometry(20, 120, 131, 16)
        self.label_2.setFont(font)

        self.label_3 = QtWidgets.QLabel("Entry Category:", self.centralwidget)
        self.label_3.setGeometry(20, 160, 161, 16)
        self.label_3.setFont(font)

        self.label_4 = QtWidgets.QLabel("Entry:", self.centralwidget)
        self.label_4.setGeometry(20, 200, 131, 16)
        self.label_4.setFont(font)

        self.label_5 = QtWidgets.QLabel("New Entry", self.centralwidget)
        self.label_5.setGeometry(240, 10, 131, 16)
        font_big = QtGui.QFont("FiraCode Nerd Font", 12, QtGui.QFont.Bold)
        self.label_5.setFont(font_big)

        # Inputs
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)  # Entry Name
        self.lineEdit.setGeometry(140, 80, 401, 20)

        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)  # Entry Date
        self.lineEdit_3.setGeometry(140, 120, 401, 20)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)  # Category
        self.comboBox.setGeometry(190, 160, 351, 22)
        self.comboBox.addItems([
            "Coding", "WoofWorks", "Games", "Work", "Progects",
            "Creations", "Misc", "To-Do", "Unknown"
        ])

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)  # Entry Text
        self.textEdit.setGeometry(80, 200, 461, 291)

        # Buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(380, 530, 156, 23)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.save_entry)
        self.buttonBox.rejected.connect(self.close)

    def save_entry(self):
        entry_name = self.lineEdit.text().strip()
        entry_date = self.lineEdit_3.text().strip()
        entry_category = self.comboBox.currentText()
        entry_text = self.textEdit.toPlainText().strip()

        if not entry_name:
            QtWidgets.QMessageBox.warning(self, "Error", "Entry name cannot be empty!")
            return

        if not entry_date:
            entry_date = datetime.now().strftime("%Y-%m-%d")

        os.makedirs("entries", exist_ok=True)
        safe_name = "".join(c for c in entry_name if c.isalnum() or c in ("_", "-")).rstrip()
        filename = f"entries/{safe_name}_{entry_date}.entry"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Name: {entry_name}\n")
            f.write(f"Date: {entry_date}\n")
            f.write(f"Category: {entry_category}\n")
            f.write("Entry:\n")
            f.write(entry_text)

        QtWidgets.QMessageBox.information(self, "Saved", f"Entry saved as:\n{filename}")
        self.close()


# ------------------- View Entries Window -------------------
class ViewEntriesWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Entries")
        self.resize(530, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        font = QtGui.QFont("FiraCode Nerd Font", 12, QtGui.QFont.Bold)
        self.label_5 = QtWidgets.QLabel("View Entry's", self.centralwidget)
        self.label_5.setGeometry(200, 20, 131, 16)
        self.label_5.setFont(font)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(30, 70, 481, 391)
        self.listWidget.itemDoubleClicked.connect(self.view_entry)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(360, 530, 156, 23)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.close)
        self.buttonBox.rejected.connect(self.close)

        self.load_entries()

    def load_entries(self):
        self.listWidget.clear()
        if not os.path.exists("entries"):
            os.makedirs("entries")

        files = [f for f in os.listdir("entries") if f.endswith(".entry")]
        if not files:
            self.listWidget.addItem("No entries found.")
            self.listWidget.setEnabled(False)
        else:
            self.listWidget.setEnabled(True)
            for file in sorted(files):
                self.listWidget.addItem(file)

    def view_entry(self, item):
        filename = os.path.join("entries", item.text())
        if not os.path.isfile(filename):
            QtWidgets.QMessageBox.warning(self, "Error", "File not found.")
            return

        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("Entry Viewer")
        msg.setText(f"File: {item.text()}")
        msg.setDetailedText(content)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()


# ------------------- Run Application -------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
