import threading
import subprocess

def run_server():
    subprocess.run(["python", "Interfaz.py"])

def run_interface():
    subprocess.run(["python", "ServidorMulticonexiones.py"])

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_server)
    interface_thread = threading.Thread(target=run_interface)

    server_thread.start()
    interface_thread.start()

    server_thread.join()
    interface_thread.join()
