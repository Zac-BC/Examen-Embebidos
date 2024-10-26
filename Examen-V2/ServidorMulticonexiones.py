import socket
import threading
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


class ServidorSocket:
    DIRECCION = "192.168.100.128"
    PUERTO = 65434
    
    def __init__(self):
        print("Dentro del self.servidor")
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.DIRECCION, self.PUERTO))
        self.servidor.listen(0)
        self.cliente_socket = None
        self.iniciar_conexiones()
        self.ColoresCircularesInterfaz = Colores

    def iniciar_conexiones(self):
        print(f"Escuchando en la dirección {self.DIRECCION} : {self.PUERTO}")
        
        while True:
            self.cliente_socket, cliente_direccion = self.servidor.accept()
            tarea= threading.Thread(target=self.manejar_conexion,args=(self.cliente_socket, cliente_direccion))
            tarea.start()
            
    def manejar_conexion(self, cliente_socket, cliente_direccion):
        print(f"Aceptando conexión de : {cliente_direccion[0]}:{cliente_direccion[1]}")
        while True:
            while True:
                try:
                    self.request = cliente_socket.recv(1024)
                    self.request = self.request.decode("utf-8")

                    if self.request.lower() == "cerrar":
                        cliente_socket.send("cerrada".encode("utf-8"))
                        break

                    print(f"recibido: {self.request}")
                    response = "acepta".encode("utf-8")
                    cliente_socket.send(response)
                    for pos, char in enumerate(self.request):
                        if char == '1':
                            print(f"Encontré una H en la posición {pos}!")
                            self.update_color_based_on_code(self, pos, 1)
                        elif char == '0':
                            print(f"Encontré una !H en la posición {pos}!")
                            self.update_color_based_on_code(self, pos, 0)

                except ConnectionResetError:
                    print("Conexion cerrada por el cliente")
                    break

            cliente_socket.close()
            print("Conexión cerrada")

def main():
    servidor = ServidorSocket()

if __name__ == "__main__":
    main() 