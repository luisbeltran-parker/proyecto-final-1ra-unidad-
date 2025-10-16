# Sistema de Simulación Computacional

## Proyecto Parcial de Primera Unidad

Aplicación de escritorio con interfaz gráfica (GUI) que implementa conceptos fundamentales de simulación computacional.

---

## 📋 Características

### 1. Generación de Variables Aleatorias
- **Distribuciones implementadas:**
  - Binomial (discreta)
  - Exponencial (continua)
- **Generador pseudoaleatorio personalizado:** Implementación del algoritmo LCG (Linear Congruential Generator)
- **Modalidades de semilla:**
  - Automática (basada en tiempo del sistema)
  - Manual (definida por el usuario)
- **Exportación de datos** a archivos de texto

### 2. Pruebas de Bondad de Ajuste
- **Prueba de Kolmogorov-Smirnov**
- **Prueba de Chi-cuadrado**
- Comparación visual entre distribuciones empíricas y teóricas
- Interpretación automática de resultados (con α=0.05)

### 3. Método de Monte Carlo
- **Estimación de π:** Método de puntos aleatorios en círculo unitario
- **Problema de la Ruina del Jugador:** Simulación probabilística
- Visualización gráfica de resultados
- Análisis estadístico detallado

### 4. Interfaz Gráfica
- Diseño intuitivo con pestañas (Notebook)
- Validación de entradas de usuario
- Gráficos interactivos (matplotlib)
- Importación/exportación de datos

---

## 🛠️ Requisitos Técnicos

### Lenguaje y Librerías
- **Python 3.8+**
- **tkinter** (interfaz gráfica)
- **numpy** (cálculos numéricos)
- **scipy** (distribuciones estadísticas)
- **matplotlib** (visualización)

### Instalación de Dependencias

```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd simulacion-computacional

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install numpy scipy matplotlib
```

**Nota:** tkinter viene preinstalado con Python en la mayoría de las distribuciones.

---

## 🚀 Ejecución

```bash
python main.py
```

---

## 📖 Guía de Uso

### Pestaña 1: Generación de Variables

1. **Seleccionar tipo de semilla:**
   - Automática: genera semilla basada en tiempo del sistema
   - Manual: permite especificar una semilla personalizada

2. **Seleccionar distribución:**
   - **Binomial:** Configurar parámetros n (ensayos) y p (probabilidad)
   - **Exponencial:** Configurar parámetro λ (tasa)

3. **Especificar número de muestras**

4. **Hacer clic en "Generar Variables"**

5. **Visualizar resultados:**
   - Estadísticas descriptivas (media, desviación estándar, mínimo, máximo)
   - Histograma de distribución

6. **Exportar datos:** Menú → Archivo → Exportar datos

### Pestaña 2: Pruebas de Bondad

1. **Generar o importar datos** primero

2. **Seleccionar distribución a probar:**
   - Exponencial
   - Normal

3. **Seleccionar tipo de prueba:**
   - Kolmogorov-Smirnov (recomendada para muestras grandes)
   - Chi-cuadrado (requiere frecuencias esperadas ≥ 5)

4. **Hacer clic en "Realizar Prueba"**

5. **Interpretar resultados:**
   - Estadístico de prueba
   - P-valor
   - Decisión sobre H₀ (α=0.05)
   - Gráfico comparativo

### Pestaña 3: Monte Carlo

#### Estimación de π:
1. Especificar número de puntos (recomendado: 10,000+)
2. Ejecutar simulación
3. Visualizar puntos dentro/fuera del círculo
4. Comparar π estimado con π real

#### Ruina del Jugador:
1. Configurar parámetros:
   - Capital inicial
   - Objetivo (capital a alcanzar)
   - Probabilidad de ganar cada ronda
   - Número de simulaciones
2. Ejecutar simulación
3. Analizar resultados:
   - Probabilidad de ruina
   - Probabilidad de éxito
   - Duración promedio del juego

---

## 📁 Estructura del Proyecto

```
simulacion-computacional/
│
├── main.py                 # Archivo principal
├── README.md              # Este archivo
├── requirements.txt       # Dependencias del proyecto
└── ejemplos/              # Datos de ejemplo
    ├── datos_exponencial.txt
    └── datos_binomial.txt
```

