import sys
import random
from PyQt5 import QtWidgets, QtGui

class CircleApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Zadanie2-3')

        self.button = QtWidgets.QPushButton('Нажми на меня!', self)
        self.button.clicked.connect(self.draw_circle)
        self.button.resize(100, 30)
        self.button.move(350, 10)

        self.setStyleSheet("background-color: White")
        self.show()

    def draw_circle(self):
        self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        diameter = random.randint(20, 100)
        color = QtGui.QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        painter.setBrush(color)
        x = random.randint(0, self.width() - diameter)
        y = random.randint(0, self.height() - diameter)
        painter.drawEllipse(x, y, diameter, diameter)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = CircleApp()
    sys.exit(app.exec_())
