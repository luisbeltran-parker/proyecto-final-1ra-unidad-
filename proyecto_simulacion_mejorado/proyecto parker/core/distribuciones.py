"""
Módulo de distribuciones de probabilidad
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import numpy as np
import math
from typing import List, Tuple, Optional, Union
from .generadores import GeneradorPseudoaleatorio


class DistribucionDiscreta:
    """Clase para generar variables aleatorias de distribuciones discretas"""
    
    @staticmethod
    def bernoulli(p: float, size: int, generador: GeneradorPseudoaleatorio) -> List[int]:
        """
        Genera variables Bernoulli(p)
        
        Args:
            p: Probabilidad de éxito
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Bernoulli
        """
        if not 0 <= p <= 1:
            raise ValueError("p debe estar en [0, 1]")
        
        return [1 if generador.siguiente() < p else 0 for _ in range(size)]
    
    @staticmethod
    def binomial(n: int, p: float, size: int, generador: GeneradorPseudoaleatorio) -> List[int]:
        """
        Genera variables Binomial(n, p)
        
        Args:
            n: Número de ensayos
            p: Probabilidad de éxito
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Binomial
        """
        if n <= 0:
            raise ValueError("n debe ser positivo")
        if not 0 <= p <= 1:
            raise ValueError("p debe estar en [0, 1]")
        
        # Método directo: suma de Bernoullis
        resultados = []
        for _ in range(size):
            exitos = sum(1 for _ in range(n) if generador.siguiente() < p)
            resultados.append(exitos)
        return resultados
    
    @staticmethod
    def poisson(lam: float, size: int, generador: GeneradorPseudoaleatorio) -> List[int]:
        """
        Genera variables Poisson(λ) usando el algoritmo de Knuth
        
        Args:
            lam: Parámetro de tasa
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Poisson
        """
        if lam <= 0:
            raise ValueError("λ debe ser positivo")
        
        resultados = []
        L = math.exp(-lam)
        
        for _ in range(size):
            k = 0
            p = 1.0
            while p > L:
                k += 1
                p *= generador.siguiente()
            resultados.append(k - 1)
        
        return resultados
    
    @staticmethod
    def geometrica(p: float, size: int, generador: GeneradorPseudoaleatorio) -> List[int]:
        """
        Genera variables Geométrica(p)
        
        Args:
            p: Probabilidad de éxito
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Geométricas
        """
        if not 0 < p <= 1:
            raise ValueError("p debe estar en (0, 1]")
        
        resultados = []
        for _ in range(size):
            intentos = 1
            while generador.siguiente() > p:
                intentos += 1
            resultados.append(intentos)
        
        return resultados
    
    @staticmethod
    def binomial_negativa(r: int, p: float, size: int, generador: GeneradorPseudoaleatorio) -> List[int]:
        """
        Genera variables Binomial Negativa(r, p)
        
        Args:
            r: Número de éxitos requeridos
            p: Probabilidad de éxito
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Binomial Negativa
        """
        if r <= 0:
            raise ValueError("r debe ser positivo")
        if not 0 < p <= 1:
            raise ValueError("p debe estar en (0, 1]")
        
        resultados = []
        for _ in range(size):
            exitos = 0
            intentos = 0
            while exitos < r:
                intentos += 1
                if generador.siguiente() < p:
                    exitos += 1
            resultados.append(intentos)
        
        return resultados


class DistribucionContinua:
    """Clase para generar variables aleatorias de distribuciones continuas"""
    
    @staticmethod
    def uniforme(low: float = 0.0, high: float = 1.0, size: int = 1, 
                generador: GeneradorPseudoaleatorio = None) -> List[float]:
        """
        Genera variables Uniforme(low, high)
        
        Args:
            low: Límite inferior
            high: Límite superior
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Uniformes
        """
        if generador is None:
            generador = GeneradorPseudoaleatorio()
        
        return generador.uniform(low, high, size)
    
    @staticmethod
    def exponencial(lam: float, size: int, generador: GeneradorPseudoaleatorio) -> List[float]:
        """
        Genera variables Exponencial(λ) usando transformada inversa
        
        Args:
            lam: Parámetro de tasa
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Exponenciales
        """
        if lam <= 0:
            raise ValueError("λ debe ser positivo")
        
        resultados = []
        for _ in range(size):
            u = generador.siguiente()
            # Método de la transformada inversa
            x = -math.log(u) / lam
            resultados.append(x)
        return resultados
    
    @staticmethod
    def normal(mu: float, sigma: float, size: int, generador: GeneradorPseudoaleatorio) -> List[float]:
        """
        Genera variables Normal(μ, σ) usando Box-Muller
        
        Args:
            mu: Media
            sigma: Desviación estándar
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Normales
        """
        if sigma <= 0:
            raise ValueError("σ debe ser positivo")
        
        resultados = []
        pairs_needed = (size + 1) // 2
        
        for _ in range(pairs_needed):
            u1 = generador.siguiente()
            u2 = generador.siguiente()
            
            # Transformación Box-Muller
            z0 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
            z1 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
            
            resultados.append(mu + sigma * z0)
            if len(resultados) < size:
                resultados.append(mu + sigma * z1)
        
        return resultados[:size]
    
    @staticmethod
    def normal_polar(mu: float, sigma: float, size: int, generador: GeneradorPseudoaleatorio) -> List[float]:
        """
        Genera variables Normal(μ, σ) usando método polar (más eficiente)
        
        Args:
            mu: Media
            sigma: Desviación estándar
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Normales
        """
        if sigma <= 0:
            raise ValueError("σ debe ser positivo")
        
        resultados = []
        pairs_needed = (size + 1) // 2
        
        for _ in range(pairs_needed):
            while True:
                u1 = generador.siguiente() * 2 - 1  # [-1, 1]
                u2 = generador.siguiente() * 2 - 1
                s = u1*u1 + u2*u2
                
                if 0 < s < 1:
                    break
            
            # Transformación polar
            z0 = u1 * math.sqrt(-2 * math.log(s) / s)
            z1 = u2 * math.sqrt(-2 * math.log(s) / s)
            
            resultados.append(mu + sigma * z0)
            if len(resultados) < size:
                resultados.append(mu + sigma * z1)
        
        return resultados[:size]
    
    @staticmethod
    def gamma(alpha: float, beta: float, size: int, generador: GeneradorPseudoaleatorio) -> List[float]:
        """
        Genera variables Gamma(α, β) usando método de aceptación-rechazo
        
        Args:
            alpha: Parámetro de forma
            beta: Parámetro de escala
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Gamma
        """
        if alpha <= 0 or beta <= 0:
            raise ValueError("α y β deben ser positivos")
        
        resultados = []
        for _ in range(size):
            # Algoritmo simple para alpha > 1
            if alpha > 1:
                a = 1 / math.sqrt(2 * alpha - 1)
                b = alpha - math.log(4)
                c = alpha + 1 / a
                
                while True:
                    u1 = generador.siguiente()
                    u2 = generador.siguiente()
                    
                    v = a * math.log(u1 / (1 - u1))
                    y = alpha * math.exp(v)
                    z = u1 * u1 * u2
                    w = b + c * v - y
                    
                    if w + 1 - math.log(4) >= 0 or w >= math.log(z):
                        resultados.append(y / beta)
                        break
            else:
                # Para alpha <= 1
                while True:
                    u = generador.siguiente()
                    v = generador.siguiente()
                    
                    if u <= math.e / (math.e + alpha):
                        x = ( (math.e + alpha) * u / math.e ) ** (1 / alpha)
                        if v <= math.exp(-x):
                            resultados.append(x / beta)
                            break
                    else:
                        x = -math.log( (math.e + alpha) * (1 - u) / (alpha * math.e) )
                        if v <= x ** (alpha - 1):
                            resultados.append(x / beta)
                            break
        
        return resultados
    
    @staticmethod
    def lognormal(mu: float, sigma: float, size: int, generador: GeneradorPseudoaleatorio) -> List[float]:
        """
        Genera variables Log-Normal(μ, σ)
        
        Args:
            mu: Media del logaritmo
            sigma: Desviación estándar del logaritmo
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Log-Normales
        """
        normales = DistribucionContinua.normal(mu, sigma, size, generador)
        return [math.exp(x) for x in normales]
    
    @staticmethod
    def weibull(alpha: float, beta: float, size: int, generador: GeneradorPseudoaleatorio) -> List[float]:
        """
        Genera variables Weibull(α, β)
        
        Args:
            alpha: Parámetro de forma
            beta: Parámetro de escala
            size: Número de muestras
            generador: Generador pseudoaleatorio
            
        Returns:
            Lista de variables Weibull
        """
        if alpha <= 0 or beta <= 0:
            raise ValueError("α y β deben ser positivos")
        
        resultados = []
        for _ in range(size):
            u = generador.siguiente()
            x = beta * (-math.log(u)) ** (1 / alpha)
            resultados.append(x)
        
        return resultados


class Estadisticos:
    """Clase para cálculos estadísticos de distribuciones"""
    
    @staticmethod
    def resumen_datos(datos: List[float]) -> dict:
        """
        Calcula estadísticos descriptivos de un conjunto de datos
        
        Args:
            datos: Lista de valores numéricos
            
        Returns:
            Diccionario con estadísticos
        """
        if not datos:
            raise ValueError("La lista de datos no puede estar vacía")
        
        arr = np.array(datos)
        
        return {
            'n': len(datos),
            'media': float(np.mean(arr)),
            'mediana': float(np.median(arr)),
            'moda': float(Estadisticos._calcular_moda(arr)),
            'desviacion_estandar': float(np.std(arr)),
            'varianza': float(np.var(arr)),
            'minimo': float(np.min(arr)),
            'maximo': float(np.max(arr)),
            'rango': float(np.max(arr) - np.min(arr)),
            'q1': float(np.percentile(arr, 25)),
            'q3': float(np.percentile(arr, 75)),
            'asimetria': float(Estadisticos._calcular_asimetria(arr)),
            'curtosis': float(Estadisticos._calcular_curtosis(arr))
        }
    
    @staticmethod
    def _calcular_moda(arr: np.ndarray) -> float:
        """Calcula la moda de un array"""
        valores, conteos = np.unique(arr, return_counts=True)
        return valores[np.argmax(conteos)]
    
    @staticmethod
    def _calcular_asimetria(arr: np.ndarray) -> float:
        """Calcula el coeficiente de asimetría"""
        n = len(arr)
        if n < 2:
            return 0.0
        
        media = np.mean(arr)
        std = np.std(arr)
        if std == 0:
            return 0.0
        
        return float(np.sum((arr - media)**3) / (n * std**3))
    
    @staticmethod
    def _calcular_curtosis(arr: np.ndarray) -> float:
        """Calcula el coeficiente de curtosis"""
        n = len(arr)
        if n < 2:
            return 0.0
        
        media = np.mean(arr)
        std = np.std(arr)
        if std == 0:
            return 0.0
        
        return float(np.sum((arr - media)**4) / (n * std**4)) - 3