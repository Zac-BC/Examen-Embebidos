import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from circle_widget import CircleWidget  # Importa la clase desde otro archivo

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz PyQt6")
        self.setGeometry(100, 100, 600, 400)

        main_layout = QHBoxLayout()

        # Column 1: Entradas
        entradas_layout = QVBoxLayout()
        entradas_layout.addWidget(QLabel("Entradas"))
        self.circle1 = CircleWidget(Qt.GlobalColor.red)
        self.circle2 = CircleWidget(Qt.GlobalColor.green)
        entradas_layout.addWidget(self.circle1)
        entradas_layout.addWidget(self.circle2)

        # Column 2: Salidas
        salidas_layout = QVBoxLayout()
        salidas_layout.addWidget(QLabel("Salidas"))
        self.circle3 = CircleWidget(Qt.GlobalColor.blue)
        self.circle4 = CircleWidget(Qt.GlobalColor.yellow)
        self.circle5 = CircleWidget(Qt.GlobalColor.cyan)
        self.circle6 = CircleWidget(Qt.GlobalColor.magenta)
        self.circle7 = CircleWidget(Qt.GlobalColor.gray)
        salidas_layout.addWidget(self.circle3)
        salidas_layout.addWidget(self.circle4)
        salidas_layout.addWidget(self.circle5)
        salidas_layout.addWidget(self.circle6)
        salidas_layout.addWidget(self.circle7)

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
