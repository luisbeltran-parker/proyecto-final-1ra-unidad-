"""
Tema y estilos para la aplicación de simulación
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import sys
import os
from pathlib import Path

# Solución robusta para la importación
try:
    # Intentar importación relativa primero
    from ..config import COLORES, FUENTES, INTERFAZ, STYLES, GRAFICOS, SIMULACION, PARAMETROS_DEFAULT, MENSAJES
except ImportError:
    try:
        # Fallback: importación absoluta
        from config import COLORES, FUENTES, INTERFAZ, STYLES, GRAFICOS, SIMULACION, PARAMETROS_DEFAULT, MENSAJES
    except ImportError:
        # Fallback final: agregar ruta manualmente
        current_dir = Path(__file__).parent
        parent_dir = current_dir.parent
        sys.path.append(str(parent_dir))
        from config import COLORES, FUENTES, INTERFAZ, STYLES, GRAFICOS, SIMULACION, PARAMETROS_DEFAULT, MENSAJES

import tkinter as tk
from tkinter import ttk

class ThemeManager:
    """
    Gestor de temas para la aplicación - Mantiene compatibilidad con código existente
    """
    
    def __init__(self, root=None):
        self.root = root
        if root:
            self.estilo = configurar_tema(root)
    
    def configurar_tema(self, root):
        """Configura el tema en una ventana (método de instancia)"""
        self.root = root
        self.estilo = configurar_tema(root)
        return self.estilo
    
    @staticmethod
    def aplicar_tema(root):
        """Método estático para aplicar tema"""
        return configurar_tema(root)
    
    def crear_frame(self, parent, **kwargs):
        """Crea un frame estilizado"""
        return crear_frame_estilizado(parent, **kwargs)
    
    def crear_label(self, parent, texto, estilo_personalizado='TLabel', **kwargs):
        """Crea un label estilizado"""
        return crear_label_estilizado(parent, texto, estilo_personalizado, **kwargs)
    
    def crear_boton(self, parent, texto, comando=None, estilo_personalizado='TButton', **kwargs):
        """Crea un botón estilizado"""
        return crear_boton_estilizado(parent, texto, comando, estilo_personalizado, **kwargs)
    
    def crear_entrada(self, parent, estilo_personalizado='TEntry', **kwargs):
        """Crea una entrada estilizada"""
        return crear_entrada_estilizada(parent, estilo_personalizado, **kwargs)
    
    @property
    def colores(self):
        """Retorna la paleta de colores"""
        return COLORES
    
    @property
    def fuentes(self):
        """Retorna la configuración de fuentes"""
        return FUENTES
    
    @property
    def interfaz(self):
        """Retorna la configuración de interfaz"""
        return INTERFAZ
    
    @property
    def styles(self):
        """Retorna los estilos ttk"""
        return STYLES

# Funciones originales (mantienen compatibilidad)
def configurar_tema(root):
    """
    Configura el tema oscuro personalizado para la aplicación
    
    Args:
        root: Ventana principal de tkinter
    """
    
    # Configurar estilo ttk
    estilo = ttk.Style()
    
    # Configurar tema para diferentes elementos
    estilo.configure('TFrame', 
                    background=COLORES['fondo_principal'])
    
    estilo.configure('TLabel',
                    background=COLORES['fondo_principal'],
                    foreground=COLORES['texto_primario'],
                    font=FUENTES['principal'])
    
    estilo.configure('TButton',
                    background=COLORES['acento_primario'],
                    foreground=COLORES['texto_primario'],
                    font=FUENTES['principal'],
                    borderwidth=0,
                    focuscolor='none')
    
    estilo.configure('TEntry',
                    fieldbackground=COLORES['fondo_secundario'],
                    foreground=COLORES['texto_primario'],
                    insertcolor=COLORES['texto_primario'],
                    borderwidth=1,
                    relief='flat')
    
    estilo.configure('TCombobox',
                    fieldbackground=COLORES['fondo_secundario'],
                    foreground=COLORES['texto_primario'],
                    background=COLORES['fondo_secundario'])
    
    estilo.configure('TNotebook',
                    background=COLORES['fondo_principal'],
                    tabmargins=[2, 5, 2, 0])
    
    estilo.configure('TNotebook.Tab',
                    background=COLORES['fondo_secundario'],
                    foreground=COLORES['texto_secundario'],
                    padding=[15, 5])
    
    # Configurar la ventana principal
    root.configure(bg=COLORES['fondo_principal'])
    
    # Estilos personalizados adicionales
    estilo.configure('Titulo.TLabel',
                    font=FUENTES['titulo'],
                    foreground=COLORES['acento_primario'])
    
    estilo.configure('Subtitulo.TLabel',
                    font=FUENTES['subtitulo'],
                    foreground=COLORES['texto_secundario'])
    
    estilo.configure('Exito.TLabel',
                    foreground=COLORES['exito'])
    
    estilo.configure('Error.TLabel',
                    foreground=COLORES['error'])
    
    estilo.configure('Acento.TButton',
                    background=COLORES['acento_secundario'],
                    foreground=COLORES['texto_primario'])
    
    return estilo

def crear_frame_estilizado(parent, **kwargs):
    """
    Crea un frame con el estilo aplicado
    
    Args:
        parent: Widget padre
        **kwargs: Argumentos adicionales para el Frame
    
    Returns:
        ttk.Frame: Frame estilizado
    """
    frame = ttk.Frame(parent, **kwargs)
    return frame

def crear_label_estilizado(parent, texto, estilo_personalizado='TLabel', **kwargs):
    """
    Crea un label con el estilo aplicado
    
    Args:
        parent: Widget padre
        texto: Texto a mostrar
        estilo_personalizado: Estilo a aplicar
        **kwargs: Argumentos adicionales para el Label
    
    Returns:
        ttk.Label: Label estilizado
    """
    label = ttk.Label(parent, text=texto, style=estilo_personalizado, **kwargs)
    return label

def crear_boton_estilizado(parent, texto, comando=None, estilo_personalizado='TButton', **kwargs):
    """
    Crea un botón con el estilo aplicado
    
    Args:
        parent: Widget padre
        texto: Texto del botón
        comando: Función a ejecutar al hacer clic
        estilo_personalizado: Estilo a aplicar
        **kwargs: Argumentos adicionales para el Button
    
    Returns:
        ttk.Button: Botón estilizado
    """
    boton = ttk.Button(parent, text=texto, command=comando, style=estilo_personalizado, **kwargs)
    return boton

def crear_entrada_estilizada(parent, estilo_personalizado='TEntry', **kwargs):
    """
    Crea una entrada de texto con el estilo aplicado
    
    Args:
        parent: Widget padre
        estilo_personalizado: Estilo a aplicar
        **kwargs: Argumentos adicionales para el Entry
    
    Returns:
        ttk.Entry: Entry estilizado
    """
    entrada = ttk.Entry(parent, style=estilo_personalizado, **kwargs)
    return entrada

def aplicar_tema_widget(widget, tipo_widget='frame'):
    """
    Aplica el tema directamente a un widget existente
    
    Args:
        widget: Widget al que aplicar el tema
        tipo_widget: Tipo de widget ('frame', 'label', 'button', 'entry')
    """
    if tipo_widget == 'frame':
        if isinstance(widget, tk.Frame):
            widget.configure(bg=COLORES['fondo_principal'])
        elif isinstance(widget, ttk.Frame):
            widget.configure(style='TFrame')
    
    elif tipo_widget == 'label':
        if isinstance(widget, tk.Label):
            widget.configure(bg=COLORES['fondo_principal'], 
                           fg=COLORES['texto_primario'],
                           font=FUENTES['principal'])
        elif isinstance(widget, ttk.Label):
            widget.configure(style='TLabel')
    
    elif tipo_widget == 'button':
        if isinstance(widget, tk.Button):
            widget.configure(bg=COLORES['acento_primario'],
                           fg=COLORES['texto_primario'],
                           font=FUENTES['principal'],
                           relief='flat',
                           borderwidth=0)
        elif isinstance(widget, ttk.Button):
            widget.configure(style='TButton')
    
    elif tipo_widget == 'entry':
        if isinstance(widget, tk.Entry):
            widget.configure(bg=COLORES['fondo_secundario'],
                           fg=COLORES['texto_primario'],
                           insertbackground=COLORES['texto_primario'],
                           relief='flat')
        elif isinstance(widget, ttk.Entry):
            widget.configure(style='TEntry')

# Función para verificar que la configuración se cargó correctamente
def verificar_configuracion():
    """Verifica que todas las configuraciones se cargaron correctamente"""
    configuraciones = {
        'COLORES': COLORES,
        'FUENTES': FUENTES, 
        'INTERFAZ': INTERFAZ,
        'STYLES': STYLES,
        'GRAFICOS': GRAFICOS,
        'SIMULACION': SIMULACION
    }
    
    for nombre, config in configuraciones.items():
        if config is not None:
            print(f"✅ {nombre} cargado correctamente")
        else:
            print(f"❌ Error cargando {nombre}")
    
    return all(config is not None for config in configuraciones.values())

# Crear una instancia global para compatibilidad
theme_manager = ThemeManager()

# Si ejecutas este archivo directamente, verifica la configuración
if __name__ == "__main__":
    print("🔧 Verificando configuración del tema...")
    if verificar_configuracion():
        print("🎉 Tema configurado correctamente!")
        print("📦 ThemeManager disponible para importación")
    else:
        print("❌ Error en la configuración del tema")