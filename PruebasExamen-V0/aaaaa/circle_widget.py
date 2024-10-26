from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QBrush, QPen
from PyQt6.QtCore import Qt

class CircleWidget(QWidget):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.setMinimumSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.color, Qt.BrushStyle.SolidPattern))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(10, 10, 30, 30)

    def change_color(self, new_color):
        self.color = new_color
        self.update()  # Redraw the widget with the new color
