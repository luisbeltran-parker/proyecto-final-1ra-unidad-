"""
Proyecto de Simulación Computacional
Sistema de Simulación con GUI - Archivo Principal
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from scipy import stats
import time

class GeneradorPseudoaleatorio:
    """Generador de números pseudoaleatorios usando el método LCG (Linear Congruential Generator)"""
    
    def __init__(self, semilla=None):
        if semilla is None:
            # Generar semilla automática usando el tiempo actual
            self.semilla = int(time.time() * 1000) % (2**31)
        else:
            self.semilla = semilla
        
        self.estado = self.semilla
        # Parámetros del generador (valores de Numerical Recipes)
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
    
    def siguiente(self):
        """Genera el siguiente número pseudoaleatorio entre 0 y 1"""
        self.estado = (self.a * self.estado + self.c) % self.m
        return self.estado / self.m
    
    def uniform(self, low=0.0, high=1.0, size=1):
        """Genera números uniformes en el rango [low, high]"""
        return [low + (high - low) * self.siguiente() for _ in range(size)]


class DistribucionDiscreta:
    """Clase para generar variables aleatorias de distribuciones discretas"""
    
    @staticmethod
    def binomial(n, p, size, generador):
        """Genera variables aleatorias con distribución Binomial"""
        resultados = []
        for _ in range(size):
            exitos = sum(1 for _ in range(n) if generador.siguiente() < p)
            resultados.append(exitos)
        return resultados
    
    @staticmethod
    def poisson(lam, size, generador):
        """Genera variables aleatorias con distribución Poisson usando el algoritmo de Knuth"""
        resultados = []
        L = np.exp(-lam)
        
        for _ in range(size):
            k = 0
            p = 1.0
            while p > L:
                k += 1
                p *= generador.siguiente()
            resultados.append(k - 1)
        
        return resultados


class DistribucionContinua:
    """Clase para generar variables aleatorias de distribuciones continuas"""
    
    @staticmethod
    def exponencial(lam, size, generador):
        """Genera variables aleatorias con distribución Exponencial"""
        resultados = []
        for _ in range(size):
            u = generador.siguiente()
            # Método de la transformada inversa
            x = -np.log(u) / lam
            resultados.append(x)
        return resultados
    
    @staticmethod
    def normal(mu, sigma, size, generador):
        """Genera variables aleatorias con distribución Normal usando Box-Muller"""
        resultados = []
        for _ in range(size // 2 + 1):
            u1 = generador.siguiente()
            u2 = generador.siguiente()
            
            # Transformación Box-Muller
            z0 = np.sqrt(-2 * np.log(u1)) * np.cos(2 * np.pi * u2)
            z1 = np.sqrt(-2 * np.log(u1)) * np.sin(2 * np.pi * u2)
            
            resultados.append(mu + sigma * z0)
            if len(resultados) < size:
                resultados.append(mu + sigma * z1)
        
        return resultados[:size]


class PruebasBondad:
    """Clase para realizar pruebas de bondad de ajuste"""
    
    @staticmethod
    def chi_cuadrado(datos, distribucion, params, bins=10):
        """Realiza la prueba de Chi-cuadrado"""
        # Crear histograma observado
        observado, bordes = np.histogram(datos, bins=bins)
        
        # Calcular frecuencias esperadas
        esperado = []
        n = len(datos)
        
        for i in range(len(bordes) - 1):
            prob = distribucion.cdf(bordes[i+1], *params) - distribucion.cdf(bordes[i], *params)
            esperado.append(n * prob)
        
        esperado = np.array(esperado)
        
        # Eliminar bins con frecuencia esperada muy baja
        mask = esperado >= 5
        observado = observado[mask]
        esperado = esperado[mask]
        
        # Calcular estadístico Chi-cuadrado
        chi2 = np.sum((observado - esperado)**2 / esperado)
        grados_libertad = len(observado) - len(params) - 1
        p_valor = 1 - stats.chi2.cdf(chi2, grados_libertad)
        
        return {
            'estadistico': chi2,
            'p_valor': p_valor,
            'grados_libertad': grados_libertad,
            'observado': observado,
            'esperado': esperado,
            'bordes': bordes[:-1][mask]
        }
    
    @staticmethod
    def kolmogorov_smirnov(datos, distribucion, params):
        """Realiza la prueba de Kolmogorov-Smirnov"""
        datos_ordenados = np.sort(datos)
        n = len(datos)
        
        # CDF empírica
        cdf_empirica = np.arange(1, n + 1) / n
        
        # CDF teórica
        cdf_teorica = distribucion.cdf(datos_ordenados, *params)
        
        # Calcular estadístico D
        D = np.max(np.abs(cdf_empirica - cdf_teorica))
        
        # Calcular p-valor
        p_valor = stats.kstest(datos, lambda x: distribucion.cdf(x, *params))[1]
        
        return {
            'estadistico': D,
            'p_valor': p_valor,
            'cdf_empirica': cdf_empirica,
            'cdf_teorica': cdf_teorica,
            'datos_ordenados': datos_ordenados
        }


class MonteCarlo:
    """Clase para implementar simulaciones de Monte Carlo"""
    
    @staticmethod
    def estimar_pi(n_puntos, generador):
        """Estima el valor de π usando el método de Monte Carlo"""
        dentro_circulo = 0
        puntos_x = []
        puntos_y = []
        colores = []
        
        for _ in range(n_puntos):
            x = generador.siguiente() * 2 - 1  # Rango [-1, 1]
            y = generador.siguiente() * 2 - 1
            
            puntos_x.append(x)
            puntos_y.append(y)
            
            if x**2 + y**2 <= 1:
                dentro_circulo += 1
                colores.append('blue')
            else:
                colores.append('red')
        
        pi_estimado = 4 * dentro_circulo / n_puntos
        
        return {
            'pi_estimado': pi_estimado,
            'dentro_circulo': dentro_circulo,
            'total_puntos': n_puntos,
            'puntos_x': puntos_x,
            'puntos_y': puntos_y,
            'colores': colores
        }
    
    @staticmethod
    def ruina_jugador(capital_inicial, objetivo, prob_ganar, n_simulaciones, generador):
        """Simula el problema de la ruina del jugador"""
        ruinas = 0
        exitos = 0
        duraciones = []
        
        for _ in range(n_simulaciones):
            capital = capital_inicial
            pasos = 0
            
            while capital > 0 and capital < objetivo:
                if generador.siguiente() < prob_ganar:
                    capital += 1
                else:
                    capital -= 1
                pasos += 1
            
            duraciones.append(pasos)
            
            if capital == 0:
                ruinas += 1
            else:
                exitos += 1
        
        return {
            'prob_ruina': ruinas / n_simulaciones,
            'prob_exito': exitos / n_simulaciones,
            'duracion_promedio': np.mean(duraciones),
            'duraciones': duraciones
        }


class AplicacionSimulacion:
    """Clase principal de la aplicación con interfaz gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Simulación Computacional")
        self.root.geometry("1200x800")
        
        # Variables
        self.generador = None
        self.datos_generados = []
        
        # Crear interfaz
        self.crear_menu()
        self.crear_notebook()
    
    def crear_menu(self):
        """Crea el menú principal"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        archivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=archivo_menu)
        archivo_menu.add_command(label="Exportar datos", command=self.exportar_datos)
        archivo_menu.add_command(label="Importar datos", command=self.importar_datos)
        archivo_menu.add_separator()
        archivo_menu.add_command(label="Salir", command=self.root.quit)
        
        ayuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=ayuda_menu)
        ayuda_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)
    
    def crear_notebook(self):
        """Crea el notebook con pestañas"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Pestaña 1: Generación de variables aleatorias
        self.tab_generacion = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_generacion, text="Generación de Variables")
        self.crear_tab_generacion()
        
        # Pestaña 2: Pruebas de bondad de ajuste
        self.tab_bondad = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_bondad, text="Pruebas de Bondad")
        self.crear_tab_bondad()
        
        # Pestaña 3: Método de Monte Carlo
        self.tab_monte_carlo = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_monte_carlo, text="Monte Carlo")
        self.crear_tab_monte_carlo()
    
    def crear_tab_generacion(self):
        """Crea la interfaz para generación de variables aleatorias"""
        # Frame superior para configuración
        frame_config = ttk.LabelFrame(self.tab_generacion, text="Configuración", padding=10)
        frame_config.pack(fill='x', padx=10, pady=10)
        
        # Tipo de semilla
        ttk.Label(frame_config, text="Tipo de Semilla:").grid(row=0, column=0, sticky='w', pady=5)
        self.tipo_semilla = tk.StringVar(value="auto")
        ttk.Radiobutton(frame_config, text="Automática", variable=self.tipo_semilla, 
                       value="auto", command=self.toggle_semilla).grid(row=0, column=1, sticky='w')
        ttk.Radiobutton(frame_config, text="Manual", variable=self.tipo_semilla, 
                       value="manual", command=self.toggle_semilla).grid(row=0, column=2, sticky='w')
        
        ttk.Label(frame_config, text="Semilla:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_semilla = ttk.Entry(frame_config, width=20, state='disabled')
        self.entry_semilla.grid(row=1, column=1, columnspan=2, sticky='w')
        
        # Tipo de distribución
        ttk.Label(frame_config, text="Tipo de Distribución:").grid(row=2, column=0, sticky='w', pady=5)
        self.tipo_dist = tk.StringVar(value="binomial")
        ttk.Radiobutton(frame_config, text="Binomial (Discreta)", variable=self.tipo_dist, 
                       value="binomial", command=self.actualizar_parametros).grid(row=2, column=1, sticky='w')
        ttk.Radiobutton(frame_config, text="Exponencial (Continua)", variable=self.tipo_dist, 
                       value="exponencial", command=self.actualizar_parametros).grid(row=2, column=2, sticky='w')
        
        # Frame para parámetros dinámicos
        self.frame_parametros = ttk.Frame(frame_config)
        self.frame_parametros.grid(row=3, column=0, columnspan=3, sticky='ew', pady=10)
        
        # Número de muestras
        ttk.Label(frame_config, text="Número de muestras:").grid(row=4, column=0, sticky='w', pady=5)
        self.entry_n_muestras = ttk.Entry(frame_config, width=20)
        self.entry_n_muestras.insert(0, "1000")
        self.entry_n_muestras.grid(row=4, column=1, columnspan=2, sticky='w')
        
        # Botón generar
        ttk.Button(frame_config, text="Generar Variables", 
                  command=self.generar_variables).grid(row=5, column=0, columnspan=3, pady=10)
        
        # Frame para resultados
        frame_resultados = ttk.LabelFrame(self.tab_generacion, text="Resultados", padding=10)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Texto para mostrar estadísticas
        self.text_estadisticas = tk.Text(frame_resultados, height=8, width=60)
        self.text_estadisticas.pack(side='left', fill='both', expand=True)
        
        scroll = ttk.Scrollbar(frame_resultados, command=self.text_estadisticas.yview)
        scroll.pack(side='left', fill='y')
        self.text_estadisticas.config(yscrollcommand=scroll.set)
        
        # Canvas para gráfico
        self.fig_generacion, self.ax_generacion = plt.subplots(figsize=(6, 4))
        self.canvas_generacion = FigureCanvasTkAgg(self.fig_generacion, frame_resultados)
        self.canvas_generacion.get_tk_widget().pack(side='right', fill='both', expand=True)
        
        # Inicializar parámetros
        self.actualizar_parametros()
    
    def crear_tab_bondad(self):
        """Crea la interfaz para pruebas de bondad de ajuste"""
        # Frame superior para configuración
        frame_config = ttk.LabelFrame(self.tab_bondad, text="Configuración", padding=10)
        frame_config.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_config, text="Distribución a probar:").grid(row=0, column=0, sticky='w', pady=5)
        self.dist_bondad = tk.StringVar(value="exponencial")
        ttk.Combobox(frame_config, textvariable=self.dist_bondad, 
                    values=["exponencial", "normal"], state='readonly', width=18).grid(row=0, column=1, sticky='w')
        
        ttk.Label(frame_config, text="Prueba:").grid(row=1, column=0, sticky='w', pady=5)
        self.tipo_prueba = tk.StringVar(value="ks")
        ttk.Radiobutton(frame_config, text="Kolmogorov-Smirnov", 
                       variable=self.tipo_prueba, value="ks").grid(row=1, column=1, sticky='w')
        ttk.Radiobutton(frame_config, text="Chi-cuadrado", 
                       variable=self.tipo_prueba, value="chi2").grid(row=1, column=2, sticky='w')
        
        ttk.Button(frame_config, text="Realizar Prueba", 
                  command=self.realizar_prueba_bondad).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Frame para resultados
        frame_resultados = ttk.LabelFrame(self.tab_bondad, text="Resultados", padding=10)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_bondad = tk.Text(frame_resultados, height=10, width=60)
        self.text_bondad.pack(side='left', fill='both', expand=True)
        
        scroll = ttk.Scrollbar(frame_resultados, command=self.text_bondad.yview)
        scroll.pack(side='left', fill='y')
        self.text_bondad.config(yscrollcommand=scroll.set)
        
        # Canvas para gráfico
        self.fig_bondad, self.ax_bondad = plt.subplots(figsize=(6, 4))
        self.canvas_bondad = FigureCanvasTkAgg(self.fig_bondad, frame_resultados)
        self.canvas_bondad.get_tk_widget().pack(side='right', fill='both', expand=True)
    
    def crear_tab_monte_carlo(self):
        """Crea la interfaz para método de Monte Carlo"""
        # Frame superior para selección de problema
        frame_config = ttk.LabelFrame(self.tab_monte_carlo, text="Configuración", padding=10)
        frame_config.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_config, text="Problema:").grid(row=0, column=0, sticky='w', pady=5)
        self.problema_mc = tk.StringVar(value="pi")
        ttk.Radiobutton(frame_config, text="Estimación de π", 
                       variable=self.problema_mc, value="pi", 
                       command=self.actualizar_parametros_mc).grid(row=0, column=1, sticky='w')
        ttk.Radiobutton(frame_config, text="Ruina del Jugador", 
                       variable=self.problema_mc, value="ruina", 
                       command=self.actualizar_parametros_mc).grid(row=0, column=2, sticky='w')
        
        # Frame para parámetros dinámicos
        self.frame_parametros_mc = ttk.Frame(frame_config)
        self.frame_parametros_mc.grid(row=1, column=0, columnspan=3, sticky='ew', pady=10)
        
        ttk.Button(frame_config, text="Ejecutar Simulación", 
                  command=self.ejecutar_monte_carlo).grid(row=2, column=0, columnspan=3, pady=10)
        
        # Frame para resultados
        frame_resultados = ttk.LabelFrame(self.tab_monte_carlo, text="Resultados", padding=10)
        frame_resultados.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_monte_carlo = tk.Text(frame_resultados, height=10, width=60)
        self.text_monte_carlo.pack(side='left', fill='both', expand=True)
        
        scroll = ttk.Scrollbar(frame_resultados, command=self.text_monte_carlo.yview)
        scroll.pack(side='left', fill='y')
        self.text_monte_carlo.config(yscrollcommand=scroll.set)
        
        # Canvas para gráfico
        self.fig_mc, self.ax_mc = plt.subplots(figsize=(6, 4))
        self.canvas_mc = FigureCanvasTkAgg(self.fig_mc, frame_resultados)
        self.canvas_mc.get_tk_widget().pack(side='right', fill='both', expand=True)
        
        # Inicializar parámetros
        self.actualizar_parametros_mc()
    
    def toggle_semilla(self):
        """Habilita/deshabilita el campo de semilla"""
        if self.tipo_semilla.get() == "manual":
            self.entry_semilla.config(state='normal')
        else:
            self.entry_semilla.config(state='disabled')
    
    def actualizar_parametros(self):
        """Actualiza los campos de parámetros según la distribución seleccionada"""
        # Limpiar frame
        for widget in self.frame_parametros.winfo_children():
            widget.destroy()
        
        if self.tipo_dist.get() == "binomial":
            ttk.Label(self.frame_parametros, text="n (número de ensayos):").grid(row=0, column=0, sticky='w')
            self.param1 = ttk.Entry(self.frame_parametros, width=15)
            self.param1.insert(0, "10")
            self.param1.grid(row=0, column=1, sticky='w', padx=5)
            
            ttk.Label(self.frame_parametros, text="p (probabilidad de éxito):").grid(row=1, column=0, sticky='w')
            self.param2 = ttk.Entry(self.frame_parametros, width=15)
            self.param2.insert(0, "0.5")
            self.param2.grid(row=1, column=1, sticky='w', padx=5)
        
        elif self.tipo_dist.get() == "exponencial":
            ttk.Label(self.frame_parametros, text="λ (tasa):").grid(row=0, column=0, sticky='w')
            self.param1 = ttk.Entry(self.frame_parametros, width=15)
            self.param1.insert(0, "1.0")
            self.param1.grid(row=0, column=1, sticky='w', padx=5)
    
    def actualizar_parametros_mc(self):
        """Actualiza los campos de parámetros para Monte Carlo"""
        # Limpiar frame
        for widget in self.frame_parametros_mc.winfo_children():
            widget.destroy()
        
        if self.problema_mc.get() == "pi":
            ttk.Label(self.frame_parametros_mc, text="Número de puntos:").grid(row=0, column=0, sticky='w')
            self.mc_param1 = ttk.Entry(self.frame_parametros_mc, width=15)
            self.mc_param1.insert(0, "10000")
            self.mc_param1.grid(row=0, column=1, sticky='w', padx=5)
        
        elif self.problema_mc.get() == "ruina":
            ttk.Label(self.frame_parametros_mc, text="Capital inicial:").grid(row=0, column=0, sticky='w')
            self.mc_param1 = ttk.Entry(self.frame_parametros_mc, width=15)
            self.mc_param1.insert(0, "50")
            self.mc_param1.grid(row=0, column=1, sticky='w', padx=5)
            
            ttk.Label(self.frame_parametros_mc, text="Objetivo:").grid(row=1, column=0, sticky='w')
            self.mc_param2 = ttk.Entry(self.frame_parametros_mc, width=15)
            self.mc_param2.insert(0, "100")
            self.mc_param2.grid(row=1, column=1, sticky='w', padx=5)
            
            ttk.Label(self.frame_parametros_mc, text="Prob. ganar:").grid(row=2, column=0, sticky='w')
            self.mc_param3 = ttk.Entry(self.frame_parametros_mc, width=15)
            self.mc_param3.insert(0, "0.48")
            self.mc_param3.grid(row=2, column=1, sticky='w', padx=5)
            
            ttk.Label(self.frame_parametros_mc, text="N° simulaciones:").grid(row=3, column=0, sticky='w')
            self.mc_param4 = ttk.Entry(self.frame_parametros_mc, width=15)
            self.mc_param4.insert(0, "1000")
            self.mc_param4.grid(row=3, column=1, sticky='w', padx=5)
    
    def generar_variables(self):
        """Genera variables aleatorias según la configuración"""
        try:
            # Validar entradas
            n_muestras = int(self.entry_n_muestras.get())
            if n_muestras <= 0:
                raise ValueError("El número de muestras debe ser positivo")
            
            # Crear generador
            if self.tipo_semilla.get() == "manual":
                semilla = int(self.entry_semilla.get())
                self.generador = GeneradorPseudoaleatorio(semilla)
            else:
                self.generador = GeneradorPseudoaleatorio()
            
            # Generar datos
            if self.tipo_dist.get() == "binomial":
                n = int(self.param1.get())
                p = float(self.param2.get())
                if not (0 <= p <= 1):
                    raise ValueError("La probabilidad debe estar entre 0 y 1")
                
                self.datos_generados = DistribucionDiscreta.binomial(n, p, n_muestras, self.generador)
                titulo = f"Distribución Binomial (n={n}, p={p})"
            
            elif self.tipo_dist.get() == "exponencial":
                lam = float(self.param1.get())
                if lam <= 0:
                    raise ValueError("Lambda debe ser positivo")
                
                self.datos_generados = DistribucionContinua.exponencial(lam, n_muestras, self.generador)
                titulo = f"Distribución Exponencial (λ={lam})"
            
            # Calcular estadísticas
            media = np.mean(self.datos_generados)
            desv = np.std(self.datos_generados)
            minimo = np.min(self.datos_generados)
            maximo = np.max(self.datos_generados)
            
            # Mostrar estadísticas
            self.text_estadisticas.delete(1.0, tk.END)
            self.text_estadisticas.insert(tk.END, f"Estadísticas de los datos generados:\n")
            self.text_estadisticas.insert(tk.END, f"{'='*50}\n")
            self.text_estadisticas.insert(tk.END, f"Semilla utilizada: {self.generador.semilla}\n")
            self.text_estadisticas.insert(tk.END, f"Número de muestras: {n_muestras}\n")
            self.text_estadisticas.insert(tk.END, f"Media: {media:.4f}\n")
            self.text_estadisticas.insert(tk.END, f"Desviación estándar: {desv:.4f}\n")
            self.text_estadisticas.insert(tk.END, f"Mínimo: {minimo:.4f}\n")
            self.text_estadisticas.insert(tk.END, f"Máximo: {maximo:.4f}\n")
            
            # Graficar histograma
            self.ax_generacion.clear()
            self.ax_generacion.hist(self.datos_generados, bins=30, density=True, alpha=0.7, edgecolor='black')
            self.ax_generacion.set_xlabel('Valor')
            self.ax_generacion.set_ylabel('Frecuencia')
            self.ax_generacion.set_title(titulo)
            self.ax_generacion.grid(True, alpha=0.3)
            self.fig_generacion.tight_layout()
            self.canvas_generacion.draw()
            
            messagebox.showinfo("Éxito", f"Se generaron {n_muestras} variables aleatorias")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def realizar_prueba_bondad(self):
        """Realiza prueba de bondad de ajuste sobre los datos"""
        try:
            if len(self.datos_generados) == 0:
                messagebox.showwarning("Advertencia", "Primero debe generar datos")
                return
            
            datos = np.array(self.datos_generados)
            dist_nombre = self.dist_bondad.get()
            
            # Estimar parámetros
            if dist_nombre == "exponencial":
                lam = 1 / np.mean(datos)
                params = (0, 1/lam)  # loc=0, scale=1/lambda
                distribucion = stats.expon
                titulo_dist = f"Exponencial (λ={lam:.4f})"
            
            elif dist_nombre == "normal":
                mu = np.mean(datos)
                sigma = np.std(datos)
                params = (mu, sigma)
                distribucion = stats.norm
                titulo_dist = f"Normal (μ={mu:.4f}, σ={sigma:.4f})"
            
            # Realizar prueba
            if self.tipo_prueba.get() == "ks":
                resultado = PruebasBondad.kolmogorov_smirnov(datos, distribucion, params)
                
                # Mostrar resultados
                self.text_bondad.delete(1.0, tk.END)
                self.text_bondad.insert(tk.END, f"Prueba de Kolmogorov-Smirnov\n")
                self.text_bondad.insert(tk.END, f"{'='*50}\n")
                self.text_bondad.insert(tk.END, f"Distribución: {titulo_dist}\n")
                self.text_bondad.insert(tk.END, f"Estadístico D: {resultado['estadistico']:.6f}\n")
                self.text_bondad.insert(tk.END, f"P-valor: {resultado['p_valor']:.6f}\n")
                self.text_bondad.insert(tk.END, f"\nInterpretación (α=0.05):\n")
                if resultado['p_valor'] > 0.05:
                    self.text_bondad.insert(tk.END, "No se rechaza H0. Los datos siguen\nla distribución especificada.\n")
                else:
                    self.text_bondad.insert(tk.END, "Se rechaza H0. Los datos NO siguen\nla distribución especificada.\n")
                
                # Graficar
                self.ax_bondad.clear()
                self.ax_bondad.plot(resultado['datos_ordenados'], resultado['cdf_empirica'], 
                                   label='CDF Empírica', linewidth=2)
                self.ax_bondad.plot(resultado['datos_ordenados'], resultado['cdf_teorica'], 
                                   label='CDF Teórica', linewidth=2, linestyle='--')
                self.ax_bondad.set_xlabel('Valor')
                self.ax_bondad.set_ylabel('Probabilidad Acumulada')
                self.ax_bondad.set_title(f'Prueba K-S: {titulo_dist}')
                self.ax_bondad.legend()
                self.ax_bondad.grid(True, alpha=0.3)
                
            elif self.tipo_prueba.get() == "chi2":
                resultado = PruebasBondad.chi_cuadrado(datos, distribucion, params)
                
                # Mostrar resultados
                self.text_bondad.delete(1.0, tk.END)
                self.text_bondad.insert(tk.END, f"Prueba de Chi-cuadrado\n")
                self.text_bondad.insert(tk.END, f"{'='*50}\n")
                self.text_bondad.insert(tk.END, f"Distribución: {titulo_dist}\n")
                self.text_bondad.insert(tk.END, f"Estadístico χ²: {resultado['estadistico']:.6f}\n")
                self.text_bondad.insert(tk.END, f"Grados de libertad: {resultado['grados_libertad']}\n")
                self.text_bondad.insert(tk.END, f"P-valor: {resultado['p_valor']:.6f}\n")
                self.text_bondad.insert(tk.END, f"\nInterpretación (α=0.05):\n")
                if resultado['p_valor'] > 0.05:
                    self.text_bondad.insert(tk.END, "No se rechaza H0. Los datos siguen\nla distribución especificada.\n")
                else:
                    self.text_bondad.insert(tk.END, "Se rechaza H0. Los datos NO siguen\nla distribución especificada.\n")
                
                # Graficar
                self.ax_bondad.clear()
                x = np.arange(len(resultado['observado']))
                width = 0.35
                self.ax_bondad.bar(x - width/2, resultado['observado'], width, 
                                  label='Frecuencia Observada', alpha=0.8)
                self.ax_bondad.bar(x + width/2, resultado['esperado'], width, 
                                  label='Frecuencia Esperada', alpha=0.8)
                self.ax_bondad.set_xlabel('Intervalo')
                self.ax_bondad.set_ylabel('Frecuencia')
                self.ax_bondad.set_title(f'Prueba Chi-cuadrado: {titulo_dist}')
                self.ax_bondad.legend()
                self.ax_bondad.grid(True, alpha=0.3)
            
            self.fig_bondad.tight_layout()
            self.canvas_bondad.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al realizar la prueba: {str(e)}")
    
    def ejecutar_monte_carlo(self):
        """Ejecuta simulación de Monte Carlo"""
        try:
            # Crear generador si no existe
            if self.generador is None:
                self.generador = GeneradorPseudoaleatorio()
            
            if self.problema_mc.get() == "pi":
                n_puntos = int(self.mc_param1.get())
                if n_puntos <= 0:
                    raise ValueError("El número de puntos debe ser positivo")
                
                resultado = MonteCarlo.estimar_pi(n_puntos, self.generador)
                
                # Mostrar resultados
                self.text_monte_carlo.delete(1.0, tk.END)
                self.text_monte_carlo.insert(tk.END, f"Estimación de π mediante Monte Carlo\n")
                self.text_monte_carlo.insert(tk.END, f"{'='*50}\n")
                self.text_monte_carlo.insert(tk.END, f"Número de puntos: {resultado['total_puntos']}\n")
                self.text_monte_carlo.insert(tk.END, f"Puntos dentro del círculo: {resultado['dentro_circulo']}\n")
                self.text_monte_carlo.insert(tk.END, f"Puntos fuera del círculo: {resultado['total_puntos'] - resultado['dentro_circulo']}\n")
                self.text_monte_carlo.insert(tk.END, f"\nπ estimado: {resultado['pi_estimado']:.6f}\n")
                self.text_monte_carlo.insert(tk.END, f"π real: {np.pi:.6f}\n")
                self.text_monte_carlo.insert(tk.END, f"Error absoluto: {abs(resultado['pi_estimado'] - np.pi):.6f}\n")
                self.text_monte_carlo.insert(tk.END, f"Error relativo: {abs(resultado['pi_estimado'] - np.pi)/np.pi * 100:.4f}%\n")
                
                # Graficar (muestreo para mejor visualización si hay muchos puntos)
                self.ax_mc.clear()
                max_puntos_grafico = min(2000, n_puntos)
                indices = np.random.choice(n_puntos, max_puntos_grafico, replace=False)
                
                puntos_x = [resultado['puntos_x'][i] for i in indices]
                puntos_y = [resultado['puntos_y'][i] for i in indices]
                colores = [resultado['colores'][i] for i in indices]
                
                self.ax_mc.scatter(puntos_x, puntos_y, c=colores, alpha=0.5, s=1)
                circulo = plt.Circle((0, 0), 1, fill=False, color='black', linewidth=2)
                self.ax_mc.add_patch(circulo)
                self.ax_mc.set_xlim(-1.1, 1.1)
                self.ax_mc.set_ylim(-1.1, 1.1)
                self.ax_mc.set_aspect('equal')
                self.ax_mc.set_title(f'Estimación de π: {resultado["pi_estimado"]:.6f}')
                self.ax_mc.grid(True, alpha=0.3)
                
            elif self.problema_mc.get() == "ruina":
                capital_inicial = int(self.mc_param1.get())
                objetivo = int(self.mc_param2.get())
                prob_ganar = float(self.mc_param3.get())
                n_sim = int(self.mc_param4.get())
                
                if capital_inicial <= 0 or objetivo <= capital_inicial:
                    raise ValueError("Valores de capital inválidos")
                if not (0 <= prob_ganar <= 1):
                    raise ValueError("La probabilidad debe estar entre 0 y 1")
                if n_sim <= 0:
                    raise ValueError("El número de simulaciones debe ser positivo")
                
                resultado = MonteCarlo.ruina_jugador(capital_inicial, objetivo, prob_ganar, n_sim, self.generador)
                
                # Mostrar resultados
                self.text_monte_carlo.delete(1.0, tk.END)
                self.text_monte_carlo.insert(tk.END, f"Problema de la Ruina del Jugador\n")
                self.text_monte_carlo.insert(tk.END, f"{'='*50}\n")
                self.text_monte_carlo.insert(tk.END, f"Capital inicial: ${capital_inicial}\n")
                self.text_monte_carlo.insert(tk.END, f"Objetivo: ${objetivo}\n")
                self.text_monte_carlo.insert(tk.END, f"Probabilidad de ganar: {prob_ganar}\n")
                self.text_monte_carlo.insert(tk.END, f"Número de simulaciones: {n_sim}\n\n")
                self.text_monte_carlo.insert(tk.END, f"RESULTADOS:\n")
                self.text_monte_carlo.insert(tk.END, f"Probabilidad de ruina: {resultado['prob_ruina']:.4f}\n")
                self.text_monte_carlo.insert(tk.END, f"Probabilidad de éxito: {resultado['prob_exito']:.4f}\n")
                self.text_monte_carlo.insert(tk.END, f"Duración promedio: {resultado['duracion_promedio']:.2f} rondas\n")
                
                # Graficar histograma de duraciones
                self.ax_mc.clear()
                self.ax_mc.hist(resultado['duraciones'], bins=50, edgecolor='black', alpha=0.7)
                self.ax_mc.axvline(resultado['duracion_promedio'], color='red', 
                                  linestyle='--', linewidth=2, label=f'Promedio: {resultado["duracion_promedio"]:.2f}')
                self.ax_mc.set_xlabel('Duración (rondas)')
                self.ax_mc.set_ylabel('Frecuencia')
                self.ax_mc.set_title('Distribución de Duraciones del Juego')
                self.ax_mc.legend()
                self.ax_mc.grid(True, alpha=0.3)
            
            self.fig_mc.tight_layout()
            self.canvas_mc.draw()
            
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def exportar_datos(self):
        """Exporta los datos generados a un archivo de texto"""
        if len(self.datos_generados) == 0:
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
        
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if filename:
                with open(filename, 'w') as f:
                    f.write(f"Datos generados - Simulación Computacional\n")
                    f.write(f"{'='*50}\n")
                    f.write(f"Semilla: {self.generador.semilla if self.generador else 'N/A'}\n")
                    f.write(f"Número de muestras: {len(self.datos_generados)}\n")
                    f.write(f"Media: {np.mean(self.datos_generados):.6f}\n")
                    f.write(f"Desviación estándar: {np.std(self.datos_generados):.6f}\n")
                    f.write(f"\nDatos:\n")
                    for i, dato in enumerate(self.datos_generados, 1):
                        f.write(f"{dato:.6f}\n")
                
                messagebox.showinfo("Éxito", f"Datos exportados a {filename}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar: {str(e)}")
    
    def importar_datos(self):
        """Importa datos desde un archivo de texto"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
            
            if filename:
                with open(filename, 'r') as f:
                    datos = []
                    for linea in f:
                        linea = linea.strip()
                        if linea and not linea.startswith('#') and not linea.startswith('='):
                            try:
                                valor = float(linea)
                                datos.append(valor)
                            except ValueError:
                                continue
                
                if len(datos) > 0:
                    self.datos_generados = datos
                    messagebox.showinfo("Éxito", f"Se importaron {len(datos)} datos")
                    
                    # Actualizar visualización
                    self.text_estadisticas.delete(1.0, tk.END)
                    self.text_estadisticas.insert(tk.END, f"Datos importados desde archivo\n")
                    self.text_estadisticas.insert(tk.END, f"{'='*50}\n")
                    self.text_estadisticas.insert(tk.END, f"Número de muestras: {len(datos)}\n")
                    self.text_estadisticas.insert(tk.END, f"Media: {np.mean(datos):.4f}\n")
                    self.text_estadisticas.insert(tk.END, f"Desviación estándar: {np.std(datos):.4f}\n")
                    self.text_estadisticas.insert(tk.END, f"Mínimo: {np.min(datos):.4f}\n")
                    self.text_estadisticas.insert(tk.END, f"Máximo: {np.max(datos):.4f}\n")
                    
                    self.ax_generacion.clear()
                    self.ax_generacion.hist(datos, bins=30, density=True, alpha=0.7, edgecolor='black')
                    self.ax_generacion.set_xlabel('Valor')
                    self.ax_generacion.set_ylabel('Frecuencia')
                    self.ax_generacion.set_title('Datos Importados')
                    self.ax_generacion.grid(True, alpha=0.3)
                    self.fig_generacion.tight_layout()
                    self.canvas_generacion.draw()
                else:
                    messagebox.showwarning("Advertencia", "No se encontraron datos válidos en el archivo")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al importar: {str(e)}")
    
    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de",
            "Sistema de Simulación Computacional\n\n"
            "Versión 1.0\n"
            "Desarrollado para el curso de Simulación Computacional\n\n"
            "Características:\n"
            "- Generación de variables aleatorias\n"
            "- Pruebas de bondad de ajuste\n"
            "- Métodos de Monte Carlo\n\n"
            "Octubre 2024"
        )


def main():
    """Función principal"""
    root = tk.Tk()
    app = AplicacionSimulacion(root)
    root.mainloop()


if __name__ == "__main__":
    main()