"""
Módulo de exportación de datos
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np
from tkinter import filedialog, messagebox


class ExportadorDatos:
    """Clase para exportar datos y resultados en diferentes formatos"""
    
    @staticmethod
    def exportar_txt(datos: List, ruta_archivo: str, 
                    metadatos: Optional[Dict] = None) -> bool:
        """
        Exporta datos a archivo de texto
        
        Args:
            datos: Lista de datos a exportar
            ruta_archivo: Ruta del archivo destino
            metadatos: Metadatos adicionales
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                # Escribir encabezado
                f.write("# Datos exportados - Sistema de Simulación Computacional\n")
                f.write(f"# Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                if metadatos:
                    for key, value in metadatos.items():
                        f.write(f"# {key}: {value}\n")
                
                f.write("# " + "="*50 + "\n")
                f.write("# DATOS:\n")
                
                # Escribir datos
                for i, dato in enumerate(datos, 1):
                    if isinstance(dato, (int, float)):
                        f.write(f"{dato:.10f}\n")
                    else:
                        f.write(f"{dato}\n")
            
            return True
            
        except Exception as e:
            print(f"Error exportando TXT: {e}")
            return False
    
    @staticmethod
    def exportar_csv(datos: List, ruta_archivo: str,
                    metadatos: Optional[Dict] = None) -> bool:
        """
        Exporta datos a archivo CSV
        
        Args:
            datos: Lista de datos a exportar
            ruta_archivo: Ruta del archivo destino
            metadatos: Metadatos adicionales
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            with open(ruta_archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Escribir metadatos como comentarios
                writer.writerow(['# Sistema de Simulación Computacional'])
                writer.writerow([f'# Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'])
                
                if metadatos:
                    for key, value in metadatos.items():
                        writer.writerow([f'# {key}: {value}'])
                
                writer.writerow(['# DATOS:'])
                writer.writerow(['Indice', 'Valor'])
                
                # Escribir datos
                for i, dato in enumerate(datos, 1):
                    writer.writerow([i, dato])
            
            return True
            
        except Exception as e:
            print(f"Error exportando CSV: {e}")
            return False
    
    @staticmethod
    def exportar_json(datos: List, ruta_archivo: str,
                     metadatos: Optional[Dict] = None) -> bool:
        """
        Exporta datos a archivo JSON
        
        Args:
            datos: Lista de datos a exportar
            ruta_archivo: Ruta del archivo destino
            metadatos: Metadatos adicionales
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            estructura = {
                'metadata': {
                    'sistema': 'Sistema de Simulación Computacional',
                    'fecha_exportacion': datetime.now().isoformat(),
                    'total_datos': len(datos)
                },
                'datos': datos
            }
            
            if metadatos:
                estructura['metadata'].update(metadatos)
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(estructura, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error exportando JSON: {e}")
            return False
    
    @staticmethod
    def exportar_resultados_simulacion(resultados: Dict, ruta_archivo: str,
                                      formato: str = 'txt') -> bool:
        """
        Exporta resultados completos de simulación
        
        Args:
            resultados: Diccionario con resultados
            ruta_archivo: Ruta del archivo destino
            formato: Formato de exportación
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            if formato == 'txt':
                return ExportadorDatos._exportar_resultados_txt(resultados, ruta_archivo)
            elif formato == 'json':
                return ExportadorDatos._exportar_resultados_json(resultados, ruta_archivo)
            else:
                return False
                
        except Exception as e:
            print(f"Error exportando resultados: {e}")
            return False
    
    @staticmethod
    def _exportar_resultados_txt(resultados: Dict, ruta_archivo: str) -> bool:
        """Exporta resultados en formato texto legible"""
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write("RESULTADOS DE SIMULACIÓN COMPUTACIONAL\n")
                f.write("=" * 60 + "\n")
                f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                ExportadorDatos._escribir_diccionario_txt(f, resultados)
            
            return True
        except Exception as e:
            print(f"Error en exportación TXT: {e}")
            return False
    
    @staticmethod
    def _escribir_diccionario_txt(archivo, datos: Dict, nivel: int = 0):
        """Escribe diccionario de forma recursiva en texto"""
        for key, value in datos.items():
            indent = "  " * nivel
            
            if isinstance(value, dict):
                archivo.write(f"{indent}{key}:\n")
                ExportadorDatos._escribir_diccionario_txt(archivo, value, nivel + 1)
            elif isinstance(value, list):
                archivo.write(f"{indent}{key}:\n")
                for i, item in enumerate(value[:10]):  # Mostrar solo primeros 10
                    archivo.write(f"{indent}  [{i}]: {item}\n")
                if len(value) > 10:
                    archivo.write(f"{indent}  ... ({len(value) - 10} elementos más)\n")
            else:
                archivo.write(f"{indent}{key}: {value}\n")
    
    @staticmethod
    def _exportar_resultados_json(resultados: Dict, ruta_archivo: str) -> bool:
        """Exporta resultados en formato JSON"""
        try:
            # Limpiar datos para JSON (convertir numpy types)
            resultados_limpios = ExportadorDatos._limpiar_datos_json(resultados)
            
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                json.dump(resultados_limpios, f, indent=2, ensure_ascii=False, default=str)
            
            return True
        except Exception as e:
            print(f"Error en exportación JSON: {e}")
            return False
    
    @staticmethod
    def _limpiar_datos_json(datos: Any) -> Any:
        """Convierte tipos no serializables a tipos básicos"""
        if isinstance(datos, dict):
            return {k: ExportadorDatos._limpiar_datos_json(v) for k, v in datos.items()}
        elif isinstance(datos, list):
            return [ExportadorDatos._limpiar_datos_json(item) for item in datos]
        elif isinstance(datos, (np.integer, np.int64)):
            return int(datos)
        elif isinstance(datos, (np.floating, np.float64)):
            return float(datos)
        elif isinstance(datos, np.ndarray):
            return datos.tolist()
        else:
            return datos
    
    @staticmethod
    def exportar_grafico(figura, ruta_archivo: str, formato: str = 'png') -> bool:
        """
        Exporta gráfico a archivo
        
        Args:
            figura: Figura de matplotlib
            ruta_archivo: Ruta del archivo destino
            formato: Formato de imagen ('png', 'jpg', 'pdf', 'svg')
            
        Returns:
            True si la exportación fue exitosa
        """
        try:
            figura.savefig(ruta_archivo, format=formato, 
                          dpi=300, bbox_inches='tight', 
                          facecolor=figura.get_facecolor())
            return True
        except Exception as e:
            print(f"Error exportando gráfico: {e}")
            return False
    
    @staticmethod
    def seleccionar_ruta_exportacion(titulo: str = "Guardar archivo",
                                   tipos_archivo: List[tuple] = None,
                                   extension_por_defecto: str = ".txt") -> Optional[str]:
        """
        Abre diálogo para seleccionar ruta de exportación
        
        Args:
            titulo: Título del diálogo
            tipos_archivo: Lista de tipos de archivo
            extension_por_defecto: Extensión por defecto
            
        Returns:
            Ruta seleccionada o None
        """
        if tipos_archivo is None:
            tipos_archivo = [
                ("Archivos de texto", "*.txt"),
                ("Archivos CSV", "*.csv"),
                ("Archivos JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ]
        
        ruta = filedialog.asksaveasfilename(
            title=titulo,
            defaultextension=extension_por_defecto,
            filetypes=tipos_archivo
        )
        
        return ruta if ruta else None
    
    @staticmethod
    def crear_directorio_salida() -> str:
        """
        Crea directorio para salidas si no existe
        
        Returns:
            Ruta del directorio de salida
        """
        directorio = os.path.join(os.getcwd(), "salidas")
        if not os.path.exists(directorio):
            os.makedirs(directorio)
        return directorio
    
    @staticmethod
    def generar_nombre_archivo(prefix: str = "simulacion") -> str:
        """
        Genera nombre de archivo único con timestamp
        
        Args:
            prefix: Prefijo para el nombre
            
        Returns:
            Nombre de archivo único
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}"