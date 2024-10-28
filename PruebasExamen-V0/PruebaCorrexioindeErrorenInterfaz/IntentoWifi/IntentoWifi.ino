#include <WiFi.h>
#include <WiFiClient.h>

// Definir Pines
const int ledRojo = 2;
const int ledAmarillo = 4;
const int ledVerde = 5;
const int ledBoton1 = 18;
const int ledRemoto = 19;

// Definición de pines para botones
const int boton1 = 34;
const int boton2 = 35;

bool estadoLedNuevo = false;

const char* ssid = "InternetX";
const char* password = "InternetZ";
const char* server_ip = "192.168.100.128";
const int server_port = 65434;
int contador = 0;
WiFiClient cliente;

void setup() {
  Serial.begin(115200);
  // Configuración de pines de salida para LEDs
  pinMode(ledRojo, OUTPUT);
  pinMode(ledAmarillo, OUTPUT);
  pinMode(ledVerde, OUTPUT);
  pinMode(ledBoton1, OUTPUT);
  pinMode(ledRemoto, OUTPUT);

  // Configuración de pines de entrada para botones
  pinMode(boton1, INPUT_PULLUP);
  pinMode(boton2, INPUT_PULLUP);

  digitalWrite(ledRemoto, LOW);

  Serial.println("Conectando a la red");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Conexion establecida");
  Serial.println("Dirección IP");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (!cliente.connected()) {
    Serial.print("Conexion perdida, reconectando");
    cliente.connect(server_ip, server_port);
  }

  if (cliente.available()) {
    String respuesta = cliente.readStringUntil('\n');
    Serial.print("Respuesta del servidor: ");
    Serial.println(respuesta);
  }

  if (Serial.available() > 0) {
    char buffer[64];
    int bytesRead = Serial.readBytesUntil('\n', buffer, sizeof(buffer) - 1);
    buffer[bytesRead] = '\0';
    cliente.println(String(buffer));
  }

  int estados[7];
  for (int i = 0; i < 7; i++) {
    estados[i] = GetterPuerto(i);
  }

  if (cliente.connected()) {
    cliente.println(String(estados[0])+String(estados[1])+String(estados[2])+String(estados[3])+String(estados[4])+String(estados[5])+String(estados[6]));// Nueva línea después de enviar todos los estados
  }

  for (int i = 0; i < 7; i++) {
    Serial.print("Estado del puerto ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(estados[i]);
  }
}

int GetterPuerto(int botonx) {
  int estado = digitalRead(botonx);
  return estado;
}