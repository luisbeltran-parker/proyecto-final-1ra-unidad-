"""
Módulo de pruebas de bondad de ajuste
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import numpy as np
from scipy import stats
from typing import List, Dict, Tuple, Optional
import math


class PruebasBondad:
    """Clase para realizar pruebas de bondad de ajuste estadístico"""
    
    @staticmethod
    def chi_cuadrado(datos: List[float], distribucion: str, params: Tuple, 
                    bins: int = 10, alpha: float = 0.05) -> Dict:
        """
        Realiza la prueba de Chi-cuadrado de bondad de ajuste
        
        Args:
            datos: Datos a evaluar
            distribucion: Nombre de la distribución ('normal', 'exponencial', etc.)
            params: Parámetros de la distribución
            bins: Número de intervalos
            alpha: Nivel de significancia
            
        Returns:
            Diccionario con resultados de la prueba
        """
        datos_arr = np.array(datos)
        n = len(datos_arr)
        
        # Crear histograma observado
        observado, bordes = np.histogram(datos_arr, bins=bins)
        
        # Calcular frecuencias esperadas
        esperado = PruebasBondad._calcular_frecuencias_esperadas(
            distribucion, params, bordes, n
        )
        
        # Aplicar regla de Cochran: frecuencias esperadas >= 5
        mascara = esperado >= 5
        observado_filtrado = observado[mascara]
        esperado_filtrado = esperado[mascara]
        
        if len(observado_filtrado) < 2:
            raise ValueError("No hay suficientes intervalos con frecuencia esperada >= 5")
        
        # Calcular estadístico Chi-cuadrado
        chi2 = np.sum((observado_filtrado - esperado_filtrado)**2 / esperado_filtrado)
        grados_libertad = len(observado_filtrado) - len(params) - 1
        
        if grados_libertad <= 0:
            grados_libertad = 1
        
        # Calcular p-valor
        p_valor = 1 - stats.chi2.cdf(chi2, grados_libertad)
        
        return {
            'prueba': 'Chi-cuadrado',
            'distribucion': distribucion,
            'estadistico': chi2,
            'p_valor': p_valor,
            'grados_libertad': grados_libertad,
            'alpha': alpha,
            'rechazar_h0': p_valor < alpha,
            'observado': observado_filtrado.tolist(),
            'esperado': esperado_filtrado.tolist(),
            'bordes': bordes[:-1][mascara].tolist(),
            'n_bins_efectivos': len(observado_filtrado)
        }
    
    @staticmethod
    def kolmogorov_smirnov(datos: List[float], distribucion: str, 
                          params: Tuple, alpha: float = 0.05) -> Dict:
        """
        Realiza la prueba de Kolmogorov-Smirnov
        
        Args:
            datos: Datos a evaluar
            distribucion: Nombre de la distribución
            params: Parámetros de la distribución
            alpha: Nivel de significancia
            
        Returns:
            Diccionario con resultados de la prueba
        """
        datos_ordenados = np.sort(datos)
        n = len(datos_ordenados)
        
        # CDF empírica
        cdf_empirica = np.arange(1, n + 1) / n
        
        # CDF teórica
        cdf_teorica = PruebasBondad._calcular_cdf_teorica(
            distribucion, params, datos_ordenados
        )
        
        # Calcular estadístico D
        D_plus = np.max(cdf_empirica - cdf_teorica)
        D_minus = np.max(cdf_teorica - cdf_empirica)
        D = np.max([D_plus, D_minus])
        
        # Calcular valor crítico aproximado
        valor_critico = PruebasBondad._valor_critico_ks(alpha, n)
        
        # Calcular p-valor aproximado
        p_valor = PruebasBondad._p_valor_ks(D, n)
        
        return {
            'prueba': 'Kolmogorov-Smirnov',
            'distribucion': distribucion,
            'estadistico': D,
            'p_valor': p_valor,
            'valor_critico': valor_critico,
            'alpha': alpha,
            'rechazar_h0': D > valor_critico,
            'cdf_empirica': cdf_empirica.tolist(),
            'cdf_teorica': cdf_teorica.tolist(),
            'datos_ordenados': datos_ordenados.tolist(),
            'D_plus': D_plus,
            'D_minus': D_minus
        }
    
    @staticmethod
    def anderson_darling(datos: List[float], distribucion: str, 
                        params: Tuple) -> Dict:
        """
        Realiza la prueba de Anderson-Darling (versión simplificada)
        
        Args:
            datos: Datos a evaluar
            distribucion: Nombre de la distribución
            params: Parámetros de la distribución
            
        Returns:
            Diccionario con resultados de la prueba
        """
        datos_ordenados = np.sort(datos)
        n = len(datos_ordenados)
        
        # CDF teórica
        cdf_teorica = PruebasBondad._calcular_cdf_teorica(
            distribucion, params, datos_ordenados
        )
        
        # Calcular estadístico A²
        A2 = -n
        for i in range(n):
            term1 = (2 * (i + 1) - 1) * math.log(cdf_teorica[i])
            term2 = (2 * n + 1 - 2 * (i + 1)) * math.log(1 - cdf_teorica[i])
            A2 -= (term1 + term2) / n
        
        return {
            'prueba': 'Anderson-Darling',
            'distribucion': distribucion,
            'estadistico': A2,
            'n': n
        }
    
    @staticmethod
    def _calcular_frecuencias_esperadas(distribucion: str, params: Tuple, 
                                       bordes: np.ndarray, n: int) -> np.ndarray:
        """Calcula frecuencias esperadas para Chi-cuadrado"""
        esperado = []
        
        for i in range(len(bordes) - 1):
            if distribucion == 'normal':
                prob = (stats.norm.cdf(bordes[i+1], *params) - 
                       stats.norm.cdf(bordes[i], *params))
            elif distribucion == 'exponencial':
                prob = (stats.expon.cdf(bordes[i+1], *params) - 
                       stats.expon.cdf(bordes[i], *params))
            elif distribucion == 'uniforme':
                prob = (stats.uniform.cdf(bordes[i+1], *params) - 
                       stats.uniform.cdf(bordes[i], *params))
            else:
                raise ValueError(f"Distribución {distribucion} no soportada")
            
            esperado.append(n * prob)
        
        return np.array(esperado)
    
    @staticmethod
    def _calcular_cdf_teorica(distribucion: str, params: Tuple, 
                             datos: np.ndarray) -> np.ndarray:
        """Calcula CDF teórica para KS"""
        if distribucion == 'normal':
            return stats.norm.cdf(datos, *params)
        elif distribucion == 'exponencial':
            return stats.expon.cdf(datos, *params)
        elif distribucion == 'uniforme':
            return stats.uniform.cdf(datos, *params)
        else:
            raise ValueError(f"Distribución {distribucion} no soportada")
    
    @staticmethod
    def _valor_critico_ks(alpha: float, n: int) -> float:
        """Calcula valor crítico para KS"""
        # Valores críticos aproximados
        if alpha == 0.01:
            return 1.63 / math.sqrt(n)
        elif alpha == 0.05:
            return 1.36 / math.sqrt(n)
        elif alpha == 0.10:
            return 1.22 / math.sqrt(n)
        else:
            return 1.36 / math.sqrt(n)  # Por defecto alpha=0.05
    
    @staticmethod
    def _p_valor_ks(D: float, n: int) -> float:
        """Calcula p-valor aproximado para KS"""
        # Aproximación de Miller
        if n > 35:
            return 2 * math.exp(-2 * (D * math.sqrt(n) + 0.12 + 0.11/math.sqrt(n))**2)
        else:
            # Para muestras pequeñas, usar aproximación simple
            return max(0, 1 - math.exp(-2 * n * D**2))
    
    @staticmethod
    def identificar_distribucion(datos: List[float], distribuciones: List[str] = None) -> Dict:
        """
        Identifica la distribución que mejor se ajusta a los datos
        
        Args:
            datos: Datos a evaluar
            distribuciones: Lista de distribuciones a probar
            
        Returns:
            Diccionario con resultados de identificación
        """
        if distribuciones is None:
            distribuciones = ['normal', 'exponencial', 'uniforme']
        
        resultados = []
        datos_arr = np.array(datos)
        
        for dist_name in distribuciones:
            try:
                # Estimar parámetros
                if dist_name == 'normal':
                    params = (np.mean(datos_arr), np.std(datos_arr))
                    prueba_ks = PruebasBondad.kolmogorov_smirnov(datos, dist_name, params)
                elif dist_name == 'exponencial':
                    params = (0, 1/np.mean(datos_arr))  # loc, scale
                    prueba_ks = PruebasBondad.kolmogorov_smirnov(datos, dist_name, params)
                elif dist_name == 'uniforme':
                    params = (np.min(datos_arr), np.max(datos_arr) - np.min(datos_arr))
                    prueba_ks = PruebasBondad.kolmogorov_smirnov(datos, dist_name, params)
                else:
                    continue
                
                resultados.append({
                    'distribucion': dist_name,
                    'parametros': params,
                    'estadistico_ks': prueba_ks['estadistico'],
                    'p_valor_ks': prueba_ks['p_valor'],
                    'ajuste_ks': 1 - prueba_ks['estadistico']  # Métrica de ajuste simple
                })
                
            except Exception as e:
                continue
        
        # Ordenar por mejor ajuste
        resultados.sort(key=lambda x: x['estadistico_ks'])
        
        return {
            'mejor_ajuste': resultados[0] if resultados else None,
            'todos_resultados': resultados,
            'distribucion_recomendada': resultados[0]['distribucion'] if resultados else None
        }