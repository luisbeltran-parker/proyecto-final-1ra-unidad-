"""
Configuración y constantes para la aplicación de simulación
Autor: [Tu Nombre]
Fecha: Octubre 2024
"""

# =============================================================================
# PALETA DE COLORES - TEMA OSCURO PROFESIONAL
# =============================================================================

COLORES = {
    # Colores primarios
    'fondo_principal': '#0a1929',
    'fondo_secundario': '#1e3a5c',
    'fondo_terciario': '#2d4a76',
    'fondo_tarjeta': 'rgba(255, 255, 255, 0.05)',
    
    # Colores de acento
    'acento_primario': '#00a8ff',
    'acento_secundario': '#0097e6',
    'acento_terciario': '#87ceeb',
    
    # Colores de texto
    'texto_primario': '#ffffff',
    'texto_secundario': '#b0bec5',
    'texto_terciario': '#78909c',
    
    # Colores de estado
    'exito': '#4caf50',
    'advertencia': '#ff9800',
    'error': '#f44336',
    'info': '#2196f3',
    
    # Colores de gráficos
    'grafico_1': '#00a8ff',
    'grafico_2': '#4caf50',
    'grafico_3': '#ff9800',
    'grafico_4': '#9c27b0',
    'grafico_5': '#f44336',
    'grafico_6': '#00bcd4'
}

# =============================================================================
# CONFIGURACIÓN DE FUENTES
# =============================================================================

FUENTES = {
    'principal': ('Segoe UI', 10),
    'titulo': ('Segoe UI', 14, 'bold'),
    'subtitulo': ('Segoe UI', 11, 'bold'),
    'encabezado': ('Segoe UI', 12, 'bold'),
    'monospace': ('Consolas', 10),
    'small': ('Segoe UI', 9)
}

# =============================================================================
# CONFIGURACIÓN DE LA INTERFAZ
# =============================================================================

INTERFAZ = {
    'ancho_ventana': 1400,
    'alto_ventana': 900,
    'border_radius': 12,
    'padding_x': 15,
    'padding_y': 10,
    'shadow_offset': 2,
    'transition_speed': 300
}

# =============================================================================
# CONFIGURACIÓN DE GRÁFICOS
# =============================================================================

GRAFICOS = {
    'tema_oscuro': True,
    'color_fondo': '#0a1929',
    'color_grid': 'rgba(255, 255, 255, 0.1)',
    'color_texto': '#ffffff',
    'color_lineas': '#00a8ff',
    'ancho_linea': 2.5,
    'alpha_fill': 0.3,
    'dpi': 100
}

# =============================================================================
# CONFIGURACIÓN DE SIMULACIÓN
# =============================================================================

SIMULACION = {
    'max_muestras': 100000,
    'default_muestras': 1000,
    'max_bins': 50,
    'default_bins': 30,
    'precision': 6,
    'alpha_pruebas': 0.05
}

# =============================================================================
# PARÁMETROS POR DEFECTO
# =============================================================================

PARAMETROS_DEFAULT = {
    'binomial': {'n': 10, 'p': 0.5},
    'poisson': {'lam': 5},
    'exponencial': {'lam': 1.0},
    'normal': {'mu': 0, 'sigma': 1},
    'uniforme': {'low': 0, 'high': 1},
    'monte_carlo_pi': {'n_puntos': 10000},
    'ruina_jugador': {
        'capital_inicial': 50,
        'objetivo': 100,
        'prob_ganar': 0.48,
        'n_simulaciones': 1000
    }
}

# =============================================================================
# TEXTO Y MENSAJES
# =============================================================================

MENSAJES = {
    'exito_generacion': '✅ Variables generadas exitosamente',
    'exito_exportacion': '✅ Datos exportados correctamente',
    'exito_importacion': '✅ Datos importados correctamente',
    'error_validacion': '❌ Error en los datos de entrada',
    'error_archivo': '❌ Error al procesar el archivo',
    'advertencia_datos': '⚠️ No hay datos disponibles',
    'info_simulacion': '🔧 Ejecutando simulación...'
}

# =============================================================================
# ESTILOS TTK PERSONALIZADOS
# =============================================================================

STYLES = {
    'TFrame': {
        'background': COLORES['fondo_principal']
    },
    'TLabel': {
        'background': COLORES['fondo_principal'],
        'foreground': COLORES['texto_primario'],
        'font': FUENTES['principal']
    },
    'TButton': {
        'background': COLORES['acento_primario'],
        'foreground': COLORES['texto_primario'],
        'font': FUENTES['principal'],
        'borderwidth': 0,
        'focuscolor': 'none'
    },
    'TEntry': {
        'fieldbackground': COLORES['fondo_secundario'],
        'foreground': COLORES['texto_primario'],
        'insertcolor': COLORES['texto_primario'],
        'borderwidth': 1,
        'relief': 'flat'
    },
    'TCombobox': {
        'fieldbackground': COLORES['fondo_secundario'],
        'foreground': COLORES['texto_primario'],
        'background': COLORES['fondo_secundario'],
        'arrowcolor': COLORES['texto_primario']
    },
    'TNotebook': {
        'background': COLORES['fondo_principal'],
        'tabmargins': [2, 5, 2, 0],
        'borderwidth': 0
    },
    'TNotebook.Tab': {
        'background': COLORES['fondo_secundario'],
        'foreground': COLORES['texto_secundario'],
        'padding': [15, 5],
        'borderwidth': 0
    }
}