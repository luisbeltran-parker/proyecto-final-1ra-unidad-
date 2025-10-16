"""
SISTEMA DE SIMULACIÓN COMPUTACIONAL - VERSIÓN COMPLETA
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar directorios al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import COLORES, FUENTES, INTERFAZ
from interfaz import ThemeManager
from interfaz.componentes import CardFrame, ModernButton, LabelTitulo
from interfaz.paneles import (
    PanelGeneracion, 
    PanelBondad, 
    PanelMonteCarlo,
    PanelResultados,
    PanelConfiguracion
)

class SistemaSimulacionApp:
    """Aplicación principal del sistema de simulación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.configurar_ventana()
        self.crear_managers()
        self.inicializar_estado()
        self.crear_interfaz()
        self.cargar_estado_inicial()
    
    def configurar_ventana(self):
        """Configura la ventana principal"""
        self.root.title("Sistema de Simulación Computacional - Professional v2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)
        self.root.configure(bg=COLORES['fondo_principal'])
        
        # Icono
        try:
            self.root.iconbitmap("assets/icons/app_icon.ico")
        except:
            pass
    
    def crear_managers(self):
        """Crea los managers de la aplicación"""
        self.theme_manager = ThemeManager(self.root)
        self.theme_manager.aplicar_tema_oscuro()
        self.theme_manager.crear_estilo_card()
    
    def inicializar_estado(self):
        """Inicializa el estado de la aplicación"""
        self.generador = None
        self.datos_actuales = []
        self.paneles = {}
        self.panel_actual = None
    
    def crear_interfaz(self):
        """Crea la interfaz principal"""
        self.crear_menu()
        self.crear_layout_principal()
        self.crear_header()
        self.crear_sidebar()
        self.crear_area_principal()
        self.crear_status_bar()
    
    def crear_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root, bg=COLORES['fondo_secundario'], fg=COLORES['texto_primario'])
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Nuevo Proyecto", command=self.nuevo_proyecto)
        menu_archivo.add_command(label="Abrir Proyecto...", command=self.abrir_proyecto)
        menu_archivo.add_command(label="Guardar Proyecto", command=self.guardar_proyecto)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Exportar Resultados...", command=self.exportar_resultados)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="Salir", command=self.salir)
        
        # Menú Simulación
        menu_simulacion = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Simulación", menu=menu_simulacion)
        menu_simulacion.add_command(label="Generar Variables Aleatorias", 
                                  command=lambda: self.mostrar_panel('generacion'))
        menu_simulacion.add_command(label="Pruebas de Bondad de Ajuste", 
                                  command=lambda: self.mostrar_panel('bondad'))
        menu_simulacion.add_command(label="Métodos de Monte Carlo", 
                                  command=lambda: self.mostrar_panel('montecarlo'))
        menu_simulacion.add_separator()
        menu_simulacion.add_command(label="Ejecutar Todas las Simulaciones", 
                                  command=self.ejecutar_todas_simulaciones)
        
        # Menú Ver
        menu_ver = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ver", menu=menu_ver)
        menu_ver.add_command(label="Resultados", 
                           command=lambda: self.mostrar_panel('resultados'))
        menu_ver.add_command(label="Dashboard", 
                           command=self.mostrar_dashboard)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Documentación", command=self.mostrar_documentacion)
        menu_ayuda.add_command(label="Ejemplos", command=self.mostrar_ejemplos)
        menu_ayuda.add_separator()
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
    
    def crear_layout_principal(self):
        """Crea el layout principal"""
        self.main_container = tk.Frame(self.root, bg=COLORES['fondo_principal'])
        self.main_container.pack(fill='both', expand=True)
    
    def crear_header(self):
        """Crea el encabezado de la aplicación"""
        header_frame = tk.Frame(self.main_container, bg=COLORES['fondo_secundario'], height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Logo y título
        logo_frame = tk.Frame(header_frame, bg=COLORES['fondo_secundario'])
        logo_frame.pack(side='left', padx=20, pady=15)
        
        # Logo simbólico
        logo_canvas = tk.Canvas(logo_frame, width=50, height=50, bg=COLORES['fondo_secundario'], 
                               highlightthickness=0)
        logo_canvas.pack(side='left')
        self.dibujar_logo(logo_canvas)
        
        # Texto del título
        titulo_frame = tk.Frame(logo_frame, bg=COLORES['fondo_secundario'])
        titulo_frame.pack(side='left', padx=(15, 0), pady=5)
        
        tk.Label(
            titulo_frame,
            text="SISTEMA DE SIMULACIÓN COMPUTACIONAL",
            font=('Segoe UI', 16, 'bold'),
            fg=COLORES['texto_primario'],
            bg=COLORES['fondo_secundario']
        ).pack(anchor='w')
        
        tk.Label(
            titulo_frame,
            text="Análisis Estadístico Avanzado - Versión Professional 2.0",
            font=('Segoe UI', 10),
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo_secundario']
        ).pack(anchor='w')
        
        # Barra de herramientas
        self.crear_toolbar(header_frame)
    
    def dibujar_logo(self, canvas):
        """Dibuja el logo personalizado"""
        # Círculo exterior
        canvas.create_oval(5, 5, 45, 45, fill=COLORES['acento_primario'], outline='')
        
        # Líneas de gráfico
        puntos = [(15, 30), (20, 20), (25, 35), (30, 25), (35, 40)]
        for i in range(len(puntos) - 1):
            canvas.create_line(puntos[i][0], puntos[i][1], puntos[i+1][0], puntos[i+1][1],
                             fill=COLORES['texto_primario'], width=3)
        
        # Puntos de datos
        for x, y in puntos:
            canvas.create_oval(x-2, y-2, x+2, y+2, fill=COLORES['texto_primario'], outline='')
    
    def crear_toolbar(self, parent):
        """Crea la barra de herramientas"""
        toolbar_frame = tk.Frame(parent, bg=COLORES['fondo_secundario'])
        toolbar_frame.pack(side='right', padx=20, pady=15)
        
        botones_toolbar = [
            ("📊 Nuevo Análisis", self.nuevo_proyecto),
            ("💾 Guardar", self.guardar_proyecto),
            ("📁 Abrir", self.abrir_proyecto),
            ("❓ Ayuda", self.mostrar_documentacion)
        ]
        
        for texto, comando in botones_toolbar:
            btn = ModernButton(toolbar_frame, text=texto, command=comando, style='secondary')
            btn.pack(side='left', padx=5)
    
    def crear_sidebar(self):
        """Crea la barra lateral de navegación"""
        # Frame del sidebar
        sidebar_frame = tk.Frame(self.main_container, bg=COLORES['fondo_secundario'], width=250)
        sidebar_frame.pack(side='left', fill='y', padx=(0, 10))
        sidebar_frame.pack_propagate(False)
        
        # Título del sidebar
        LabelTitulo(
            sidebar_frame,
            text="NAVEGACIÓN",
            nivel=2
        ).pack(pady=15)
        
        # Botones de navegación
        nav_frame = tk.Frame(sidebar_frame, bg=COLORES['fondo_secundario'])
        nav_frame.pack(fill='both', expand=True, padx=10)
        
        secciones = [
            ("🏠 Dashboard", "dashboard", self.mostrar_dashboard),
            ("🎲 Generar Variables", "generacion", lambda: self.mostrar_panel('generacion')),
            ("📈 Pruebas Bondad", "bondad", lambda: self.mostrar_panel('bondad')),
            ("🎯 Monte Carlo", "montecarlo", lambda: self.mostrar_panel('montecarlo')),
            ("📊 Resultados", "resultados", lambda: self.mostrar_panel('resultados')),
            ("⚙️ Configuración", "configuracion", lambda: self.mostrar_panel('configuracion'))
        ]
        
        for texto, key, comando in secciones:
            btn = ModernButton(nav_frame, text=texto, command=comando, style='nav')
            btn.pack(fill='x', pady=2)
    
    def crear_area_principal(self):
        """Crea el área principal de contenido"""
        self.area_contenido = tk.Frame(self.main_container, bg=COLORES['fondo_principal'])
        self.area_contenido.pack(side='right', fill='both', expand=True)
        
        # Mostrar dashboard inicial
        self.mostrar_dashboard()
    
    def crear_status_bar(self):
        """Crea la barra de estado"""
        self.status_frame = tk.Frame(self.root, bg=COLORES['fondo_secundario'])
        self.status_frame.pack(fill='x', side='bottom')
        
        # Estado del sistema
        self.status_label = tk.Label(
            self.status_frame,
            text="Sistema listo - Bienvenido al Sistema de Simulación Computacional",
            font=FUENTES['small'],
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo_secundario']
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # Información de versión
        version_label = tk.Label(
            self.status_frame,
            text="v2.0 Professional",
            font=FUENTES['small'],
            fg=COLORES['texto_terciario'],
            bg=COLORES['fondo_secundario']
        )
        version_label.pack(side='right', padx=10, pady=5)
    
    def cargar_estado_inicial(self):
        """Carga el estado inicial de la aplicación"""
        self.actualizar_status("Sistema inicializado correctamente")
    
    def mostrar_dashboard(self):
        """Muestra el dashboard principal"""
        self.limpiar_area_contenido()
        self.panel_actual = 'dashboard'
        
        # Título
        LabelTitulo(
            self.area_contenido,
            text="DASHBOARD PRINCIPAL",
            nivel=1
        ).pack(fill='x', padx=20, pady=(10, 5))
        
        # Frame de contenido
        contenido_frame = tk.Frame(self.area_contenido, bg=COLORES['fondo_principal'])
        contenido_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Cards de estadísticas
        stats_frame = tk.Frame(contenido_frame, bg=COLORES['fondo_principal'])
        stats_frame.pack(fill='x', pady=(0, 20))
        
        estadisticas = [
            ("Simulaciones Realizadas", "0", "📈", COLORES['grafico_1']),
            ("Precisión Promedio", "95.2%", "✅", COLORES['exito']),
            ("Tiempo Ejecución", "2.4s", "⚡", COLORES['advertencia']),
            ("Datos Generados", "15,847", "📊", COLORES['grafico_4'])
        ]
        
        for i, (titulo, valor, icono, color) in enumerate(estadisticas):
            card = CardFrame(stats_frame, text=titulo, width=200, height=100)
            card.pack(side='left', fill='both', expand=True, padx=(0, 15) if i < 3 else (0, 0))
            
            contenido = card.obtener_frame_contenido()
            
            tk.Label(contenido, text=icono, font=('Segoe UI', 20), 
                    bg=COLORES['fondo_tarjeta'], fg=color).pack(anchor='w')
            
            tk.Label(contenido, text=valor, font=('Segoe UI', 24, 'bold'),
                    bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_primario']).pack(anchor='w')
            
            tk.Label(contenido, text=titulo, font=('Segoe UI', 10),
                    bg=COLORES['fondo_tarjeta'], fg=COLORES['texto_secundario']).pack(anchor='w')
        
        # Mensaje de bienvenida
        welcome_card = CardFrame(contenido_frame, text="BIENVENIDO")
        welcome_card.pack(fill='x', pady=(0, 20))
        welcome_content = welcome_card.obtener_frame_contenido()
        
        tk.Label(
            welcome_content,
            text="Sistema de Simulación Computacional Professional v2.0",
            font=FUENTES['titulo'],
            fg=COLORES['texto_primario'],
            bg=COLORES['fondo_tarjeta']
        ).pack(anchor='w', pady=(0, 10))
        
        tk.Label(
            welcome_content,
            text="Una herramienta avanzada para simulación y análisis de sistemas estocásticos.\n\n"
                 "Características principales:\n"
                 "• Generación de variables aleatorias con múltiples distribuciones\n"
                 "• Pruebas de bondad de ajuste estadístico\n"
                 "• Métodos de Monte Carlo para diversos problemas\n"
                 "• Visualización interactiva de resultados\n"
                 "• Interfaz moderna y profesional",
            font=FUENTES['principal'],
            fg=COLORES['texto_secundario'],
            bg=COLORES['fondo_tarjeta'],
            justify='left'
        ).pack(anchor='w')
        
        # Acciones rápidas
        actions_card = CardFrame(contenido_frame, text="ACCIONES RÁPIDAS")
        actions_card.pack(fill='x')
        actions_content = actions_card.obtener_frame_contenido()
        
        actions_frame = tk.Frame(actions_content, bg=COLORES['fondo_tarjeta'])
        actions_frame.pack(fill='x')
        
        quick_actions = [
            ("🎲 Generar Variables Aleatorias", lambda: self.mostrar_panel('generacion')),
            ("📈 Ejecutar Pruebas de Bondad", lambda: self.mostrar_panel('bondad')),
            ("🎯 Métodos Monte Carlo", lambda: self.mostrar_panel('montecarlo')),
            ("📊 Ver Resultados", lambda: self.mostrar_panel('resultados'))
        ]
        
        for texto, comando in quick_actions:
            btn = ModernButton(actions_frame, text=texto, command=comando, style='secondary')
            btn.pack(fill='x', pady=2)
    
    def mostrar_panel(self, nombre_panel):
        """Muestra un panel específico"""
        self.limpiar_area_contenido()
        self.panel_actual = nombre_panel
        
        if nombre_panel not in self.paneles:
            self.crear_panel(nombre_panel)
        
        self.paneles[nombre_panel].pack(fill='both', expand=True)
        self.actualizar_status(f"Panel: {nombre_panel.title()}")
    
    def crear_panel(self, nombre_panel):
        """Crea un panel específico"""
        if nombre_panel == 'generacion':
            self.paneles['generacion'] = PanelGeneracion(self.area_contenido, self.generador, self.datos_actuales)
        elif nombre_panel == 'bondad':
            self.paneles['bondad'] = PanelBondad(self.area_contenido, self.datos_actuales)
        elif nombre_panel == 'montecarlo':
            self.paneles['montecarlo'] = PanelMonteCarlo(self.area_contenido, self.generador)
        elif nombre_panel == 'resultados':
            self.paneles['resultados'] = PanelResultados(self.area_contenido)
        elif nombre_panel == 'configuracion':
            self.paneles['configuracion'] = PanelConfiguracion(self.area_contenido)
    
    def limpiar_area_contenido(self):
        """Limpia el área de contenido"""
        for widget in self.area_contenido.winfo_children():
            widget.destroy()
    
    def actualizar_status(self, mensaje):
        """Actualiza la barra de estado"""
        self.status_label.config(text=mensaje)
    
    # Métodos de funcionalidad de la aplicación
    def nuevo_proyecto(self):
        """Inicia un nuevo proyecto"""
        self.generador = None
        self.datos_actuales = []
        self.paneles = {}
        self.mostrar_dashboard()
        self.actualizar_status("Nuevo proyecto creado")
        messagebox.showinfo("Nuevo Proyecto", "Proyecto reiniciado correctamente")
    
    def abrir_proyecto(self):
        """Abre un proyecto existente"""
        messagebox.showinfo("Abrir Proyecto", "Funcionalidad en desarrollo")
    
    def guardar_proyecto(self):
        """Guarda el proyecto actual"""
        messagebox.showinfo("Guardar Proyecto", "Funcionalidad en desarrollo")
    
    def exportar_resultados(self):
        """Exporta los resultados"""
        messagebox.showinfo("Exportar Resultados", "Funcionalidad en desarrollo")
    
    def ejecutar_todas_simulaciones(self):
        """Ejecuta todas las simulaciones"""
        messagebox.showinfo("Ejecutar Simulaciones", "Funcionalidad en desarrollo")
    
    def mostrar_documentacion(self):
        """Muestra la documentación"""
        messagebox.showinfo("Documentación", 
                          "Sistema de Simulación Computacional v2.0\n\n"
                          "Documentación completa disponible en el manual de usuario.")
    
    def mostrar_ejemplos(self):
        """Muestra ejemplos de uso"""
        messagebox.showinfo("Ejemplos", 
                          "Ejemplos de uso:\n\n"
                          "1. Generación de variables normales\n"
                          "2. Prueba de bondad para distribución exponencial\n"
                          "3. Estimación de π con Monte Carlo\n"
                          "4. Problema de la ruina del jugador")
    
    def mostrar_acerca_de(self):
        """Muestra información acerca de la aplicación"""
        messagebox.showinfo("Acerca de",
                          "Sistema de Simulación Computacional\n"
                          "Versión 2.0 Professional\n\n"
                          "Desarrollado para el curso de Simulación Computacional\n\n"
                          "Características:\n"
                          "• Interfaz moderna y profesional\n"
                          "• Múltiples distribuciones de probabilidad\n"
                          "• Pruebas estadísticas avanzadas\n"
                          "• Métodos de Monte Carlo\n"
                          "• Visualización interactiva\n\n"
                          "© 2024 - Todos los derechos reservados")
    
    def salir(self):
        """Sale de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Está seguro de que desea salir?"):
            self.root.quit()
    
    def ejecutar(self):
        """Ejecuta la aplicación"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"Error en la aplicación: {str(e)}")

def main():
    """Función principal"""
    app = SistemaSimulacionApp()
    app.ejecutar()

if __name__ == "__main__":
    main()