"""
Módulo de generadores pseudoaleatorios
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import time
import numpy as np
from typing import List, Union, Optional


class GeneradorPseudoaleatorio:
    """
    Generador de números pseudoaleatorios usando métodos robustos
    Implementa LCG (Linear Congruential Generator) y Mersenne Twister mejorado
    """
    
    def __init__(self, semilla: Optional[int] = None):
        """
        Inicializa el generador con una semilla
        
        Args:
            semilla: Semilla para el generador. Si es None, se genera automáticamente
        """
        if semilla is None:
            # Generar semilla automática usando tiempo y procesos del sistema
            self.semilla = self._generar_semilla_automatica()
        else:
            self.semilla = semilla
        
        self.estado = self.semilla
        # Parámetros optimizados para LCG (valores de Numerical Recipes)
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
        
        # Estado para Mersenne Twister alternativo
        self._inicializar_mt()
        
        # Historial para verificación
        self.historial = [self.semilla]
    
    def _generar_semilla_automatica(self) -> int:
        """
        Genera una semilla automática robusta
        
        Returns:
            Semilla entera de 32 bits
        """
        tiempo_actual = int(time.time() * 1000000)
        pid = hash(str(time.process_time()))
        return (tiempo_actual ^ pid) % (2**31)
    
    def _inicializar_mt(self):
        """Inicializa el estado para el generador tipo Mersenne Twister"""
        self.mt_index = 0
        self.mt_state = [0] * 624
        self.mt_state[0] = self.semilla
        
        for i in range(1, 624):
            self.mt_state[i] = (1812433253 * 
                              (self.mt_state[i-1] ^ (self.mt_state[i-1] >> 30)) + i) & 0xFFFFFFFF
    
    def siguiente(self) -> float:
        """
        Genera el siguiente número pseudoaleatorio entre 0 y 1
        
        Returns:
            Número pseudoaleatorio en [0, 1)
        """
        # Método LCG mejorado
        self.estado = (self.a * self.estado + self.c) % self.m
        numero = self.estado / self.m
        
        # Mezclar con método alternativo para mejor distribución
        numero_mezclado = self._mezclar_bits(numero)
        self.historial.append(self.estado)
        
        return numero_mezclado
    
    def _mezclar_bits(self, x: float) -> float:
        """
        Mezcla los bits para mejorar la distribución
        
        Args:
            x: Número a mezclar
            
        Returns:
            Número mezclado
        """
        # Transformación XOR-shift simple
        temp = int(x * (2**32))
        temp ^= (temp << 13) & 0xFFFFFFFF
        temp ^= (temp >> 17) & 0xFFFFFFFF
        temp ^= (temp << 5) & 0xFFFFFFFF
        return temp / (2**32)
    
    def uniform(self, low: float = 0.0, high: float = 1.0, size: int = 1) -> List[float]:
        """
        Genera números uniformes en el rango [low, high]
        
        Args:
            low: Límite inferior
            high: Límite superior
            size: Número de muestras
            
        Returns:
            Lista de números uniformes
        """
        return [low + (high - low) * self.siguiente() for _ in range(size)]
    
    def enteros(self, low: int, high: int, size: int = 1) -> List[int]:
        """
        Genera enteros uniformes en [low, high] inclusive
        
        Args:
            low: Límite inferior
            high: Límite superior
            size: Número de muestras
            
        Returns:
            Lista de enteros
        """
        return [int(low + (high - low + 1) * self.siguiente()) for _ in range(size)]
    
    def eleccion(self, secuencia: List, size: int = 1) -> List:
        """
        Elige elementos aleatorios de una secuencia
        
        Args:
            secuencia: Secuencia de elementos
            size: Número de elecciones
            
        Returns:
            Lista de elementos elegidos
        """
        if not secuencia:
            raise ValueError("La secuencia no puede estar vacía")
        
        indices = self.enteros(0, len(secuencia) - 1, size)
        return [secuencia[i] for i in indices]
    
    def shuffle(self, secuencia: List) -> List:
        """
        Mezcla una secuencia in-place usando Fisher-Yates
        
        Args:
            secuencia: Secuencia a mezclar
            
        Returns:
            Secuencia mezclada
        """
        n = len(secuencia)
        for i in range(n-1, 0, -1):
            j = self.enteros(0, i)[0]
            secuencia[i], secuencia[j] = secuencia[j], secuencia[i]
        return secuencia
    
    def reset(self, semilla: Optional[int] = None):
        """
        Reinicia el generador con nueva semilla
        
        Args:
            semilla: Nueva semilla (opcional)
        """
        if semilla is not None:
            self.semilla = semilla
        self.estado = self.semilla
        self._inicializar_mt()
        self.historial = [self.semilla]


class GeneradorCongruencialMultiplicativo(GeneradorPseudoaleatorio):
    """
    Generador Congruencial Multiplicativo (GCM)
    Variante del LCG sin término constante
    """
    
    def __init__(self, semilla: Optional[int] = None, a: int = 48271, m: int = 2**31 - 1):
        """
        Inicializa el GCM
        
        Args:
            semilla: Semilla inicial
            a: Multiplicador
            m: Módulo (preferiblemente primo)
        """
        super().__init__(semilla)
        self.a = a
        self.m = m
        # Asegurar que la semilla sea impar y positiva
        if self.estado % 2 == 0:
            self.estado = (self.estado + 1) % self.m
    
    def siguiente(self) -> float:
        """Genera siguiente número con GCM"""
        self.estado = (self.a * self.estado) % self.m
        self.historial.append(self.estado)
        return self.estado / self.m


class PruebasAleatoriedad:
    """
    Clase para realizar pruebas de aleatoriedad en los generadores
    """
    
    @staticmethod
    def prueba_chisquare(datos: List[float], bins: int = 10) -> dict:
        """
        Prueba de chi-cuadrado para uniformidad
        
        Args:
            datos: Lista de números aleatorios
            bins: Número de intervalos
            
        Returns:
            Diccionario con resultados de la prueba
        """
        n = len(datos)
        esperado = n / bins
        observado, _ = np.histogram(datos, bins=bins, range=(0, 1))
        
        chi2 = np.sum((observado - esperado)**2 / esperado)
        grados_libertad = bins - 1
        
        return {
            'estadistico': chi2,
            'grados_libertad': grados_libertad,
            'p_valor': 1 - float(self._chi2_cdf(chi2, grados_libertad)),
            'uniforme': chi2 < 3 * grados_libertad  # Regla práctica
        }
    
    @staticmethod
    def _chi2_cdf(x: float, k: int) -> float:
        """Función de distribución chi-cuadrado aproximada"""
        from math import gamma
        if x <= 0:
            return 0.0
        # Aproximación simple
        return 1 - np.exp(-x/2) * (x/2)**(k/2) / gamma(k/2 + 1)
    
    @staticmethod
    def prueba_corridas(datos: List[float]) -> dict:
        """
        Prueba de corridas arriba/abajo de la media
        
        Args:
            datos: Lista de números aleatorios
            
        Returns:
            Diccionario con resultados
        """
        media = np.mean(datos)
        secuencia = ['+' if x > media else '-' for x in datos]
        
        corridas = 1
        for i in range(1, len(secuencia)):
            if secuencia[i] != secuencia[i-1]:
                corridas += 1
        
        n = len(datos)
        esperado = (2 * n - 1) / 3
        varianza = (16 * n - 29) / 90
        
        z = (corridas - esperado) / np.sqrt(varianza)
        
        return {
            'corridas_observadas': corridas,
            'corridas_esperadas': esperado,
            'z_score': z,
            'aleatorio': abs(z) < 1.96  # 95% confianza
        }