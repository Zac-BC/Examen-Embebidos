from PyQt6.QtGui import QColor

class ColorManager:
    def __init__(self):
        self.colors = {}

    def set_color(self, identifier, color):
        print("Llego al set_color")
        self.colors[identifier] = color

    def get_color(self, identifier):
        return self.colors.get(identifier, None)

    def update_color_based_on_code(self, identifier, code):
        # Cambiar color a verde o rojo según el código
        if code == 1:
            self.set_color(identifier, QColor(0, 255, 0))  # Verde
            print("Llego al color_based1")
        elif code == 0:
            self.set_color(identifier, QColor(255, 0, 0))  # Rojo
            print("Llego al color_based0")