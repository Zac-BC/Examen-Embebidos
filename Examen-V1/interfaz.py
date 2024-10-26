import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QGroupBox
from PyQt6.QtCore import QThread, pyqtSignal

SERVER_IP = "http://127.0.0.1:5000"

class StatusWorker(QThread):
    update_leds = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def run(self):
        while True:
            try:
                response = requests.get(f"{SERVER_IP}/status", timeout=10)  # Aumentar el timeout
                response.raise_for_status()
                led_states = response.json()
                self.update_leds.emit(led_states)
            except requests.ConnectionError:
                self.error_occurred.emit('Error: No se pudo conectar con el servidor.')
            except requests.exceptions.RequestException as e:
                self.error_occurred.emit(f'Error: {str(e)}')
            self.msleep(1000)  # Pausar por 1 segundo entre solicitudes

class ToggleWorker(QThread):
    toggle_complete = pyqtSignal()
    error_occurred = pyqtSignal(str)

    def run(self):
        try:
            response = requests.get(f"{SERVER_IP}/toggle", timeout=10)  # Aumentar el timeout
            response.raise_for_status()
            self.toggle_complete.emit()
        except requests.ConnectionError:
            self.error_occurred.emit('Error: No se pudo conectar con el servidor.')
        except requests.exceptions.RequestException as e:
            self.error_occurred.emit(f'Error: {str(e)}')

class LEDControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.status_worker = StatusWorker()
        self.status_worker.update_leds.connect(self.update_led_labels)
        self.status_worker.error_occurred.connect(self.handle_error)
        self.status_worker.start()

    def initUI(self):
        self.setWindowTitle('Control de LEDs')

        # Layout principal
        main_layout = QVBoxLayout()

        # Monitor de LEDs
        monitor_group = QGroupBox("Monitor")
        monitor_layout = QVBoxLayout()
        self.status_label = QLabel('Estado de los LEDs')
        monitor_layout.addWidget(self.status_label)
        self.toggle_button = QPushButton('Toggle LED Remoto')
        self.toggle_button.clicked.connect(self.toggle_led)
        monitor_layout.addWidget(self.toggle_button)
        monitor_group.setLayout(monitor_layout)
        main_layout.addWidget(monitor_group)

        # LEDs
        self.led_labels = {}
        for color in ['rojo', 'amarillo', 'verde', 'boton1', 'remoto']:
            label = QLabel(f'LED {color.capitalize()}')
            label.setStyleSheet("background-color: grey; border-radius: 10px;")
            self.led_labels[color] = label
            monitor_layout.addWidget(label)

        self.setLayout(main_layout)

    def toggle_led(self):
        self.toggle_worker = ToggleWorker()
        self.toggle_worker.toggle_complete.connect(self.status_worker.start)
        self.toggle_worker.error_occurred.connect(self.handle_error)
        self.toggle_worker.start()

    def update_led_labels(self, led_states):
        print("Actualizando LEDs:", led_states)  # Agregar información de depuración
        for color, estado in led_states.items():
            if color in self.led_labels:
                color_state = 'green' if estado == 'ENCENDIDO' else 'grey'
                self.led_labels[color].setStyleSheet(f"background-color: {color_state}; border-radius: 10px;")
                print(f"{color.capitalize()} LED actualizado a: {color_state}")  # Debug info

    def handle_error(self, error_message):
        self.status_label.setText(error_message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LEDControlApp()
    ex.show()
    sys.exit(app.exec())
