import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPainter, QBrush, QPen
from PyQt6.QtCore import Qt

class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(50, 50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(Qt.GlobalColor.blue, Qt.BrushStyle.SolidPattern))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(10, 10, 30, 30)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz PyQt6")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

        # Column 1: Entradas
        entradas_layout = QVBoxLayout()
        entradas_layout.addWidget(QLabel("Entradas"))
        entradas_layout.addWidget(CircleWidget())
        entradas_layout.addWidget(CircleWidget())

        # Column 2: Salidas
        salidas_layout = QVBoxLayout()
        salidas_layout.addWidget(QLabel("Salidas"))
        for _ in range(5):
            salidas_layout.addWidget(CircleWidget())

        # Column 3: Monitoreo
        monitoreo_layout = QVBoxLayout()
        monitoreo_layout.addWidget(QLabel("Monitoreo"))
        
        direccion_layout = QHBoxLayout()
        direccion_layout.addWidget(QLabel("Dirección:"))
        direccion_layout.addWidget(QLineEdit())
        monitoreo_layout.addLayout(direccion_layout)
        
        puerto_layout = QHBoxLayout()
        puerto_layout.addWidget(QLabel("Puerto:"))
        puerto_layout.addWidget(QLineEdit())
        monitoreo_layout.addLayout(puerto_layout)
        
        monitoreo_layout.addWidget(QPushButton("Conectar"))

        # Add columns to main layout
        main_layout.addLayout(entradas_layout)
        main_layout.addLayout(salidas_layout)
        main_layout.addLayout(monitoreo_layout)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
