import cv2
import sys
import os

import codecs
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *


class ImageShow(QGraphicsView):

    def __init__(self, imgs):
        super(ImageShow, self).__init__()
        self.idx = 0
        self.imgs = imgs
        self.showimg()

    def showimg(self):
        imgtest_file = self.imgs[self.idx]
        imgtest = cv2.imread(imgtest_file)  # read img BGR(0,255)
        logfn = imgtest_file.replace("imgs", "logs").replace("png", "txt")
        self.fout = codecs.open(logfn, 'w', encoding='utf-8')
        imgtest = cv2.cvtColor(imgtest, cv2.COLOR_BGR2RGB)  # BGR to RGB
        imgtest = cv2.resize(imgtest, (512, 512))
        x = imgtest.shape[1]
        y = imgtest.shape[0]
        print("%d, %d" % (imgtest.shape[1], imgtest.shape[0]))
        # self.setGeometry(0, 0, x, y)

        self.setWindowTitle("Image Show")

        self.setFixedSize(600, 600)
        frame = QtGui.QImage(imgtest, x, y, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(frame)
        self.item = QGraphicsPixmapItem(pix)
        self.scene = QGraphicsScene()
        self.scene.addItem(self.item)
        self.setScene(self.scene)
        self.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.show()

    def mousePressEvent(self, event):
        x = event.globalX() - self.geometry().x()
        y = event.globalY() - self.geometry().y()

        print("pressed")
        print("%d, %d" % (x, y))
        self.fout.write("%d,%d" % (x, y))

    def keyPressEvent(self, event):
        key = event.key()
        if key == 0x20:  # 空格键
            print("space")
            self.idx = self.idx + 1
            self.fout.close()
            self.showimg()
            self.fout.flush()
        if key == 0x51: # Q
            print(";")
            self.fout.write(";")
        if key == 0x57: # W
            print("next line")
            self.fout.write("\r\n")



def main():
    imgnfs = os.listdir("./imgs")

    print("%d" % len(imgnfs))
    imgfs = []
    for f in imgnfs:
        p = "./imgs/" + f
        imgfs.append(p)
    app = QApplication(sys.argv)

    is1 = ImageShow(imgfs)
    # is1.show()
    sys.exit(app.exec_())
    pass


if __name__ == '__main__':
    main()


