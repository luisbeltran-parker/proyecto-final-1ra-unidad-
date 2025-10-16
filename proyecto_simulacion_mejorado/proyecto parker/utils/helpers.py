"""
Módulo de funciones auxiliares y utilidades generales
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import tkinter as tk
from tkinter import ttk
import time
import math
from typing import Any, Callable, List, Dict, Optional
from config import COLORES, FUENTES


class Helpers:
    """Clase con funciones auxiliares generales"""
    
    @staticmethod
    def formatear_numero(numero: float, decimales: int = 6, 
                        notacion_cientifica: bool = False) -> str:
        """
        Formatea un número para mostrar
        
        Args:
            numero: Número a formatear
            decimales: Número de decimales
            notacion_cientifica: Usar notación científica
            
        Returns:
            String formateado
        """
        if numero is None:
            return "N/A"
        
        if math.isnan(numero) or math.isinf(numero):
            return str(numero)
        
        if notacion_cientifica and (abs(numero) >= 1e6 or abs(numero) <= 1e-6):
            return f"{numero:.{decimales}e}"
        else:
            return f"{numero:.{decimales}f}"
    
    @staticmethod
    def formatear_lista_numeros(numeros: List[float], max_elementos: int = 10) -> str:
        """
        Formatea una lista de números para mostrar
        
        Args:
            numeros: Lista de números
            max_elementos: Máximo de elementos a mostrar
            
        Returns:
            String formateado
        """
        if not numeros:
            return "[]"
        
        if len(numeros) <= max_elementos:
            elementos = [Helpers.formatear_numero(x, 4) for x in numeros]
            return f"[{', '.join(elementos)}]"
        else:
            primeros = [Helpers.formatear_numero(x, 4) for x in numeros[:3]]
            ultimos = [Helpers.formatear_numero(x, 4) for x in numeros[-3:]]
            return f"[{', '.join(primeros)}, ..., {', '.join(ultimos)}]"
    
    @staticmethod
    def calcular_tiempo_ejecucion(func: Callable) -> Callable:
        """
        Decorador para calcular tiempo de ejecución
        
        Args:
            func: Función a decorar
            
        Returns:
            Función decorada
        """
        def wrapper(*args, **kwargs):
            inicio = time.time()
            resultado = func(*args, **kwargs)
            fin = time.time()
            tiempo_ejecucion = fin - inicio
            
            print(f"⏱️  {func.__name__} ejecutado en {tiempo_ejecucion:.4f} segundos")
            
            # Si la función retorna un diccionario, agregar tiempo de ejecución
            if isinstance(resultado, dict):
                resultado['tiempo_ejecucion'] = tiempo_ejecucion
            
            return resultado
        return wrapper
    
    @staticmethod
    def crear_tooltip(widget: tk.Widget, texto: str):
        """
        Crea un tooltip para un widget
        
        Args:
            widget: Widget al que agregar tooltip
            texto: Texto del tooltip
        """
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry("+0+0")
        tooltip.withdraw()
        
        label = tk.Label(tooltip, text=texto, justify='left',
                        background="#ffffe0", relief='solid', borderwidth=1,
                        font=('Segoe UI', 9))
        label.pack()
        
        def mostrar_tooltip(event):
            x = event.x_root + 10
            y = event.y_root + 10
            tooltip.wm_geometry(f"+{x}+{y}")
            tooltip.deiconify()
        
        def ocultar_tooltip(event):
            tooltip.withdraw()
        
        widget.bind('<Enter>', mostrar_tooltip)
        widget.bind('<Leave>', ocultar_tooltip)
        widget.bind('<Motion>', mostrar_tooltip)
    
    @staticmethod
    def limpiar_frame(frame: tk.Frame):
        """
        Limpia todos los widgets de un frame
        
        Args:
            frame: Frame a limpiar
        """
        for widget in frame.winfo_children():
            widget.destroy()
    
    @staticmethod
    def centrar_ventana(ventana: tk.Tk):
        """
        Centra una ventana en la pantalla
        
        Args:
            ventana: Ventana a centrar
        """
        ventana.update_idletasks()
        
        ancho = ventana.winfo_width()
        alto = ventana.winfo_height()
        
        x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
        y = (ventana.winfo_screenheight() // 2) - (alto // 2)
        
        ventana.geometry(f'{ancho}x{alto}+{x}+{y}')
    
    @staticmethod
    def crear_marco_con_titulo(parent: tk.Widget, titulo: str, 
                              padding: int = 10) -> tk.Frame:
        """
        Crea un frame con título decorativo
        
        Args:
            parent: Widget padre
            titulo: Título del marco
            padding: Padding interno
            
        Returns:
            Frame con título
        """
        marco_principal = tk.Frame(parent, bg=COLORES['fondo_principal'])
        marco_principal.pack(fill='x', pady=5)
        
        # Título
        label_titulo = tk.Label(
            marco_principal,
            text=titulo,
            font=FUENTES['subtitulo'],
            fg=COLORES['acento_primario'],
            bg=COLORES['fondo_principal']
        )
        label_titulo.pack(anchor='w', padx=5)
        
        # Línea decorativa
        linea = tk.Frame(
            marco_principal,
            height=1,
            bg=COLORES['acento_primario']
        )
        linea.pack(fill='x', pady=(2, 5))
        
        # Frame de contenido
        frame_contenido = tk.Frame(
            marco_principal,
            bg=COLORES['fondo_secundario'],
            relief='flat'
        )
        frame_contenido.pack(fill='x', padx=2, pady=(0, 5))
        
        return frame_contenido
    
    @staticmethod
    def crear_barra_progreso(parent: tk.Widget, longitud: int = 200) -> ttk.Progressbar:
        """
        Crea una barra de progreso estilizada
        
        Args:
            parent: Widget padre
            longitud: Longitud de la barra
            
        Returns:
            Barra de progreso
        """
        estilo = ttk.Style()
        estilo.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=COLORES['fondo_terciario'],
            background=COLORES['acento_primario'],
            bordercolor=COLORES['fondo_terciario'],
            lightcolor=COLORES['acento_primario'],
            darkcolor=COLORES['acento_primario']
        )
        
        barra = ttk.Progressbar(
            parent,
            style="Custom.Horizontal.TProgressbar",
            length=longitud,
            mode='indeterminate'
        )
        
        return barra
    
    @staticmethod
    def mostrar_estado_temporal(parent: tk.Widget, mensaje: str, duracion: int = 3000):
        """
        Muestra un mensaje de estado temporal
        
        Args:
            parent: Widget padre
            mensaje: Mensaje a mostrar
            duracion: Duración en milisegundos
        """
        # Implementar mensaje temporal
        pass


class Animaciones:
    """Clase para manejar animaciones y transiciones"""
    
    @staticmethod
    def animar_cambio_color(widget: tk.Widget, color_inicial: str, 
                           color_final: str, duracion: int = 300):
        """
        Anima cambio de color de un widget
        
        Args:
            widget: Widget a animar
            color_inicial: Color inicial
            color_final: Color final
            duracion: Duración en ms
        """
        pasos = 20
        delay = duracion // pasos
        
        # Convertir colores hex a RGB
        def hex_a_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        rgb_inicial = hex_a_rgb(color_inicial)
        rgb_final = hex_a_rgb(color_final)
        
        # Calcular incrementos
        incrementos = [
            (rgb_final[i] - rgb_inicial[i]) / pasos 
            for i in range(3)
        ]
        
        def actualizar_color(paso):
            if paso <= pasos:
                # Calcular color intermedio
                r = int(rgb_inicial[0] + incrementos[0] * paso)
                g = int(rgb_inicial[1] + incrementos[1] * paso)
                b = int(rgb_inicial[2] + incrementos[2] * paso)
                
                color_actual = f'#{r:02x}{g:02x}{b:02x}'
                
                try:
                    widget.config(bg=color_actual)
                    widget.after(delay, lambda: actualizar_color(paso + 1))
                except tk.TclError:
                    pass  # Widget destruido
        
        actualizar_color(1)
    
    @staticmethod
    def animar_aparicion(widget: tk.Widget, duracion: int = 400):
        """
        Anima la aparición de un widget
        
        Args:
            widget: Widget a animar
            duracion: Duración en ms
        """
        pasos = 20
        delay = duracion // pasos
        
        def mostrar(paso):
            if paso <= pasos:
                try:
                    alpha = paso / pasos
                    # Simular opacidad cambiando colores
                    widget.update()
                    widget.after(delay, lambda: mostrar(paso + 1))
                except tk.TclError:
                    pass
        
        widget.pack()  # Asegurar que esté visible
        mostrar(1)
    
    @staticmethod
    def efecto_click(widget: tk.Widget, color_original: str = COLORES['acento_primario']):
        """
        Efecto visual al hacer click
        
        Args:
            widget: Widget afectado
            color_original: Color original del widget
        """
        color_clic = COLORES['acento_secundario']
        
        def restaurar():
            try:
                widget.config(bg=color_original)
            except tk.TclError:
                pass
        
        try:
            widget.config(bg=color_clic)
            widget.after(150, restaurar)
        except tk.TclError:
            pass


class GestorCache:
    """Clase para gestión simple de cache en memoria"""
    
    def __init__(self, max_entradas: int = 100):
        self.cache = {}
        self.max_entradas = max_entradas
        self.orden_acceso = []
    
    def obtener(self, clave: str) -> Any:
        """
        Obtiene valor del cache
        
        Args:
            clave: Clave del valor
            
        Returns:
            Valor almacenado o None
        """
        if clave in self.cache:
            # Mover al final (más reciente)
            self.orden_acceso.remove(clave)
            self.orden_acceso.append(clave)
            return self.cache[clave]
        return None
    
    def almacenar(self, clave: str, valor: Any):
        """
        Almacena valor en cache
        
        Args:
            clave: Clave para almacenar
            valor: Valor a almacenar
        """
        if clave in self.cache:
            self.orden_acceso.remove(clave)
        elif len(self.cache) >= self.max_entradas:
            # Eliminar el menos reciente
            clave_antigua = self.orden_acceso.pop(0)
            del self.cache[clave_antigua]
        
        self.cache[clave] = valor
        self.orden_acceso.append(clave)
    
    def limpiar(self):
        """Limpia todo el cache"""
        self.cache.clear()
        self.orden_acceso.clear()
    
    def estadisticas(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del cache
        
        Returns:
            Diccionario con estadísticas
        """
        return {
            'total_entradas': len(self.cache),
            'max_entradas': self.max_entradas,
            'uso_memoria': f"{(sum(len(str(v)) for v in self.cache.values()) / 1024):.2f} KB"
        }