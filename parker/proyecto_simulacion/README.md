# Sistema de Simulación Computacional

## 📋 Descripción
Aplicación de escritorio desarrollada en Python con interfaz gráfica para simulación computacional, generación de variables aleatorias, pruebas de bondad de ajuste y métodos Monte Carlo.

## 🚀 Características

### 1. Generación de Variables Aleatorias
- **Distribuciones Discretas**: Binomial, Poisson
- **Distribuciones Continuas**: Exponencial, Normal
- **Generador Pseudoaleatorio**: LCG (Linear Congruential Generator)
- **Semillas**: Automática o manual definida por usuario

### 2. Pruebas de Bondad de Ajuste
- **Chi-cuadrado**: Para distribuciones discretas y continuas
- **Kolmogorov-Smirnov**: Para distribuciones continuas
- **Visualización**: Gráficos comparativos CDF y histogramas

### 3. Métodos Monte Carlo
- **Estimación de π**: Visualización interactiva de puntos
- **Ruina del Jugador**: Simulación de problemas de probabilidad
- **Análisis Estadístico**: Resultados detallados con métricas

## 🛠️ Instalación

### Requisitos
```bash
Python 3.8+
pip install numpy scipy matplotlib tkinter