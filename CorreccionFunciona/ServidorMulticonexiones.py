import socket
import threading
from ColorManager import ColorManager  # Importar desde el nuevo archivo

class ServidorSocket:
    DIRECCION = "192.168.100.128"
    PUERTO = 65434
    
    def __init__(self, mainColor):
        self.mainColor = mainColor
        print("Dentro del self.servidor")
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.DIRECCION, self.PUERTO))
        self.servidor.listen(0)
        self.cliente_socket = None
        self.color_manager = ColorManager()  # Instancia de ColorManager
        self.iniciar_conexiones()

    def iniciar_conexiones(self):
        print(f"Escuchando en la dirección {self.DIRECCION} : {self.PUERTO}")
        
        while True:
            self.cliente_socket, cliente_direccion = self.servidor.accept()
            tarea = threading.Thread(target=self.manejar_conexion, args=(self.cliente_socket, cliente_direccion))
            tarea.start()
            
    def manejar_conexion(self, cliente_socket, cliente_direccion):
        print(f"Aceptando conexión de : {cliente_direccion[0]}:{cliente_direccion[1]}")
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
                        self.mainColor.updateColorFromCode(pos, 1)
                    elif char == '0':
                        print(f"Encontré una !H en la posición {pos}!")
                        self.mainColor.updateColorFromCode(pos, 0)

            except ConnectionResetError:
                print("Conexion cerrada por el cliente")
                break

        cliente_socket.close()
        print("Conexión cerrada")

def start_server(mainColor):
    servidor = ServidorSocket(mainColor)