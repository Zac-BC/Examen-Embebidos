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

const int puertos[7]= {2,4,5,18,19,34,35};
WiFiClient cliente;

// Variables para el semáforo
unsigned long previousMillis = 0;
const long intervalRojo = 5000; // 5 segundos
const long intervalAmarillo = 2000; // 2 segundos
const long intervalVerde = 5000; // 5 segundos
int estadoSemaforo = 0; // 0: Rojo, 1: Verde, 2: Amarillo

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
    Serial.println("Conexion perdida, reconectando");
    cliente.connect(server_ip, server_port);
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
  Serial.println("Led2:"+String(estados[0])+"Led4:"+String(estados[1])+"Led5:"+String(estados[2])+"Led18:"+String(estados[3])+"Led19:"+String(estados[4])+"Led34:"+String(estados[5])+"Led35:"+String(estados[6]));// Nueva línea después de enviar todos los estados
  if (cliente.connected()) {
    sleep(1);
    //int puertos[7]= {2,4,5,18,19,34,35}
    Serial.println(String(estados[0])+String(estados[1])+String(estados[2])+String(estados[3])+String(estados[4])+String(estados[5])+String(estados[6]));// Nueva línea después de enviar todos los estados
    cliente.println(String(estados[0])+String(estados[1])+String(estados[2])+String(estados[3])+String(estados[4])+String(estados[5])+String(estados[6]));// Nueva línea después de enviar todos los estados
  }

  // Control del semáforo
  unsigned long currentMillis = millis();
  switch (estadoSemaforo) {
    case 0: // Rojo
      if (currentMillis - previousMillis >= intervalRojo) {
        previousMillis = currentMillis;
        estadoSemaforo = 1;
        digitalWrite(ledRojo, LOW);
        digitalWrite(ledVerde, HIGH);
      }
      break;
    case 1: // Verde
      if (currentMillis - previousMillis >= intervalVerde) {
        previousMillis = currentMillis;
        estadoSemaforo = 2;
        digitalWrite(ledVerde, LOW);
        digitalWrite(ledAmarillo, HIGH);
      }
      break;
    case 2: // Amarillo
      if (currentMillis - previousMillis >= intervalAmarillo) {
        previousMillis = currentMillis;
        estadoSemaforo = 0;
        digitalWrite(ledAmarillo, LOW);
        digitalWrite(ledRojo, HIGH);
      }
      break;
  }
}

int GetterPuerto(int posicion) {
  //int puertos[7]= {2,4,5,18,19,34,35}
  int estado = digitalRead(puertos[posicion]);
  return estado;
}
