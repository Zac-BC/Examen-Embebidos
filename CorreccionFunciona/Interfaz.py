import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QColorDialog
)
from PyQt6.QtGui import QPainter, QBrush, QPen, QColor
from PyQt6.QtCore import Qt
from ColorManager import ColorManager  # Importar desde el nuevo archivo

class EditableCircleWidget(QWidget):
    def __init__(self, identifier, color_manager):
        super().__init__()
        self.setMinimumSize(50, 50)
        self.identifier = identifier
        self.color_manager = color_manager
        self.color = self.color_manager.get_color(self.identifier) or QColor(Qt.GlobalColor.blue)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.color, Qt.BrushStyle.SolidPattern))
        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        painter.drawEllipse(10, 10, 30, 30)

    def setColor(self, color):
        print("Ya no se")
        self.color = color
        self.color_manager.set_color(self.identifier, color)
        self.update()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz PyQt6")
        self.setGeometry(100, 100, 600, 400)

        self.color_manager = ColorManager()
        main_layout = QHBoxLayout()

        # Column 1: Entradas
        entradas_layout = QVBoxLayout()
        entradas_layout.addWidget(QLabel("Entradas"))
        
        self.circles = []
        for i in range(7):  # Siete círculos editables
            circle_widget = EditableCircleWidget(f'circle_{i}', self.color_manager)
            self.circles.append(circle_widget)
            entradas_layout.addWidget(circle_widget)

            # Botón para cambiar color
            btn = QPushButton(f"Cambiar color círculo {i + 1}")
            btn.clicked.connect(lambda _, cw=circle_widget: self.changeColor(cw))
            entradas_layout.addWidget(btn)

            # Botones para cambiar color basado en código
            for code in [0, 1]:
                btn_code = QPushButton(f"Círculo {i + 1}: Set color {'Rojo' if code == 0 else 'Verde'}")
                btn_code.clicked.connect(lambda _, ci=i, c=code: self.updateColorFromCode(ci, c))
                entradas_layout.addWidget(btn_code)

        # Column 2: Salidas
        salidas_layout = QVBoxLayout()
        salidas_layout.addWidget(QLabel("Salidas"))
        for _ in range(5):
            salidas_layout.addWidget(EditableCircleWidget('salida_circle', self.color_manager))

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

    def changeColor(self, circle_widget):
        color = QColorDialog.getColor(circle_widget.color, self)
        if color.isValid():
            circle_widget.setColor(color)

    def updateColorFromCode(self, circle_index, code):
        self.color_manager.update_color_based_on_code(f'circle_{circle_index}', code)
        new_color = self.color_manager.get_color(f'circle_{circle_index}')
        self.circles[circle_index].setColor(new_color)  # Actualiza el color del círculo

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Iniciar el servidor en un hilo separado
    import threading
    from ServidorMulticonexiones import start_server
    server_thread = threading.Thread(target=start_server, args=(window,))
    server_thread.start()

    sys.exit(app.exec())