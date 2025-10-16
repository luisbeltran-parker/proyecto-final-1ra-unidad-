import random
import string
from typing import List, Dict, Any, Optional, Union
from datetime import datetime, timedelta
import hashlib
import json

class Helpers:
    """
    Clase con funciones auxiliares generales
    """
    
    @staticmethod
    def generar_id_unico(prefijo: str = "id") -> str:
        """
        Genera un ID único basado en timestamp y random
        
        Args:
            prefijo (str): Prefijo para el ID
            
        Returns:
            str: ID único
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
        return f"{prefijo}_{timestamp}_{random_str}"
    
    @staticmethod
    def formatear_numero(numero: float, decimales: int = 4) -> str:
        """
        Formatea un número con decimales específicos
        
        Args:
            numero (float): Número a formatear
            decimales (int): Número de decimales
            
        Returns:
            str: Número formateado
        """
        if numero is None:
            return "N/A"
            
        try:
            return f"{numero:.{decimales}f}"
        except (ValueError, TypeError):
            return str(numero)
    
    @staticmethod
    def formatear_lista_numeros(numeros: List[float], 
                               max_elementos: int = 10, 
                               decimales: int = 2) -> str:
        """
        Formatea una lista de números para mostrar
        
        Args:
            numeros (List[float]): Lista de números
            max_elementos (int): Máximo de elementos a mostrar
            decimales (int): Decimales para formateo
            
        Returns:
            str: Lista formateada
        """
        if not numeros:
            return "[]"
            
        if len(numeros) <= max_elementos:
            elementos = [Helpers.formatear_numero(n, decimales) for n in numeros]
            return f"[{', '.join(elementos)}]"
        else:
            primeros = [Helpers.formatear_numero(n, decimales) for n in numeros[:3]]
            ultimos = [Helpers.formatear_numero(n, decimales) for n in numeros[-3:]]
            return f"[{', '.join(primeros)}, ..., {', '.join(ultimos)}] ({len(numeros)} elementos)"
    
    @staticmethod
    def calcular_hash_datos(datos: Any) -> str:
        """
        Calcula hash MD5 de datos para verificar integridad
        
        Args:
            datos (Any): Datos a hashear
            
        Returns:
            str: Hash MD5
        """
        if isinstance(datos, (list, dict)):
            datos_str = json.dumps(datos, sort_keys=True)
        else:
            datos_str = str(datos)
            
        return hashlib.md5(datos_str.encode()).hexdigest()
    
    @staticmethod
    def crear_resumen_estadistico(estadisticas: Dict[str, float]) -> Dict[str, Any]:
        """
        Crea un resumen legible de estadísticas
        
        Args:
            estadisticas (Dict): Estadísticas a resumir
            
        Returns:
            Dict: Resumen formateado
        """
        resumen = {}
        
        for clave, valor in estadisticas.items():
            if isinstance(valor, float):
                resumen[clave] = Helpers.formatear_numero(valor)
            else:
                resumen[clave] = valor
                
        return resumen
    
    @staticmethod
    def validar_y_convertir_lista(valores: List[str], 
                                 tipo: type = float) -> List[Any]:
        """
        Valida y convierte una lista de strings a números
        
        Args:
            valores (List[str]): Valores a convertir
            tipo (type): Tipo de conversión (float o int)
            
        Returns:
            List: Lista convertida
        """
        resultados = []
        errores = []
        
        for i, valor in enumerate(valores):
            try:
                if tipo == float:
                    resultados.append(float(valor))
                elif tipo == int:
                    resultados.append(int(valor))
                else:
                    resultados.append(valor)
            except (ValueError, TypeError):
                errores.append(f"Valor inválido en posición {i}: '{valor}'")
                
        if errores:
            raise ValueError(f"Errores en conversión: {', '.join(errores)}")
            
        return resultados
    
    @staticmethod
    def dividir_lista_en_partes(lista: List[Any], 
                               n_partes: int) -> List[List[Any]]:
        """
        Divide una lista en n partes aproximadamente iguales
        
        Args:
            lista (List): Lista a dividir
            n_partes (int): Número de partes
            
        Returns:
            List[List]: Lista de listas
        """
        if n_partes <= 0:
            return [lista]
            
        k, m = divmod(len(lista), n_partes)
        return [lista[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] 
                for i in range(n_partes)]
    
    @staticmethod
    def calcular_tiempo_restante(iteracion_actual: int, 
                                total_iteraciones: int, 
                                tiempo_inicio: datetime) -> str:
        """
        Calcula el tiempo restante estimado para un proceso
        
        Args:
            iteracion_actual (int): Iteración actual
            total_iteraciones (int): Total de iteraciones
            tiempo_inicio (datetime): Tiempo de inicio
            
        Returns:
            str: Tiempo restante formateado
        """
        if iteracion_actual <= 0 or total_iteraciones <= 0:
            return "Calculando..."
            
        tiempo_transcurrido = datetime.now() - tiempo_inicio
        progreso = iteracion_actual / total_iteraciones
        
        if progreso == 0:
            return "Calculando..."
            
        tiempo_total_estimado = tiempo_transcurrido / progreso
        tiempo_restante = tiempo_total_estimado - tiempo_transcurrido
        
        # Convertir a formato legible
        segundos_totales = int(tiempo_restante.total_seconds())
        
        if segundos_totales < 60:
            return f"{segundos_totales} segundos"
        elif segundos_totales < 3600:
            minutos = segundos_totales // 60
            segundos = segundos_totales % 60
            return f"{minutos} min {segundos} seg"
        else:
            horas = segundos_totales // 3600
            minutos = (segundos_totales % 3600) // 60
            return f"{horas} h {minutos} min"
    
    @staticmethod
    def crear_paginacion(total_elementos: int, 
                        pagina_actual: int, 
                        elementos_por_pagina: int) -> Dict[str, Any]:
        """
        Crea información de paginación
        
        Args:
            total_elementos (int): Total de elementos
            pagina_actual (int): Página actual
            elementos_por_pagina (int): Elementos por página
            
        Returns:
            Dict: Información de paginación
        """
        total_paginas = max(1, (total_elementos + elementos_por_pagina - 1) // elementos_por_pagina)
        pagina_actual = max(1, min(pagina_actual, total_paginas))
        
        inicio = (pagina_actual - 1) * elementos_por_pagina
        fin = min(inicio + elementos_por_pagina, total_elementos)
        
        return {
            'pagina_actual': pagina_actual,
            'total_paginas': total_paginas,
            'total_elementos': total_elementos,
            'elementos_por_pagina': elementos_por_pagina,
            'inicio': inicio,
            'fin': fin,
            'tiene_anterior': pagina_actual > 1,
            'tiene_siguiente': pagina_actual < total_paginas
        }
    
    @staticmethod
    def limpiar_diccionario_nulos(diccionario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Elimina valores None y vacíos de un diccionario
        
        Args:
            diccionario (Dict): Diccionario a limpiar
            
        Returns:
            Dict: Diccionario limpio
        """
        return {k: v for k, v in diccionario.items() 
                if v is not None and v != '' and v != [] and v != {}}
    
    @staticmethod
    def obtener_timestamp_legible(timestamp: Optional[datetime] = None) -> str:
        """
        Convierte timestamp a formato legible
        
        Args:
            timestamp (datetime): Timestamp a convertir
            
        Returns:
            str: Timestamp formateado
        """
        if timestamp is None:
            timestamp = datetime.now()
            
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")