import PyQt5.QtCore
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QMainWindow,
        QMessageBox, QTextEdit)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.curFile = ''

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()

        self.readSettings()

        self.textEdit.document().contentsChanged.connect(self.documentWasModified)

        self.setCurrentFile('')

    def closeEvent(self, event):
        if self.maybeSave():
            self.writeSettings()
            event.accept()
        else:
            event.ignore()

    def newFile(self):
        if self.maybeSave():
            self.textEdit.clear()
            self.setCurrentFile('')

    def open(self):
        if self.maybeSave():
            fileName, _ = QFileDialog.getOpenFileName(self)
            if fileName:
                self.loadFile(fileName)

    def save(self):
        if self.curFile:
            return self.saveFile(self.curFile)

        return self.saveAs()

    def saveAs(self):
        fileName, _ = QFileDialog.getSaveFileName(self)
        if fileName:
            return self.saveFile(fileName)

        return False

    def about(self):
        QMessageBox.about(self, "About Application",
                "The <b>Application</b> example demonstrates how to write "
                "modern GUI applications using Qt, with a menu bar, "
                "toolbars, and a status bar.")

    def documentWasModified(self):
        self.setWindowModified(self.textEdit.document().isModified())

    def createActions(self):
        root = PyQt5.QtCore.QFileInfo(__file__).absolutePath()

        self.newAct = QAction(QIcon(root + '/images/new.png'), " &New", self,
                shortcut=QKeySequence.New, statusTip="Create a new file",
                triggered=self.newFile)

        self.openAct = QAction(QIcon(root + '/images/open.png'), " &Open...",
                self, shortcut=QKeySequence.Open,
                statusTip="Open an existing file", triggered=self.open)

        self.saveAct = QAction(QIcon(root + '/images/save.png'), " &Save", self,
                shortcut=QKeySequence.Save,
                statusTip="Save the document to disk", triggered=self.save)

        self.saveAsAct = QAction(" &Save As...", self,
                shortcut=QKeySequence.SaveAs,
                statusTip="Save the document under a new name",
                triggered=self.saveAs)

        self.exitAct = QAction(" &Exit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)

        self.cutAct = QAction(QIcon(root + '/images/cut.png'), " &Cut", self,
                shortcut=QKeySequence.Cut,
                statusTip="Cut the current selection's contents to the clipboard",
                triggered=self.textEdit.cut)

        self.copyAct = QAction(QIcon(root + '/images/copy.png'), " &Copy", self,
                shortcut=QKeySequence.Copy,
                statusTip="Copy the current selection's contents to the clipboard",
                triggered=self.textEdit.copy)

        self.pasteAct = QAction(QIcon(root + '/images/paste.png'), " &Paste",
                self, shortcut=QKeySequence.Paste,
                statusTip="Paste the clipboard's contents into the current selection",
                triggered=self.textEdit.paste)

        self.aboutAct = QAction(" &About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QAction(" About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QApplication.instance().aboutQt)

        self.cutAct.setEnabled(False)
        self.copyAct.setEnabled(False)
        self.textEdit.copyAvailable.connect(self.cutAct.setEnabled)
        self.textEdit.copyAvailable.connect(self.copyAct.setEnabled)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu(" &File")
        self.fileMenu.addAction(self.newAct)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.saveAct)
        self.fileMenu.addAction(self.saveAsAct)
        self.fileMenu.addSeparator();
        self.fileMenu.addAction(self.exitAct)

        self.editMenu = self.menuBar().addMenu(" &Edit")
        self.editMenu.addAction(self.cutAct)
        self.editMenu.addAction(self.copyAct)
        self.editMenu.addAction(self.pasteAct)

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu(" &Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.newAct)
        self.fileToolBar.addAction(self.openAct)
        self.fileToolBar.addAction(self.saveAct)

        self.editToolBar = self.addToolBar("Edit")
        self.editToolBar.addAction(self.cutAct)
        self.editToolBar.addAction(self.copyAct)
        self.editToolBar.addAction(self.pasteAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def readSettings(self):
        settings = PyQt5.QtCore.QSettings("Trolltech", "Application Example")
        pos = settings.value("pos", PyQt5.QtCore.QPoint(200, 200))
        size = settings.value("size", PyQt5.QtCore.QSize(400, 400))
        self.resize(size)
        self.move(pos)

    def writeSettings(self):
        settings = PyQt5.QtCore.QSettings("Trolltech", "Application Example")
        settings.setValue("pos", self.pos())
        settings.setValue("size", self.size())

    def maybeSave(self):
        if self.textEdit.document().isModified():
            ret = QMessageBox.warning(self, "Application",
                    "The document has been modified.\nDo you want to save "
                    "your changes?",
                    QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)

            if ret == QMessageBox.Save:
                return self.save()

            if ret == QMessageBox.Cancel:
                return False

        return True

    def loadFile(self, fileName):
        file = PyQt5.QtCore.QFile(fileName)
        if not file.open(PyQt5.QtCore.QFile.ReadOnly | PyQt5.QtCore.QFile.Text):
            QMessageBox.warning(self, "Application",
                    "Cannot read file %s:\n%s." % (fileName, file.errorString()))
            return

        inf = PyQt5.QtCore.QTextStream(file)
        QApplication.setOverrideCursor(PyQt5.QtCore.Qt.WaitCursor)
        self.textEdit.setPlainText(inf.readAll())
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName)
        self.statusBar().showMessage("File loaded", 2000)

    def saveFile(self, fileName):
        file = PyQt5.QtCore.QFile(fileName)
        if not file.open(PyQt5.QtCore.QFile.WriteOnly | PyQt5.QtCore.QFile.Text):
            QMessageBox.warning(self, "Application",
                    "Cannot write file %s:\n%s." % (fileName, file.errorString()))
            return False

        outf = PyQt5.QtCore.QTextStream(file)
        QApplication.setOverrideCursor(PyQt5.QtCore.Qt.WaitCursor)
        outf << self.textEdit.toPlainText()
        QApplication.restoreOverrideCursor()

        self.setCurrentFile(fileName);
        self.statusBar().showMessage("File saved", 2000)
        return True

    def setCurrentFile(self, fileName):
        self.curFile = fileName
        self.textEdit.document().setModified(False)
        self.setWindowModified(False)

        if self.curFile:
            shownName = self.strippedName(self.curFile)
        else:
            shownName = 'untitled.txt'

        self.setWindowTitle("%s[*] - Application" % shownName)

    def strippedName(self, fullFileName):
        return PyQt5.QtCore.QFileInfo(fullFileName).fileName()


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
