# color_manager.py

from PyQt6.QtGui import QColor

class ColorManager:
    def __init__(self):
        self.colors = {}

    def set_color(self, identifier, color):
        self.colors[identifier] = color

    def get_color(self, identifier):
        return self.colors.get(identifier, None)

    def update_color_based_on_code(self, identifier, code):
        # Cambiar color a verde o rojo según el código
        if code == 1:
            self.set_color(identifier, QColor(0, 255, 0))  # Verde
        elif code == 0:
            self.set_color(identifier, QColor(255, 0, 0))  # Rojo
