"""
Copyright 1999 Illinois Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL ILLINOIS INSTITUTE OF TECHNOLOGY BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of Illinois Institute
of Technology shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Software without prior written
authorization from Illinois Institute of Technology.
"""

import os
import glob
import fabio
import numpy as np
from PIL import Image
from os.path import split
from tif_compressor import __version__
from tif_compressor.modules.pyqt_utils import *

input_types = ['tif', 'tiff']

class viewerGUI(QMainWindow):
    """
    A class for GUI of Image Merger
    """
    def __init__(self):
        """
        Initial window
        """
        QWidget.__init__(self)
        self.img_list = []
        self.img_grps = []
        self.stop_process = False
        self.initUI()
        self.setConnections()

    def initUI(self):
        """
        initial all widgets
        """
        self.setWindowTitle("TIFF Compressor-Decompressor v." + __version__)
        self.centralWid = QWidget(self)
        self.setCentralWidget(self.centralWid)
        self.mainLayout = QGridLayout(self.centralWid)

        self.in_directory = QLineEdit()
        self.select_in_folder = QPushButton("File")
        self.in_directory = QLineEdit()
        self.select_in_folder_folder = QPushButton("Folder")
        # self.out_directory = QLineEdit()
        # self.select_out_folder = QPushButton("Browse")

        self.detailGrp = QGroupBox("Logs")
        self.detailLayout = QVBoxLayout(self.detailGrp)
        self.detail = QPlainTextEdit()
        self.detail.setReadOnly(True)
        self.progressbar = QProgressBar()
        self.detailLayout.addWidget(self.detail)
        self.detailLayout.addWidget(self.progressbar)

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)

        self.compressChkBx = QCheckBox("Check to COMPRESS/Uncheck to DECOMPRESS")
        self.compressChkBx.setChecked(False)

        self.mainLayout.addWidget(QLabel("Input Directory : "), 0, 0, 1, 1)
        self.mainLayout.addWidget(self.in_directory, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.select_in_folder, 0, 2, 1, 1)
        self.mainLayout.addWidget(self.select_in_folder_folder, 0, 3, 1, 1)

        # self.mainLayout.addWidget(QLabel("Output Directory : "), 1, 0, 1, 1)
        # self.mainLayout.addWidget(self.out_directory, 1, 1, 1, 1)
        # self.mainLayout.addWidget(self.select_out_folder, 1, 2, 1, 1)

        self.mainLayout.addWidget(self.compressChkBx, 3, 0, 1, 4)

        self.mainLayout.addWidget(self.detailGrp, 4, 0, 1, 4)
        self.mainLayout.addWidget(self.start_button, 5, 0, 1, 4, Qt.AlignCenter)

        self.mainLayout.columnStretch(1)
        self.mainLayout.rowStretch(3)
        self.resize(800, 400)
        self.show()

    def setConnections(self):
        """
        Set handler for all widgets
        """
        self.select_in_folder.clicked.connect(self.browse_input)
        self.select_in_folder_folder.clicked.connect(self.browse_input_folder)
        # self.select_out_folder.clicked.connect(self.browse_output)
        self.start_button.toggled.connect(self.start_clicked)

    def browse_input(self):
        """
        Handle when Browse for input folder is clicked
        :return:
        """
        path = getAFile()
        if len(path) > 0:
            self.in_directory.setText(path)
            dir_path, _ = split(str(path))
            # self.out_directory.setText(join(dir_path, 'converted_tiffs'))
            QApplication.processEvents()

    def browse_input_folder(self):
        """
        Handle when Browse for input folder is clicked
        :return:
        """
        path = getAFolder()
        if len(path) > 0:
            self.in_directory.setText(path)
            dir_path = path
            # self.out_directory.setText(join(dir_path, 'converted_tiffs'))
            QApplication.processEvents()

    # def browse_output(self):
    #     """
    #     Handle when Browse for output folder is clicked
    #     :return:
    #     """
    #     path = getAFolder()
    #     if len(path) > 0:
    #         self.out_directory.setText(path)

    def start_clicked(self):
        """
        handle when Start is clicked
        :return:
        """
        if self.start_button.text() == 'Start':
            self.stop_process = False
            self.start_button.setText("Stop")
            self.in_directory.setEnabled(False)
            self.select_in_folder.setEnabled(False)
            # self.out_directory.setEnabled(False)
            # self.select_out_folder.setEnabled(False)
            self.compressChkBx.setEnabled(False)
            self.progressbar.reset()
            self.progressbar.setHidden(False)
            # createFolder(str(self.out_directory.text()))
            self.processFile()
        else:
            self.stop_process = True

    def processFile(self):
        """
        converting images
        :return:
        """
        if os.path.isdir(self.in_directory.text()):
            files = [os.path.join(self.in_directory.text(), file) for file in os.listdir(self.in_directory.text())]
        else:
            files = glob.glob(self.in_directory.text())
        n = len(files)
        compress = self.compressChkBx.isChecked()
        # outpath = self.out_directory.text()
        if compress:
            self.detail.insertPlainText('\nCompressing TIFF Files...')
            self.detail.moveCursor(QTextCursor.End)
            QApplication.processEvents()
            print('Compressing TIFF Files...')

        else:
            self.detail.insertPlainText('\nDecompressing TIFF Files...')
            self.detail.moveCursor(QTextCursor.End)
            QApplication.processEvents()
            print('Decompressing TIFF Files...')
        
        for i, f in enumerate(files):
            if isImg(f):
                if self.stop_process:
                    break
                self.detail.insertPlainText(f'\nProcessing {f}...')
                self.detail.moveCursor(QTextCursor.End)
                QApplication.processEvents()

                self.compress_tiff_files(f, compress)
                self.log_progress(i, n)

                self.detail.insertPlainText(f' [DONE]')
                self.detail.moveCursor(QTextCursor.End)
                QApplication.processEvents()

        self.progressbar.setValue(100)
        self.detail.insertPlainText('\n------------------------------ Completed ------------------------------')
        self.detail.moveCursor(QTextCursor.End)
        self.stop_process = False
        QApplication.processEvents()

        QApplication.restoreOverrideCursor()
        self.detail.moveCursor(QTextCursor.End)
        self.detail.insertPlainText("\nDone. All images have been processed.")
        QApplication.processEvents()
        self.start_button.setChecked(False)
        self.start_button.setText('Start')
        self.in_directory.setEnabled(True)
        self.select_in_folder.setEnabled(True)
        # self.out_directory.setEnabled(True)
        # self.select_out_folder.setEnabled(True)
        self.compressChkBx.setEnabled(True)

    def log_progress(self, progress, total):
        """
        Print the progress in the terminal
        :param progress, total:
        :return: -
        """
        per = int(progress * 100 / total)
        self.progressbar.setValue(per)
        QApplication.processEvents()
        print('\r[{1:>3}%  {0:40}]'.format('#' * int(40*per/100), per), end='')
        if per >= 100:
            print(' [DONE]')

    def compress_tiff_files(self, fn, compress):
        """
        Decompress/compress tiff files.
        :param im, path, prefix:
        :return: -
        """
        with Image.open(fn) as im:
            if compress:
                im.save(fn, compression='tiff_lzw')
            else:
                data = np.array(im)
                fabio.tifimage.tifimage(data=data).write(fn)

def compress_tiff_files_headless(fn, compress):
    """
    Decompress/compress tiff files.
    :param im, path, prefix:
    :return: -
    """
    with Image.open(fn) as im:
        if compress:
            print(f'Compressing TIFF File {fn}...')
            im.save(fn, compression='tiff_lzw')
        else:
            print(f'Decompressing TIFF File {fn}...')
            data = np.array(im)
            fabio.tifimage.tifimage(data=data).write(fn)
        print('Done.')

def isImg(fileName):
    """
    Check if a file name is an image file
    :param fileName: (str)
    :return: True or False
    """
    nameList = fileName.split('.')
    return nameList[-1] in input_types
