#define X_PIN 25
#define Y_PIN 26
#define DELAY_PUNTO 1500

// ===== COORDENADAS CASA =====
#define CASA_IZQ -0.65
#define CASA_DER 0.65
#define CASA_ABAJO -0.65
#define CASA_ARRIBA 0.20
#define TECHO_PICO 0.85

// ===== COORDENADAS ÁRBOL =====
#define ARBOL_X 0.93
#define ARBOL_X_IZQ 0.88
#define ARBOL_X_DER 0.98

// Plotea un punto en coordenadas normalizadas (-1 a +1)
void punto(float x, float y) {
  int X = (x + 1.0) * 127.5;
  int Y = (y + 1.0) * 127.5;
  X = constrain(X, 0, 255);
  Y = constrain(Y, 0, 255);
  dacWrite(X_PIN, X);
  dacWrite(Y_PIN, Y);
  delayMicroseconds(DELAY_PUNTO);
}

// Dibuja línea interpolada
void linea(float x1, float y1, float x2, float y2, int pasos = 80) {
  for (int i = 0; i <= pasos; i++) {
    float t = (float)i / pasos;
    float x = x1 + (x2 - x1) * t;
    float y = y1 + (y2 - y1) * t;
    punto(x, y);
  }
}

// Dibuja rectángulo
void rectangulo(float x1, float y1, float x2, float y2) {
  linea(x1, y1, x2, y1);
  linea(x2, y1, x2, y2);
  linea(x2, y2, x1, y2);
  linea(x1, y2, x1, y1);
}

// Dibuja triángulo
void triangulo(float x1, float y1, float x2, float y2, float x3, float y3) {
  linea(x1, y1, x2, y2);
  linea(x2, y2, x3, y3);
  linea(x3, y3, x1, y1);
}

// Dibuja cruz en ventana
void cruzVentana(float x1, float y1, float x2, float y2) {
  float xmid = (x1 + x2) / 2;
  float ymid = (y1 + y2) / 2;
  linea(xmid, y1, xmid, y2);
  linea(x1, ymid, x2, ymid);
}

// ===== DIBUJAR CASA =====
void dibujarCasa() {
  // Paredes
  rectangulo(CASA_IZQ, CASA_ABAJO, CASA_DER, CASA_ARRIBA);
  
  // Techo
  triangulo(CASA_IZQ, CASA_ARRIBA, 0.0, TECHO_PICO, CASA_DER, CASA_ARRIBA);
  
  // Puerta
  rectangulo(-0.18, CASA_ABAJO, 0.18, -0.05);
  
  // Ventana izquierda
  rectangulo(-0.50, -0.05, -0.25, 0.20);
  cruzVentana(-0.50, -0.05, -0.25, 0.20);
  
  // Ventana derecha
  rectangulo(0.25, -0.05, 0.50, 0.20);
  cruzVentana(0.25, -0.05, 0.50, 0.20);
  
  // Chimenea
  rectangulo(0.30, 0.40, 0.50, 0.90);
}

// ===== DIBUJAR ÁRBOL MEJORADO =====
void dibujarArbol() {
  // ===== TRONCO =====
  rectangulo(ARBOL_X_IZQ, CASA_ABAJO, ARBOL_X_DER, 0.05);
  linea(ARBOL_X, CASA_ABAJO, ARBOL_X, 0.05);  // Corteza
  
  // Pequeñas raíces
  linea(ARBOL_X_IZQ, CASA_ABAJO, ARBOL_X_IZQ - 0.08, CASA_ABAJO - 0.05);
  linea(ARBOL_X_DER, CASA_ABAJO, ARBOL_X_DER + 0.08, CASA_ABAJO - 0.05);
  
  // ===== COPA NIVEL 1 (BASE - ANCHA) =====
  // Triángulo principal
  triangulo(0.60, 0.05, ARBOL_X, 0.50, 1.26, 0.05);
  
  // Ramas internas principales
  linea(0.68, 0.15, ARBOL_X, 0.42);
  linea(ARBOL_X, 0.42, 1.18, 0.15);
  
  // Ramas secundarias izquierda
  linea(0.64, 0.08, ARBOL_X - 0.10, 0.30);
  linea(ARBOL_X - 0.10, 0.30, ARBOL_X, 0.38);
  
  // Ramas secundarias derecha
  linea(1.22, 0.08, ARBOL_X + 0.10, 0.30);
  linea(ARBOL_X + 0.10, 0.30, ARBOL_X, 0.38);
  
  // Detalles de textura en copa 1
  linea(0.73, 0.18, ARBOL_X - 0.05, 0.28);
  linea(1.13, 0.18, ARBOL_X + 0.05, 0.28);
  
  // ===== COPA NIVEL 2 (MEDIA) =====
  // Triángulo principal
  triangulo(0.70, 0.38, ARBOL_X, 0.68, 1.16, 0.38);
  
  // Ramas internas
  linea(0.78, 0.48, ARBOL_X, 0.60);
  linea(ARBOL_X, 0.60, 1.08, 0.48);
  
  // Ramas laterales nivel 2
  linea(0.75, 0.42, ARBOL_X - 0.12, 0.52);
  linea(1.11, 0.42, ARBOL_X + 0.12, 0.52);
  
  // Detalles textura
  linea(0.82, 0.50, ARBOL_X - 0.03, 0.57);
  linea(1.04, 0.50, ARBOL_X + 0.03, 0.57);
  
  // ===== COPA NIVEL 3 (SUPERIOR) =====
  // Triángulo principal
  triangulo(0.78, 0.60, ARBOL_X, 0.85, 1.08, 0.60);
  
  // Ramas internas
  linea(0.84, 0.68, ARBOL_X, 0.78);
  linea(ARBOL_X, 0.78, 1.02, 0.68);
  
  // Detalles textura
  linea(0.88, 0.65, ARBOL_X - 0.02, 0.72);
  linea(0.98, 0.65, ARBOL_X + 0.02, 0.72);
  
  // ===== COPA NIVEL 4 (PUNTA - PEQUEÑA) =====
  triangulo(0.85, 0.78, ARBOL_X, 0.98, 1.01, 0.78);
  
  // Rama central hacia punta
  linea(ARBOL_X, 0.60, ARBOL_X, 1.00);
  
  // ===== DETALLES FINALES =====
  // Pequeñas ramas salientes en costados
  linea(0.60, 0.20, 0.52, 0.25);
  linea(1.26, 0.20, 1.34, 0.25);
  
  linea(0.70, 0.45, 0.60, 0.50);
  linea(1.16, 0.45, 1.26, 0.50);
  
  linea(0.78, 0.68, 0.70, 0.72);
  linea(1.08, 0.68, 1.16, 0.72);
}

void setup() {
  dacWrite(X_PIN, 128);
  dacWrite(Y_PIN, 128);
  delay(1000);
}

void loop() {
  dibujarCasa();
  dibujarArbol();
  delay(100);
}
