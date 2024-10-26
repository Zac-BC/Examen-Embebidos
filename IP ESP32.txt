#include <WiFi.h>

const char* ssid = "TU_SSID";  // Reemplaza con tu SSID
const char* password = "TU_PASSWORD";  // Reemplaza con tu contraseña

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }

  Serial.println("Conectado a WiFi");
  Serial.print("Dirección IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  // Aquí puedes agregar el resto de tu código
}



