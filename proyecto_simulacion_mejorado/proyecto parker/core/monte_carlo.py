"""
Módulo de métodos de Monte Carlo
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import numpy as np
import math
from typing import List, Dict, Tuple, Optional
from .generadores import GeneradorPseudoaleatorio


class MonteCarlo:
    """Clase para implementar simulaciones de Monte Carlo"""
    
    @staticmethod
    def estimar_pi(n_puntos: int, generador: GeneradorPseudoaleatorio) -> Dict:
        """
        Estima el valor de π usando el método de Monte Carlo
        
        Args:
            n_puntos: Número de puntos a generar
            generador: Generador pseudoaleatorio
            
        Returns:
            Diccionario con resultados de la estimación
        """
        dentro_circulo = 0
        puntos_x = []
        puntos_y = []
        colores = []
        
        for i in range(n_puntos):
            x = generador.siguiente() * 2 - 1  # Rango [-1, 1]
            y = generador.siguiente() * 2 - 1
            
            puntos_x.append(x)
            puntos_y.append(y)
            
            distancia = x**2 + y**2
            if distancia <= 1:
                dentro_circulo += 1
                colores.append('#00a8ff')  # Azul para puntos dentro
            else:
                colores.append('#ff4757')  # Rojo para puntos fuera
        
        pi_estimado = 4 * dentro_circulo / n_puntos
        error_absoluto = abs(pi_estimado - math.pi)
        error_relativo = (error_absoluto / math.pi) * 100
        
        # Calcular intervalo de confianza (95%)
        p = dentro_circulo / n_puntos
        std_error = math.sqrt(p * (1 - p) / n_puntos)
        margen_error = 1.96 * std_error
        ic_inferior = 4 * (p - margen_error)
        ic_superior = 4 * (p + margen_error)
        
        return {
            'pi_estimado': pi_estimado,
            'pi_real': math.pi,
            'error_absoluto': error_absoluto,
            'error_relativo': error_relativo,
            'dentro_circulo': dentro_circulo,
            'total_puntos': n_puntos,
            'proporcion_dentro': dentro_circulo / n_puntos,
            'puntos_x': puntos_x,
            'puntos_y': puntos_y,
            'colores': colores,
            'intervalo_confianza': (ic_inferior, ic_superior),
            'margen_error': margen_error * 4
        }
    
    @staticmethod
    def ruina_jugador(capital_inicial: int, objetivo: int, prob_ganar: float,
                     n_simulaciones: int, generador: GeneradorPseudoaleatorio) -> Dict:
        """
        Simula el problema de la ruina del jugador
        
        Args:
            capital_inicial: Capital inicial del jugador
            objetivo: Capital objetivo a alcanzar
            prob_ganar: Probabilidad de ganar cada apuesta
            n_simulaciones: Número de simulaciones a ejecutar
            generador: Generador pseudoaleatorio
            
        Returns:
            Diccionario con resultados de la simulación
        """
        if capital_inicial <= 0:
            raise ValueError("El capital inicial debe ser positivo")
        if objetivo <= capital_inicial:
            raise ValueError("El objetivo debe ser mayor al capital inicial")
        if not 0 <= prob_ganar <= 1:
            raise ValueError("La probabilidad debe estar entre 0 y 1")
        
        ruinas = 0
        exitos = 0
        duraciones = []
        trayectorias = []
        
        for _ in range(n_simulaciones):
            capital = capital_inicial
            pasos = 0
            trayectoria = [capital]
            
            while capital > 0 and capital < objetivo:
                if generador.siguiente() < prob_ganar:
                    capital += 1
                else:
                    capital -= 1
                pasos += 1
                trayectoria.append(capital)
            
            duraciones.append(pasos)
            trayectorias.append(trayectoria)
            
            if capital == 0:
                ruinas += 1
            else:
                exitos += 1
        
        prob_ruina = ruinas / n_simulaciones
        prob_exito = exitos / n_simulaciones
        duracion_promedio = np.mean(duraciones)
        duracion_std = np.std(duraciones)
        
        # Calcular probabilidad teórica (solo para prob_ganar = 0.5)
        prob_ruina_teorica = 0.0
        if prob_ganar == 0.5:
            prob_ruina_teorica = 1 - capital_inicial / objetivo
        
        return {
            'prob_ruina': prob_ruina,
            'prob_exito': prob_exito,
            'prob_ruina_teorica': prob_ruina_teorica,
            'duracion_promedio': duracion_promedio,
            'duracion_std': duracion_std,
            'duraciones': duraciones,
            'trayectorias': trayectorias,
            'ruinas': ruinas,
            'exitos': exitos,
            'n_simulaciones': n_simulaciones,
            'capital_inicial': capital_inicial,
            'objetivo': objetivo,
            'prob_ganar': prob_ganar
        }
    
    @staticmethod
    def integracion_montecarlo(funcion, a: float, b: float, 
                              n_puntos: int, generador: GeneradorPseudoaleatorio) -> Dict:
        """
        Calcula integral definida usando Monte Carlo
        
        Args:
            funcion: Función a integrar
            a: Límite inferior
            b: Límite superior
            n_puntos: Número de puntos
            generador: Generador pseudoaleatorio
            
        Returns:
            Diccionario con resultados de la integración
        """
        if a >= b:
            raise ValueError("El límite inferior debe ser menor al superior")
        
        # Método de muestreo uniforme
        puntos_x = generador.uniform(a, b, n_puntos)
        valores_y = [funcion(x) for x in puntos_x]
        
        integral_estimada = (b - a) * np.mean(valores_y)
        
        # Calcular error
        std_valores = np.std(valores_y)
        error_estandar = (b - a) * std_valores / math.sqrt(n_puntos)
        
        # Intervalo de confianza 95%
        ic_inferior = integral_estimada - 1.96 * error_estandar
        ic_superior = integral_estimada + 1.96 * error_estandar
        
        return {
            'integral_estimada': integral_estimada,
            'error_estandar': error_estandar,
            'intervalo_confianza': (ic_inferior, ic_superior),
            'puntos_x': puntos_x,
            'valores_y': valores_y,
            'n_puntos': n_puntos,
            'rango': (a, b)
        }
    
    @staticmethod
    def simulacion_inventarios(demanda_media: float, tiempo_entrega: float,
                              punto_reorden: float, cantidad_pedido: float,
                              costo_almacenamiento: float, costo_escasez: float,
                              n_dias: int, generador: GeneradorPseudoaleatorio) -> Dict:
        """
        Simula sistema de inventarios con política (s, Q)
        
        Args:
            demanda_media: Demanda promedio por día
            tiempo_entrega: Tiempo de entrega en días
            punto_reorden: Punto de reorden (s)
            cantidad_pedido: Cantidad a pedir (Q)
            costo_almacenamiento: Costo por unidad almacenada
            costo_escasez: Costo por unidad en escasez
            n_dias: Días a simular
            generador: Generador pseudoaleatorio
            
        Returns:
            Diccionario con resultados de la simulación
        """
        inventario = cantidad_pedido
        pedido_pendiente = False
        tiempo_llegada_pedido = 0
        costo_total = 0
        inventario_promedio = 0
        dias_escasez = 0
        
        historial_inventario = []
        historial_costos = []
        
        for dia in range(n_dias):
            # Generar demanda del día (Poisson)
            demanda = MonteCarlo._generar_demanda_poisson(demanda_media, generador)
            
            # Satisfacer demanda
            if inventario >= demanda:
                inventario -= demanda
                costo_almacenamiento_dia = inventario * costo_almacenamiento
                costo_escasez_dia = 0
            else:
                demanda_insatisfecha = demanda - inventario
                inventario = 0
                costo_almacenamiento_dia = 0
                costo_escasez_dia = demanda_insatisfecha * costo_escasez
                dias_escasez += 1
            
            costo_dia = costo_almacenamiento_dia + costo_escasez_dia
            costo_total += costo_dia
            inventario_promedio += inventario
            
            # Verificar si llega pedido
            if pedido_pendiente and dia >= tiempo_llegada_pedido:
                inventario += cantidad_pedido
                pedido_pendiente = False
            
            # Hacer pedido si es necesario
            if not pedido_pendiente and inventario <= punto_reorden:
                pedido_pendiente = True
                tiempo_llegada_pedido = dia + tiempo_entrega
            
            historial_inventario.append(inventario)
            historial_costos.append(costo_dia)
        
        inventario_promedio /= n_dias
        costo_promedio_dia = costo_total / n_dias
        proporcion_escasez = dias_escasez / n_dias
        
        return {
            'costo_total': costo_total,
            'costo_promedio_dia': costo_promedio_dia,
            'inventario_promedio': inventario_promedio,
            'dias_escasez': dias_escasez,
            'proporcion_escasez': proporcion_escasez,
            'historial_inventario': historial_inventario,
            'historial_costos': historial_costos,
            'nivel_servicio': 1 - proporcion_escasez
        }
    
    @staticmethod
    def _generar_demanda_poisson(media: float, generador: GeneradorPseudoaleatorio) -> int:
        """Genera demanda con distribución Poisson"""
        L = math.exp(-media)
        k = 0
        p = 1.0
        while p > L:
            k += 1
            p *= generador.siguiente()
        return k - 1
    
    @staticmethod
    def analisis_sensibilidad(parametros_base: Dict, variacion: float,
                             n_simulaciones: int, generador: GeneradorPseudoaleatorio) -> Dict:
        """
        Realiza análisis de sensibilidad para simulaciones Monte Carlo
        
        Args:
            parametros_base: Parámetros base de la simulación
            variacion: Porcentaje de variación (±)
            n_simulaciones: Número de simulaciones por escenario
            generador: Generador pseudoaleatorio
            
        Returns:
            Diccionario con resultados del análisis de sensibilidad
        """
        resultados = {}
        
        for param_name, param_value in parametros_base.items():
            if isinstance(param_value, (int, float)):
                # Variación positiva
                valor_pos = param_value * (1 + variacion)
                parametros_pos = parametros_base.copy()
                parametros_pos[param_name] = valor_pos
                
                # Variación negativa
                valor_neg = param_value * (1 - variacion)
                parametros_neg = parametros_base.copy()
                parametros_neg[param_name] = valor_neg
                
                # Ejecutar simulaciones (ejemplo con ruina del jugador)
                try:
                    resultado_base = MonteCarlo.ruina_jugador(**parametros_base, 
                                                             n_simulaciones=n_simulaciones,
                                                             generador=generador)
                    resultado_pos = MonteCarlo.ruina_jugador(**parametros_pos, 
                                                           n_simulaciones=n_simulaciones,
                                                           generador=generador)
                    resultado_neg = MonteCarlo.ruina_jugador(**parametros_neg, 
                                                           n_simulaciones=n_simulaciones,
                                                           generador=generador)
                    
                    sensibilidad = (resultado_pos['prob_ruina'] - resultado_neg['prob_ruina']) / (2 * variacion * param_value)
                    
                    resultados[param_name] = {
                        'sensibilidad': sensibilidad,
                        'base': resultado_base['prob_ruina'],
                        'positivo': resultado_pos['prob_ruina'],
                        'negativo': resultado_neg['prob_ruina'],
                        'impacto': abs(sensibilidad) * variacion * param_value
                    }
                except:
                    continue
        
        # Ordenar por impacto
        resultados_ordenados = dict(sorted(
            resultados.items(), 
            key=lambda x: x[1]['impacto'], 
            reverse=True
        ))
        
        return {
            'resultados': resultados_ordenados,
            'parametro_mas_sensible': next(iter(resultados_ordenados)) if resultados_ordenados else None,
            'variacion_utilizada': variacion
        }