#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

// Definición de pines para LEDs
const int ledRojo = 2;
const int ledAmarillo = 4;
const int ledVerde = 5;
const int ledBoton1 = 18;
const int ledRemoto = 19;

// Definición de pines para botones
const int boton1 = 34;
const int boton2 = 35;

bool estadoLedNuevo = false;

// Datos de la red Wi-Fi
const char* ssid = "INFINITUMD488-5G";
const char* password = "3Putoslocos";

WebServer server(80);

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

  conectarWiFi();

  server.on("/", handleRoot);
  server.on("/toggle", handleToggle);
  server.on("/status", handleStatus);  // Endpoint para el estado de los LEDs
  server.onNotFound(handleNotFound);

  server.begin();
}

void loop() {
  server.handleClient();
  manejarLEDs();
  manejarBotones();
}

void manejarLEDs() {
  static unsigned long lastUpdateTime = 0;
  unsigned long currentTime = millis();
  if (currentTime - lastUpdateTime > 5000) {  // Actualizar LEDs cada 5 segundos
    lastUpdateTime = currentTime;

    // Secuencia de LEDs
    digitalWrite(ledVerde, HIGH);
    delay(1000);
    digitalWrite(ledVerde, LOW);

    digitalWrite(ledAmarillo, HIGH);
    delay(1000);
    digitalWrite(ledAmarillo, LOW);

    digitalWrite(ledRojo, HIGH);
    delay(1000);
    digitalWrite(ledRojo, LOW);
  }
}

void manejarBotones() {
  if (digitalRead(boton1) == LOW) {
    digitalWrite(ledBoton1, HIGH);  // Encender LED Botón 1 cuando el botón está presionado
  } else {
    digitalWrite(ledBoton1, LOW);   // Apagar LED Botón 1 cuando el botón está liberado
  }

  if (digitalRead(boton2) == LOW) {
    digitalWrite(ledRemoto, HIGH);  // Encender LED Remoto cuando el botón está presionado
  } else {
    digitalWrite(ledRemoto, LOW);   // Apagar LED Remoto cuando el botón está liberado
  }
}

void conectarWiFi() {
  Serial.print("Conectando a ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  unsigned long startAttemptTime = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - startAttemptTime < 10000) {
    delay(1000);
    Serial.print(".");
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("");
    Serial.println("WiFi conectado.");
    Serial.print("Dirección IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("");
    Serial.println("No se pudo conectar a Wi-Fi.");
  }
}

void handleRoot() {
  server.send(200, "text/plain", "ESP32 Server");
}

void handleToggle() {
  estadoLedNuevo = !estadoLedNuevo;
  digitalWrite(ledRemoto, estadoLedNuevo ? HIGH : LOW);
  server.send(200, "text/plain", estadoLedNuevo ? "LED ON" : "LED OFF");
  Serial.println(estadoLedNuevo ? "LED ON" : "LED OFF");
}

void handleStatus() {
  Serial.println("Manejando solicitud de estado");
  StaticJsonDocument<200> doc;
  doc["rojo"] = digitalRead(ledRojo) == HIGH ? "ENCENDIDO" : "APAGADO";
  doc["amarillo"] = digitalRead(ledAmarillo) == HIGH ? "ENCENDIDO" : "APAGADO";
  doc["verde"] = digitalRead(ledVerde) == HIGH ? "ENCENDIDO" : "APAGADO";
  doc["boton1"] = digitalRead(ledBoton1) == HIGH ? "ENCENDIDO" : "APAGADO";
  doc["remoto"] = estadoLedNuevo ? "ENCENDIDO" : "APAGADO";

  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
  Serial.println("Estado enviado: " + response);
}

void handleNotFound() {
  server.send(404, "text/plain", "Not Found");
  Serial.println("Solicitud no encontrada");
}