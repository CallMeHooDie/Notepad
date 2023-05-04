from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from notepad_ui import Ui_MainWindow
import sys


class Notepad(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPreview.triggered.connect(self.preview_file)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionQuit.triggered.connect(self.quit)

        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)
        self.actionDelete.triggered.connect(self.textEdit.clear)

        self.actionBold.triggered.connect(self.bold_text)
        self.actionItalic.triggered.connect(self.italic_text)
        self.actionUnderline.triggered.connect(self.underline_text)
        self.actionLeft.triggered.connect(self.left_text)
        self.actionRight.triggered.connect(self.right_text)
        self.actionCenter.triggered.connect(self.center_text)
        self.actionJustify.triggered.connect(self.justify_text)

        self.actionFont.triggered.connect(self.set_font)
        self.actionColor.triggered.connect(self.set_color)
        self.actionAbout_Me.triggered.connect(self.about_me)

    def save_file(self):
        if self.textEdit.document().isModified():
            filename = QFileDialog.getSaveFileName(self, "Save File", '/path/to/default/directory//', "*.txt")
            if filename[0]:
                with open(filename[0], 'w') as file:
                    txt = self.textEdit.toPlainText()
                    file.write(txt)
                    QMessageBox.about(self, "Save File", "File Saved")
        else:
            return False
        self.textEdit.document().setModified(False)

    def new_file(self):
        if not self.textEdit.document().isModified():
            return False
        msg = QMessageBox.warning(self, "NotePad", "Do you want to save changes?",
                                  QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |
                                  QMessageBox.StandardButton.Cancel)
        if self.textEdit.document().isModified():
            if msg == QMessageBox.StandardButton.Save:
                self.save_file()
                self.textEdit.clear()
            elif msg == QMessageBox.StandardButton.Discard:
                self.textEdit.clear()
            elif msg == QMessageBox.StandardButton.Cancel:
                return False

    def open_file(self):
        if not self.textEdit.document().isModified():
            file_name, ok = QFileDialog.getOpenFileNames(self, "Open File")
            if ok:
                with open(file_name[0], 'r') as file:
                    self.textEdit.clear()
                    self.textEdit.setText(file.read())
        elif self.textEdit.document().isModified():
            msg = QMessageBox.warning(self, "NotePad", "Do you want to save changes?",
                                      QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |
                                      QMessageBox.StandardButton.Cancel)
            if msg == QMessageBox.StandardButton.Save:
                self.save_file()
                file_name, ok = QFileDialog.getOpenFileNames(self, "Open File")
                if ok:
                    with open(file_name[0], 'r') as file:
                        self.textEdit.clear()
                        self.textEdit.setText(file.read())
            elif msg == QMessageBox.StandardButton.Discard:
                file_name, ok = QFileDialog.getOpenFileNames(self, "Open File")
                if ok:
                    with open(file_name[0], 'r') as file:
                        self.textEdit.clear()
                        self.textEdit.setText(file.read())
            elif msg == QMessageBox.StandardButton.Cancel:
                return False

    def print_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        print_dialog = QPrintDialog(printer)
        if print_dialog.exec() == QPrintDialog.DialogCode.Accepted:
            self.textEdit.print(printer)
        self.textEdit.document().setModified(False)

    def preview_file(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        print_dialog = QPrintPreviewDialog(printer, self)
        print_dialog.paintRequested.connect(self.preview_print_file)
        print_dialog.exec()

    def preview_print_file(self, printer):
        self.textEdit.print(printer)
        self.textEdit.document().setModified(False)

    def export_pdf(self):
        fn, ok = QFileDialog.getSaveFileName(self, "Export PDF", '/path/to/default/directory//', "*.pdf")
        if ok:
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)
        self.textEdit.document().setModified(False)

    def quit(self):
        if not self.textEdit.document().isModified():
            sys.exit()
        msg = QMessageBox.warning(self, "NotePad", "Do you want to save changes?",
                                  QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |
                                  QMessageBox.StandardButton.Cancel)
        if msg == QMessageBox.StandardButton.Save:
            self.save_file()
            sys.exit()
        elif msg == QMessageBox.StandardButton.Discard:
            sys.exit()
        elif msg == QMessageBox.StandardButton.Cancel:
            return False

    def bold_text(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def italic_text(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def underline_text(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def left_text(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def right_text(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignRight)

    def center_text(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def justify_text(self):
        self.textEdit.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def set_font(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def set_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textEdit.setTextColor(color)

    def about_me(self):
        QMessageBox.about(self, "Abot Me", "NotePad app\nHey, My nickname is HooDie\nDont forget to Star\n"
                                "Instagram: @call.me.hoodie")

    def closeEvent(self, event):
        if not self.textEdit.document().isModified():
            sys.exit()
        msg = QMessageBox.warning(self, "NotePad", "Do you want to save changes?",
                                  QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard |
                                  QMessageBox.StandardButton.Cancel)
        if msg == QMessageBox.StandardButton.Save:
            self.save_file()
            event.accept()
        elif msg == QMessageBox.StandardButton.Discard:
            self.close()
            event.accept()
        elif msg == QMessageBox.StandardButton.Cancel:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = Notepad()
    ui.show()
    sys.exit(app.exec())