---

## 🔬 Fundamentos Teóricos

### Generador Pseudoaleatorio (LCG)

El generador utiliza la fórmula:
```
X_{n+1} = (a * X_n + c) mod m
```

Donde:
- a = 1664525 (multiplicador)
- c = 1013904223 (incremento)
- m = 2³² (módulo)

### Distribuciones Implementadas

**Binomial:**
- Genera n ensayos Bernoulli independientes
- Cuenta el número de éxitos

**Exponencial:**
- Usa el método de la transformada inversa
- X = -ln(U) / λ, donde U ~ Uniforme(0,1)

### Pruebas de Bondad

**Kolmogorov-Smirnov:**
- Mide la distancia máxima entre CDF empírica y teórica
- D = max|F_n(x) - F(x)|

**Chi-cuadrado:**
- Compara frecuencias observadas vs esperadas
- χ² = Σ[(O_i - E_i)² / E_i]

### Monte Carlo

**Estimación de π:**
- Genera puntos aleatorios en cuadrado [-1,1]×[-1,1]
- π ≈ 4 × (puntos_dentro_círculo / total_puntos)

**Ruina del Jugador:**
- Simula juego de apuestas hasta ruina o éxito
- Calcula probabilidades empíricas

---

## 📊 Ejemplos de Salida

### Exportación de Datos
Los datos se exportan en formato texto:
```
Datos generados - Simulación Computacional
==================================================
Semilla: 1697401234567
Número de muestras: 1000
Media: 5.012000
Desviación estándar: 1.587401

Datos:
5.000000
4.000000
6.000000
...
```

---

## 🎯 Características de POO

El proyecto implementa Programación Orientada a Objetos:

- **`GeneradorPseudoaleatorio`**: Encapsula la lógica del generador LCG
- **`DistribucionDiscreta`**: Métodos estáticos para distribuciones discretas
- **`DistribucionContinua`**: Métodos estáticos para distribuciones continuas
- **`PruebasBondad`**: Implementa pruebas estadísticas
- **`MonteCarlo`**: Métodos de simulación Monte Carlo
- **`AplicacionSimulacion`**: Clase principal con la GUI

---

## ✅ Validaciones Implementadas

- Verificación de valores numéricos válidos
- Rangos apropiados para probabilidades [0, 1]
- Valores positivos para parámetros (n, λ, etc.)
- Manejo de archivos con datos incorrectos
- Validación de existencia de datos antes de pruebas

---

## 🐛 Solución de Problemas

### Error: "No module named 'tkinter'"
**Solución:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# Fedora
sudo dnf install python3-tkinter

# Windows/Mac: tkinter viene preinstalado
```

### Error: "No hay datos para exportar"
**Solución:** Primero genere variables aleatorias en la pestaña "Generación de Variables"

### Gráficos no se visualizan correctamente
**Solución:** Actualice matplotlib:
```bash
pip install --upgrade matplotlib
```

---

## 📝 Notas Adicionales

- El generador LCG es determinístico con la misma semilla
- Para investigación seria, considere generadores más robustos (Mersenne Twister)
- Las pruebas de bondad requieren al menos 30 datos
- El método de Monte Carlo converge más lento que otros métodos analíticos

---

## 👨‍💻 Autor

[Tu Nombre]  
[Tu Correo]  
Universidad Nacional (UNA)  
Curso: Simulación Computacional

---

## 📅 Información del Proyecto

- **Fecha de entrega:** 14 de octubre de 2025, 23:59 hrs
- **Exposición:** A partir del 15 de octubre de 2025
- **Plataforma:** Aula Virtual UNA

---

## 📜 Licencia

Este proyecto es de uso académico para el curso de Simulación Computacional.

---

## 🔗 Referencias

- Numerical Recipes in C (Press et al.)
- Law, A. M., & Kelton, W. D. (2000). Simulation Modeling and Analysis
- Ross, S. M. (2013). Simulation (5th ed.)
- Documentación de SciPy: https://docs.scipy.org/
- Documentación de NumPy: https://numpy.org/doc/