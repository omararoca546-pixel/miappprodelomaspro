import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import io

def crear_pdf(nombre, edad, deporte):
    """
    Crea un PDF personalizado con la información del usuario
    
    Args:
        nombre (str): Nombre del usuario
        edad (int): Edad del usuario
        deporte (str): Deporte favorito del usuario
    
    Returns:
        bytes: PDF generado en formato bytes
    """
    # Crear buffer en memoria para el PDF
    buffer = io.BytesIO()
    
    # Crear el objeto canvas
    c = canvas.Canvas(buffer, pagesize=letter)
    ancho, alto = letter
    
    # Colores personalizados
    color_titulo = HexColor('#1E3A8A')  # Azul oscuro
    color_subtitulo = HexColor('#3B82F6')  # Azul
    color_texto = HexColor('#1F2937')  # Gris oscuro
    
    # Dibujar rectángulo de encabezado
    c.setFillColor(HexColor('#EFF6FF'))  # Azul muy claro
    c.rect(0, alto - 2*inch, ancho, 2*inch, fill=1, stroke=0)
    
    # Título principal
    c.setFillColor(color_titulo)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(ancho/2, alto - 1*inch, "Presentación Personal")
    
    # Línea decorativa
    c.setStrokeColor(color_subtitulo)
    c.setLineWidth(3)
    c.line(1.5*inch, alto - 1.5*inch, ancho - 1.5*inch, alto - 1.5*inch)
    
    # Sección de información
    y_position = alto - 3*inch
    
    # Nombre
    c.setFillColor(color_subtitulo)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1.5*inch, y_position, "Nombre:")
    c.setFillColor(color_texto)
    c.setFont("Helvetica", 20)
    c.drawString(3*inch, y_position, nombre)
    
    # Edad
    y_position -= 0.8*inch
    c.setFillColor(color_subtitulo)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1.5*inch, y_position, "Edad:")
    c.setFillColor(color_texto)
    c.setFont("Helvetica", 20)
    c.drawString(3*inch, y_position, f"{edad} años")
    
    # Deporte favorito
    y_position -= 0.8*inch
    c.setFillColor(color_subtitulo)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1.5*inch, y_position, "Deporte Favorito:")
    c.setFillColor(color_texto)
    c.setFont("Helvetica", 20)
    c.drawString(4.2*inch, y_position, deporte)
    
    # Mensaje personalizado
    y_position -= 1.5*inch
    c.setFillColor(color_texto)
    c.setFont("Helvetica-Oblique", 14)
    mensaje = f"¡Hola! Mi nombre es {nombre}, tengo {edad} años y me apasiona el {deporte}."
    
    # Dividir el mensaje en líneas si es muy largo
    max_width = ancho - 3*inch
    palabras = mensaje.split()
    lineas = []
    linea_actual = ""
    
    for palabra in palabras:
        test_linea = linea_actual + " " + palabra if linea_actual else palabra
        if c.stringWidth(test_linea, "Helvetica-Oblique", 14) < max_width:
            linea_actual = test_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra
    if linea_actual:
        lineas.append(linea_actual)
    
    for linea in lineas:
        c.drawCentredString(ancho/2, y_position, linea)
        y_position -= 0.3*inch
    
    # Pie de página
    c.setFillColor(HexColor('#9CA3AF'))
    c.setFont("Helvetica", 10)
    c.drawCentredString(ancho/2, 0.5*inch, "Generado con Streamlit + ReportLab")
    
    # Finalizar el PDF
    c.save()
    
    # Obtener el contenido del PDF
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


def main():
    """
    Función principal de la aplicación Streamlit
    """
    # Configuración de la página
    st.set_page_config(
        page_title="Generador de Presentación Personal",
        page_icon="📄",
        layout="centered"
    )
    
    # Título de la aplicación
    st.title("📄 Generador de Presentación Personal en PDF")
    st.markdown("---")
    
    # Descripción
    st.markdown("""
    Completa el siguiente formulario para generar tu presentación personal en formato PDF.
    """)
    
    # Formulario
    with st.form("formulario_personal"):
        st.subheader("📝 Información Personal")
        
        # Campo de nombre
        nombre = st.text_input(
            "Nombre completo",
            placeholder="Ej: Juan Pérez",
            help="Ingresa tu nombre completo"
        )
        
        # Campo de edad
        edad = st.slider(
            "Edad",
            min_value=1,
            max_value=100,
            value=25,
            help="Selecciona tu edad"
        )
        
        # Campo de deporte favorito
        deportes = [
            "Selecciona un deporte...",
            "Fútbol",
            "Baloncesto",
            "Tenis",
            "Natación",
            "Ciclismo",
            "Voleibol",
            "Atletismo",
            "Béisbol",
            "Rugby",
            "Boxeo",
            "Artes Marciales",
            "Gimnasia",
            "Escalada",
            "Surf",
            "Skateboarding",
            "Otro"
        ]
        
        deporte = st.selectbox(
            "Deporte favorito",
            deportes,
            help="Elige tu deporte favorito"
        )
        
        # Botón de envío
        submitted = st.form_submit_button("🎯 Generar PDF", use_container_width=True)
        
        # Procesar el formulario
        if submitted:
            # Validaciones
            errores = []
            
            if not nombre or nombre.strip() == "":
                errores.append("⚠️ Por favor, ingresa tu nombre")
            
            if deporte == "Selecciona un deporte...":
                errores.append("⚠️ Por favor, selecciona un deporte")
            
            # Mostrar errores si existen
            if errores:
                for error in errores:
                    st.error(error)
            else:
                # Generar PDF
                with st.spinner("Generando tu presentación personal..."):
                    pdf_bytes = crear_pdf(nombre, edad, deporte)
                
                # Mensaje de éxito
                st.success("✅ ¡PDF generado exitosamente!")
                
                # Botón de descarga
                st.download_button(
                    label="📥 Descargar PDF",
                    data=pdf_bytes,
                    file_name=f"presentacion_{nombre.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                # Información adicional
                st.info("""
                **✨ Tu presentación personal está lista para descargar.**
                
                El PDF incluye:
                - Tu nombre completo
                - Tu edad
                - Tu deporte favorito
                - Un mensaje personalizado
                """)
    
    # Pie de página
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #6B7280; font-size: 0.9em;'>
            Desarrollado con ❤️ usando Streamlit y ReportLab
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()