import streamlit as st
import pandas as pd
import numpy as np

# --- Título y Encabezado ---
st.title("🚀 Showcase Básico de Streamlit")
st.header("Una Aplicación Simple sin Dependencias Externas")

# --- Contenido Estático ---
st.write(
    """
    Esta es una aplicación de demostración construida únicamente con
    **Streamlit** y sus librerías integradas (`pandas`, `numpy`).
    """
)

# --- Componente Interactivo (Slider) ---
st.subheader("Interacción con un Slider")
# Crear un slider
num_puntos = st.slider(
    "Selecciona el número de puntos de datos:",
    min_value=10,
    max_value=100,
    value=50,
    step=5
)
st.info(f"Se mostrarán **{num_puntos}** puntos de datos en el gráfico.")

# --- Visualización de Datos (Gráfico) ---
st.subheader("Gráfico de Barras Simple")

# Generar datos de ejemplo
data = pd.DataFrame(
    np.random.randn(num_puntos, 2), # Genera 'num_puntos' filas y 2 columnas de números aleatorios
    columns=['a', 'b']
)

# Crear un gráfico usando el método st.bar_chart()
st.bar_chart(data)

# --- Información Adicional ---
st.caption("¡Así de fácil es crear una aplicación interactiva con Streamlit!")

# Nota: Para ejecutar este código, guárdalo como un archivo Python (ej: app.py)
# y luego ejecuta en tu terminal: streamlit run app.py\

