# Created by: Wei-Cheng Lin, 2021/10/18

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow, QWidget
from PyQt5.QtGui import QImage
import cv2, imutils
import matplotlib.pyplot as plt
import numpy as np
import random
import math
# from haar import haar_2d



class Ui_MainWindow(QtWidgets.QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1088, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 461, 591))
        self.label.setText("")
        self.label.setWordWrap(False)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(500, 250, 81, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(500, 310, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(500, 370, 81, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(610, 30, 461, 591))
        self.label_2.setText("")
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(200, 630, 100, 35))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(700, 630, 320, 35))
        self.label_4.setObjectName("label_4")
    
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        self.label_2.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1088, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.filename = None # Will hold the image address location
        self.input = None # Hold input image
        self.output = None # Hold output image
        self.tmp = None # Will hold the temporary image for display
        self.hist = None # Hold image histogram
        self.gray = None # Hold grayscale image
        self.sigma = None # Gaussian noise sigma 
        self.layer = None # Layer of wavelet transform
        
        self.pushButton.clicked.connect(self.loadImage)
        self.pushButton_2.clicked.connect(self.wavelet)
        self.pushButton_3.clicked.connect(self.savePhoto)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def loadImage(self):
        self.filename = QFileDialog.getOpenFileName(filter="Images (*.png *.bmp *.jpg *.ppm)")[0]
        print(f"Read Image : {self.filename}")
        self.input = cv2.imread(self.filename)
        self.gray = cv2.cvtColor(self.input, cv2.COLOR_BGR2GRAY)
        self.tmp = self.input
        image = imutils.resize(self.tmp,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def get_hist(self):
        gray_img = self.gray.copy()
        self.hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
        fig = plt.figure()
        plt.plot(self.hist, color='blue')
        fig.canvas.draw()
        self.output = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        self.output  = self.output.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        self.tmp = self.output
        self.tmp = cv2.cvtColor(self.tmp, cv2.COLOR_RGB2BGR)
        frame = imutils.resize(self.output,width=500)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))       

    def wavelet(self):
        gray_img = self.gray.copy()
        resized_img = cv2.resize(gray_img, (512,512))
        wt = resized_img.copy()
        w, h = 512, 512
        self.layer,  _ = QtWidgets.QInputDialog.getText(
             self, 'Layers of wavelet transform', 'Enter number of layers:')
        self.layer = int(self.layer)  
        for layer in range(self.layer):
            b=0
            for i in range(0,w-1,2):
                a=0
                for j in range(0,h-1,2):
                    wt[a][b]=(resized_img[j][i]+resized_img[j+1][i]+resized_img[j][i+1]+resized_img[j+1][i+1])//4
                    wt[a+round(h/2)-1][b]=(resized_img[j][i]-resized_img[j+1][i]+resized_img[j][i+1]-resized_img[j+1][i+1])//4
                    wt[a][b+round(w/2)-1]=(resized_img[j][i]+resized_img[j+1][i]-resized_img[j][i+1]-resized_img[j+1][i+1])//4
                    wt[a+round(h/2)-1][b+round(w/2)-1]=(resized_img[j][i]-resized_img[j+1][i]-resized_img[j][i+1]+resized_img[j+1][i+1])//4
                    a=a+1
                b=b+1
            w=round(w/2)
            h=round(h/2)
            resized_img=wt.copy()    
        self.output = resized_img  
        self.tmp = self.output
        frame = imutils.resize(self.output,width=500)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_Grayscale8)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image))
    def gaussian(self):
        gray_img = self.gray.copy()

        ## adjust image shape 
        if gray_img.shape[0] % 2 !=0:
            gray_img = cv2.resize(gray_img,(gray_img.shape[1], gray_img.shape[0]-1))
        if gray_img.shape[1] % 2 !=0:
            gray_img = cv2.resize(gray_img,(gray_img.shape[1]-1, gray_img.shape[0]))
        print(self.input.shape, gray_img.shape)
        gray_gaussain = gray_img.copy()
        self.sigma,  _ = QtWidgets.QInputDialog.getText(
             self, 'Sigma', 'Enter a number:')
        print(f"Input Sigma: {self.sigma}")
        self.sigma = float(self.sigma)
        noise = []
        for i in range(gray_img.shape[0]):
            for j in range(0, gray_img.shape[1], 2):
                r = random.random()
                phi = random.random()
                z1 = self.sigma*(math.cos(2*math.pi*phi))*(math.sqrt((-2)*math.log(r)))
                z2 = self.sigma*(math.sin(2*math.pi*phi))*(math.sqrt((-2)*math.log(r)))
                gray_gaussain[i][j] += z1
                gray_gaussain[i][j+1] += z2
                noise.append(z1)
                noise.append(z2)
                if gray_gaussain[i][j] < 0:
                    gray_gaussain[i][j] = 0
                if gray_gaussain[i][j] > 255:
                    gray_gaussain[i][j] = 255                
                if gray_gaussain[i][j+1] < 0 :
                    gray_gaussain[i][j+1] = 0
                if gray_gaussain[i][j+1] > 255:
                    gray_gaussain[i][j+1] = 255
        self.tmp = gray_gaussain
        self.output = gray_gaussain
        gray_gaussain = imutils.resize(gray_gaussain,width=640)
        # frame = cv2.cvtColor(gray_gaussain, cv2.COLOR_BGR2RGB)
        image = QImage(gray_gaussain, gray_gaussain.shape[1],gray_gaussain.shape[0],gray_gaussain.strides[0], QImage.Format_Grayscale8)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label_3.setText("Output")
        print(len(noise))
        fig = plt.figure()
        plt.hist(noise,200, color='blue')
        fig.canvas.draw()        
        self.output = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        self.output  = self.output.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        frame = imutils.resize(self.output,width=500)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format_RGB888)
        self.label_2.setPixmap(QtGui.QPixmap.fromImage(image)) 

    def savePhoto(self):
        filename = QFileDialog.getSaveFileName(filter="Images (*.png *.bmp *.jpg *.ppm)")[0]
        cv2.imwrite(filename,self.tmp)
        print('Image saved as:',self.filename)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "AIP_40675028H"))
        self.pushButton.setText(_translate("MainWindow", "Load"))
        self.pushButton_2.setText(_translate("MainWindow", "Exec"))
        self.pushButton_3.setText(_translate("MainWindow", "Save"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Input</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Output</span></p></body></html>"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
