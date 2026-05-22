from cProfile import label
import datetime

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
import io
from io import BytesIO
import os
from PIL import Image
import altair as alt
import serial
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title='DigitalTwinLab', layout="wide")
st.markdown("""
    <style>
        /* Esto reduce el padding superior del contenedor principal */
        .block-container {
            padding-top: 1.4rem; /* Valor original es como 5rem o 6rem */
            padding-bottom: 0rem;
        }
        .katex-display {
            margin top: 0px !important;
            margin bottom: -55px !important; /* El valor negativo acerca la gráfica hacia arriba */
        }
        
        [data-testid="stMetric"] {
            align-items: center !important;
            text-align: center !important;
        }
        /* Reduce el tamaño del título (label) del metric */
        [data-testid="stMetricLabel"] {
            font-size: 12px !important;
            padding-bottom: 0px !important;
            margin-bottom: 0px !important;
            display: flex !important;
            justify-content: center !important;
            text-align: center !important;
            width: 100% !important;
        }
        
        /* Reduce el tamaño del valor (value) del metric */
        [data-testid="stMetricValue"] {
            font-size: 22px !important;
            justify-content: center !important;
        }
        
        /* Reduce el tamaño del delta (delta) del metric */
        [data-testid="stMetricDelta"] {
            font-size: 12px !important;
            justify-content: center !important;
        }
    </style>
""",
    unsafe_allow_html=True
)

#st.title("DINÁMICA POBLACIONAL DE MICROALGAS🧫")
st.markdown("<h1 style= 'text-align: center;'>DINÁMICA POBLACIONAL DE MICROALGAS🧫</h1>", unsafe_allow_html=True)
#st.header('Columnas')
center_column, column_div, right_column = st.columns([1.5,0.1,2])

#encendido = 'False'
if 'encendido' not in st.session_state:
    st.session_state.encendido = "False"

if 'color' not in st.session_state:
    st.session_state.color = "Ninguno"

if 'color_parapixi' not in st.session_state:
    st.session_state.color_parapixi = "Ninguno"
    
if 'nivel' not in st.session_state:
    st.session_state.nivel = 0
#if 'cambios' not in st.session_state:
#    st.session_state.cambios = False
if 'dibujar_grafica' not in st.session_state:
    st.session_state.dibujar_grafica = False


#---------------------------------------------------------------------------------#
#   E S T A D O   D E   L A S   V A R I A B L E S   D E   L O S   S L I D E R S
#---------------------------------------------------------------------------------#
if 'color_actual' not in st.session_state:
    st.session_state.color_actual = ''
if 'color_anterior' not in st.session_state:
    st.session_state.color_anterior = ''

if 'intensidad_actual' not in st.session_state:
    st.session_state.intensidad_actual = 0
if 'intensidad_anterior' not in st.session_state:
    st.session_state.intensidad_anterior = 0
if 'cambio_intensidad' not in st.session_state:
    st.session_state.cambio_intensidad = 0

if 'temperatura_actual' not in st.session_state:
    st.session_state.temperatura_actual = 0
if 'temperatura_anterior' not in st.session_state:
    st.session_state.temperatura_anterior = 0
if 'cambio_temperatura' not in st.session_state:
    st.session_state.cambio_temperatura = 0

if 'nitrogeno_actual' not in st.session_state:
    st.session_state.nitrogeno_actual = 0
if 'nitrogeno_anterior' not in st.session_state:
    st.session_state.nitrogeno_anterior = 0
if 'cambio_nitrogeno' not in st.session_state:
    st.session_state.cambio_nitrogeno = 0

if 'dia_actual' not in st.session_state:
    st.session_state.dia_actual = 0

#-----------------------------------------------------------------------------------------------------------#
#  E S T A D O   D E   L A S   V A R I A B L E S   D E   E C U A C I O N E S   Y   L A S   E S P E C I E S
#-----------------------------------------------------------------------------------------------------------#
if 'mu_chlorella' not in st.session_state:
    st.session_state.mu_chlorella = 0
if 'mu_cambioC' not in st.session_state:
    st.session_state.mu_cambioC = 0
if 'mu_anteriorC' not in st.session_state:
    st.session_state.mu_anteriorC = 0

if 'mu_scenedesmus' not in st.session_state:
    st.session_state.mu_scenedesmus = 0
if 'mu_cambioS' not in st.session_state:
    st.session_state.mu_cambioS = 0
if 'mu_anteriorS' not in st.session_state:
    st.session_state.mu_anteriorS = 0

if 'mu_planktothrix' not in st.session_state:
    st.session_state.mu_planktothrix = 0
if 'mu_cambioP' not in st.session_state:
    st.session_state.mu_cambioP = 0
if 'mu_anteriorP' not in st.session_state:
    st.session_state.mu_anteriorP = 0

#cantidadMicroalgasC = st.session_state.mu_chlorella
#cantidadMicroalgasS = st.session_state.mu_scenedesmus
#cantidadMicroalgasP = st.session_state.mu_planktothrix
if 'dias_usuario' not in st.session_state:
    st.session_state.dias_usuario = 0

if 'microalgas_totales_C' not in st.session_state:
    st.session_state.microalgas_totales_C = 0
if 'microalgas_totales_S' not in st.session_state:
    st.session_state.microalgas_totales_S = 0
if 'microalgas_totales_P' not in st.session_state:
    st.session_state.microalgas_totales_P = 0

cantidadMicroalgasC = st.session_state.microalgas_totales_C
cantidadMicroalgasS = st.session_state.microalgas_totales_S
cantidadMicroalgasP = st.session_state.microalgas_totales_P



cambios_js = st.session_state.color_parapixi
encendido_js = st.session_state.encendido
nivel_intensidad_js = st.session_state.nivel
#cambios_js = "true" if st.session_state.cambios else "false"



#--------------------------------------------------------------------------------------------#
#       F  U  N  C  I  Ó  N    P  A  R  A    D  E  S  C  A  R  G  A  R    T  A  B  L  A  S
#--------------------------------------------------------------------------------------------#
def archivo_excel(df1, df2, df3, df4, df5, df6, df7):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df1.to_excel(writer, sheet_name='Exponencial', index=False)
        df2.to_excel(writer, sheet_name='Logístico', index=False)
        df3.to_excel(writer, sheet_name='Monod', index=False)
        df4.to_excel(writer, sheet_name='Fotoinhibicion', index=False)
        df5.to_excel(writer, sheet_name='Efecto de la Temperatura', index=False)
        df6.to_excel(writer, sheet_name='Competencia por el Nitrogeno', index=False)
        df7.to_excel(writer, sheet_name='Efecto de la Luz', index=False)
    datos = output.getvalue()
    return datos


#--------------------------------------------------------------------------------------------#
#       F  U  N  C  I  Ó  N    P  A  R  A    C  A  R  G  A  R    I  M  Á  G  E  N  E  S
#--------------------------------------------------------------------------------------------#
def cargar(ruta):
    if not os.path.exists(ruta): return None
    with open(ruta, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    ext = ruta.split('.')[-1].lower()
    return f"data:image/{ext};base64,{encoded}"

# 1. CONFIGURACIÓN: Pon aquí el nombre exacto de tu archivo
img_biorreactor = "imagenes/biorreactor.png"
img_lampara = "imagenes/lampara_lab.png"
img_lampara_amarilla = "imagenes/lampara_amarilla.png"
img_lampara_roja = "imagenes/lampara_roja.png"
img_lampara_verde = "imagenes/lampara_verde.png"
img_lampara_violeta = "imagenes/lampara_violeta.png"
img_resplandor = "imagenes/resplandor.png"
img_chlorella = "imagenes/Chlorella.png"
img_scenedesmus = "imagenes/Scenedesmus.png"
img_planktothrix = "imagenes/Planktothrix.png"

img_biorreactor1 = cargar(img_biorreactor)
img_lampara1 = cargar(img_lampara)
img_lampara_amarilla1 = cargar(img_lampara_amarilla)
img_lampara_roja1 = cargar(img_lampara_roja)
img_lampara_verde1 = cargar(img_lampara_verde)
img_lampara_violeta1 = cargar(img_lampara_violeta)
img_resplandor1 = cargar(img_resplandor)
img_chlorella1 = cargar(img_chlorella)
img_scenedesmus1 = cargar(img_scenedesmus)
img_planktothrix1 = cargar(img_planktothrix)

# 2. PYTHON: Lee la imagen y la convierte a texto para el navegador
if not img_biorreactor1 or not img_lampara1 or not img_lampara_amarilla1 or not img_lampara_roja1 or not img_lampara_verde1 or not img_lampara_violeta1 or not img_resplandor1 or not img_chlorella1 or not img_scenedesmus1 or not img_planktothrix1:
    st.error(f"Error")
    st.info(f"Estoy buscando en esta carpeta: {os.getcwd()}")
    st.stop() # Se detiene aquí si no hay imagen

puerto = 'COM7'

@st.cache_resource
def iniciar_conexion(puerto):
    try:
        return serial.Serial(puerto, 115200, timeout=1)
    except Exception as e:
        return None





###########################################################################################################################################
#                            P   A   N   E   L         D   E        C   O   N   T   R   O   L
###########################################################################################################################################
with st.sidebar:
    #st.header('Panel de control')
    st.markdown("<h3 style= 'text-align: center;'>Panel de control</h3>", unsafe_allow_html=True)

    #----------------------------------------------------------------------------------------------------#
    #    S  E  L  E  C  C  I  Ó  N     D  E  L     M  O  D  O     D  E     O  P  E  R  A  C  I  Ó  N
    #----------------------------------------------------------------------------------------------------#
    modo_operacion = st.sidebar.radio("Selecciona el modo de operación", ("Manual", "Tiempo-Real"), horizontal=True)
    st.sidebar.divider()
    # ///////////////////////////////
    #    M O D O     M A N U A L    
    # ///////////////////////////////
    if modo_operacion == "Manual":

        color_de_luz = st.radio(
            'Elige el color de luz',
            ("🟡Amarillo","🔴Rojo","🟢Verde","🟣Violeta"),
            horizontal=True
        )  

        intensidad = st.slider("☀️Seleccione la Intensidad de luz (lx)", 0, 15000, 300, step=1)
        with st.expander("💡Variables de intensidad de luz", expanded=False):
            with st.expander("Valor de la  absorción de fotones (alpha)", expanded=False):
                alphaC = st.number_input(":green[Chlorella]", min_value=0.0001, max_value=0.01, value=0.001, step=0.0001, format="%.4f", key="alphaC")
                alphaS = st.number_input(":blue[Scenedesmus]", min_value=0.0001, max_value=0.01, value=0.001, step=0.0001, format="%.4f", key="alphaS")
                alphaP = st.number_input(":orange[Planktothrix]", min_value=0.0001, max_value=0.01, value=0.001, step=0.0001, format="%.4f", key="alphaP")
            with st.expander("Valor del tiempo de recambio de los centros de reacción (tau)", expanded=False):
                tauC = st.number_input(":green[Chlorella]", min_value=0.001, max_value=0.5, value=0.1, step=0.001, format="%.3f", key="tauC")
                tauS = st.number_input(":blue[Scenedesmus]", min_value=0.001, max_value=0.5, value=0.1, step=0.001, format="%.3f", key="tauS")
                tauP = st.number_input(":orange[Planktothrix]", min_value=0.001, max_value=0.5, value=0.1, step=0.001, format="%.3f", key="tauP")
            with st.expander("Valor de la tasa de respiración (R)", expanded=False):
                R_chlorella = st.number_input(":green[Chlorella]", min_value=0.01, max_value=0.3, value=0.05, step=0.01, key="R_chlorella")
                R_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.01, max_value=0.3, value=0.05, step=0.01, key="R_scenedesmus")
                R_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.01, max_value=0.3, value=0.05, step=0.01, key="R_planktothrix")
            with st.expander("Coeficiente de saturacion luminosa", expanded=False):
                KI_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=10.0, value=0.5, step=0.1, key="KI_chlorella")
                KI_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=10.0, value=0.5, step=0.1, key="KI_scenedesmus")
                KI_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=10.0, value=0.5, step=0.1, key="KI_planktothrix")
            #R = st.number_input("Valor de la tasa de respiración (R)", min_value= max_value)
        
        temperatura = st.slider("🌡️Seleccione la Temperatura (°C)", 0, 45, 25, step=1)
        with st.expander("🔥Variables de temperatura", expanded=False):
            with st.expander("Valor de la tasa metabólica de referencia", expanded=False):
                resp_refC = st.number_input(":green[Chlorella]", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
                resp_refS = st.number_input(":blue[Scenedesmus]", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
                resp_refP = st.number_input(":orange[Planktothrix]", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
            with st.expander("Valor del Q10", expanded=False):
                q10C = st.number_input(":green[Chlorella]", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
                q10S = st.number_input(":blue[Scenedesmus]", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
                q10P = st.number_input(":orange[Planktothrix]", min_value=1.0, max_value=3.0, value=2.0, step=0.1)
            with st.expander("Valor de la temperatura de referencia", expanded=False):
                temp_refC = st.number_input(":green[Chlorella]", min_value=15, max_value=30, value=25, step=1)
                temp_refS = st.number_input(":blue[Scenedesmus]", min_value=15, max_value=30, value=25, step=1)
                temp_refP = st.number_input(":orange[Planktothrix]", min_value=15, max_value=30, value=25, step=1)
        nitrogeno = st.slider("🧪Seleccione la cantidad de Nitrógeno (mg/L)", 0, 200, 100, step=1)
        
        if color_de_luz == "🟡Amarillo":
            st.session_state.color_actual = "🟡"
            st.session_state.color = "🟡Amarillo"
        elif color_de_luz == "🔴Rojo":
            st.session_state.color_actual = "🔴"
            st.session_state.color = "🔴Rojo"
        elif color_de_luz == "🟢Verde":
            st.session_state.color_actual = "🟢"
            st.session_state.color = "🟢Verde"
        elif color_de_luz == "🟣Violeta":
            st.session_state.color_actual = "🟣"
            st.session_state.color = "🟣Violeta"

        with right_column:
            sub_col1, sub_col2, sub_col3 = st.columns(3, gap="small")

            with sub_col1:
                with st.container():
                    st.metric(
                        label="Intensidad de luz",
                        value=f"{intensidad} lx",
                        delta=f"{st.session_state.cambio_intensidad} lx"   
                    )  
                    
            with sub_col2:
                with st.container():
                    st.metric(
                        label="Temperatura",
                        value=f"{temperatura} °C",
                        delta=f"{st.session_state.cambio_temperatura} °C"
                    )
            with sub_col3:
                with st.container():
                #st.write("Nitrógeno: ", nitrogeno)
                    st.metric(
                        label="Nitrógeno",
                        value=f"{nitrogeno} mg/L",
                        delta=f"{st.session_state.cambio_nitrogeno}"
                    )
        
        st.divider()
        #st.write("--------------------")   



    # /////////////////////////////////////
    #    M O D O     T I E M P O - R E A L
    # /////////////////////////////////////
    else:
        st.sidebar.success("Leyendo datos en tiempo real del ESP32...")

        #sub_col1, sub_col2 = st.sidebar.columns(2)
        #sub_col1.metric("Estado", "Conectado", delta="🟢")
        #sub_col2.metric("Puerto", puerto, delta="🔌")
        ser = iniciar_conexion(puerto)
        if ser is not None and ser.is_open:
            estado = "Conectado"
            estado_puerto = f"Puerto {puerto} Activo"
            estado_icono = "✅"
        else:
            estado = "Desconectado"
            estado_puerto = "Revisar conexión"
            estado_icono = "❌"
        
        label("Estado de la conexión:")
        st.sidebar.caption(f"📊Estado: {estado} {estado_icono}")
        st.sidebar.caption(f"🔌Puerto: {estado_puerto}") 

        actualizacion = datetime.datetime.now().strftime("%H:%M:%S")
        st.sidebar.caption(f"🔄Última actualización: {actualizacion}")
        st.sidebar.divider()

        nitrogeno = st.slider("🧪Seleccione la cantidad de Nitrógeno (mg/L)", 0, 200, 100, step=1)
        with right_column:
          
            st.markdown("<h3 style= 'text-align: center;'>Experimentación y Resultados</h3>", unsafe_allow_html=True)
            @st.fragment(run_every=15)
            def actualizar_datosSensores():
                ser = iniciar_conexion(puerto)
                sensor_temperatura = st.session_state.temperatura_anterior
                sensor_luz = st.session_state.intensidad_anterior
                st.session_state.temperatura_actual = sensor_temperatura
                st.session_state.intensidad_actual = sensor_luz
                sensor_temperaturaCambio = 0.0
                sensor_luzCambio = 0.0
                if ser is not None:
                    try:
                        if ser.in_waiting > 0:
                            linea = ser.readline().decode('utf-8').strip()
                            partes = linea.split(',')
                            if len(partes) >= 2:
                                sensor_temperatura = float(partes[0])
                                sensor_luz = float(partes[1])
                                sensor_temperaturaCambio = sensor_temperatura - st.session_state.temperatura_anterior
                                sensor_luzCambio = sensor_luz - st.session_state.intensidad_anterior
                                st.session_state.temperatura_anterior = sensor_temperatura
                                st.session_state.intensidad_anterior = sensor_luz
                            
                    except Exception as e:
                        st.warning(f"Error al leer datos de temperatura: {e}")
                else:
                    st.warning(f"Esperando datos...")
                sub_col2, sub_col3, sub_col4 = st.columns(3)
                
                with sub_col2:
                    with st.container(border=True, height=135):
                        st.metric(
                            label="Intensidad de luz",
                            value=f"{sensor_luz:.2f} lx",
                            delta=f"{sensor_luzCambio:.2f} lx"   
                        )  
                
                with sub_col3:
                    with st.container(border=True, height=135):
                        st.metric(
                            label="Temperatura",
                            value=f"{sensor_temperatura:.2f} °C",
                            delta=f"{sensor_temperaturaCambio:.2f} °C"
                        )
                with sub_col4:
                    with st.container(border=True, height=135):
                    #st.write("Nitrógeno: ", nitrogeno)
                        st.metric(
                            label="Nitrógeno",
                            value=f"{nitrogeno} mg/L",
                            delta=f"{st.session_state.cambio_nitrogeno}"
                        )
            actualizar_datosSensores()



    # ---------------------------------------------------------------------------------------------------------------#
    #              P  A  R  Á  M  E  T  R  O  S      D  E      L  A     S  I  M  U  L  A  C  I  Ó  N
    # ---------------------------------------------------------------------------------------------------------------#
    
    with st.expander("Cantidad inicial de microalgas (cel/ml)", expanded=False):
            cantidad_inicial_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=1000000.0, value=10.0, step=0.1)
            cantidad_inicial_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=1000000.0, value=10.0, step=0.1)
            cantidad_inicial_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=1000000.0, value=10.0, step=0.1)
    
    with st.expander("📈Tasa máxima de crecimiento (1/días)", expanded=False):
            mu_maxChlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=5.0, value=1.2, step=0.01)
            mu_maxScenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=5.0, value=1.5, step=0.01)
            mu_maxPlanktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=5.0, value=2.0, step=0.01)
            st.session_state.mu_chlorella = mu_maxChlorella
            st.session_state.mu_scenedesmus = mu_maxScenedesmus
            st.session_state.mu_planktothrix = mu_maxPlanktothrix
            

    with st.expander("🔋Coeficiente de sustrato", expanded=False):
            kn_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
            kn_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
            kn_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=10.0, value=2.5, step=0.1)

    with st.expander("⚡Rendimiento", expanded=False):
            Y_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
            Y_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
            Y_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=10.0, value=0.5, step=0.1)

    with st.expander("🔋Capacidad de carga", expanded=False):
            Kc_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=1000000.0, value=1.0, step=0.1)
            st.session_state.microalgas_totales_C = Kc_chlorella
            Kc_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=1000000.0, value=1.0, step=0.1)
            st.session_state.microalgas_totales_S = Kc_scenedesmus
            Kc_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=1000000.0, value=1.0, step=0.1)
            st.session_state.microalgas_totales_P = Kc_planktothrix

    dias_simulacion = st.slider("Duración de la simulación (días)", 1, 30, 15, step=1)
       #dias_simulacion = st.session_state.dias_usuario
    
    velocidad_simulacion = st.slider("Velocidad de la simulación (segundos)", 0.1, 2.0, 0.5, step=0.1)
    velocidad_chlorella = int((velocidad_simulacion * 1000) / float(st.session_state.mu_chlorella))
    velocidad_scenedesmus = int((velocidad_simulacion * 1000) / float(st.session_state.mu_scenedesmus))
    velocidad_planktothrix = int((velocidad_simulacion * 1000) / float(st.session_state.mu_planktothrix))
        #velocidad_simulacion = st.session_state.tiempo_simulacion

#----------------------------------------------------------------------------------------------------------------------------------------#
#                E  C  U  A  C  I  O  N  E  S     M  A  T  E  M  Á  T  I  C  A  S     D  E     C  R  E  C  I  M  I  E  N  T  O  
#----------------------------------------------------------------------------------------------------------------------------------------#

    def monod(mu_max, N, Kn): 
        #mu_max = 1.2
        s = 0.1
        Ks = 0.5
        mu = mu_max * (N/(Kn + N))
        return mu
    
    #cantidad_inicial = 10
    
    #def monod2(mu_max, y, N, Kn): 
    #    mu = ( (mu_max/-y) * (N/(Kn + N)) * cantidad_inicial)
    #    return mu

    def modelo_haldane(mumax, alpha, intensidad_luz, tau, R):
        k_bar = mumax + R
        I_umol = intensidad_luz / 54
        mu_i = k_bar*((alpha*I_umol)/((tau*alpha*(I_umol**2))+(alpha*I_umol + 1))) - R
        return mu_i

    def ajuste_termico(resp_ref, q10, temp_ref, temp_actual):
        ajuste = resp_ref * (q10 ** ((temp_actual - temp_ref) / 10))
        return ajuste
    
    def monod_multiespecie(mu_C, y_C, N_C, mu_S, y_S, N_S, mu_P, y_P, N_P): 
        ds = - ((mu_C/y_C)*N_C) + ((mu_S/y_S)*N_S) + ((mu_P/y_P)*N_P)
        crec_c = (mu_C*N_C)
        crec_s = (mu_S*N_S)   
        crec_p = (mu_P*N_P)
        return ds, crec_c, crec_s, crec_p
    
    #def luz_intermitente(mu_lg, mu_li, mu_ls, frecuencia_mezcla, frecuencia_media_saturacion,n):

  


#------------------------------------------------#
#     B      O     T     O     N     E     S
#------------------------------------------------#

    def encender_simulacion():
        st.session_state.color_parapixi = st.session_state.color
        st.session_state.encendido = "True"
        st.session_state.nivel = intensidad

        #C   H   L   O   R   E   L   L   A
        st.session_state.mu_chlorella = monod(mu_maxChlorella, nitrogeno, kn_chlorella)
        st.session_state.mu_cambioC = st.session_state.mu_chlorella - st.session_state.mu_anteriorC
        st.session_state.mu_anteriorC = st.session_state.mu_chlorella
        
        #S   C   E   N   E   D   E   S   M   U   S
        st.session_state.mu_scenedesmus = monod(mu_maxScenedesmus, nitrogeno, kn_scenedesmus)
        st.session_state.mu_cambioS = st.session_state.mu_scenedesmus - st.session_state.mu_anteriorS
        st.session_state.mu_anteriorS = st.session_state.mu_scenedesmus
        
        #P   L   A   N   K   T   O   T   H   R   I   X
        st.session_state.mu_planktothrix = monod(mu_maxPlanktothrix, nitrogeno, kn_planktothrix)
        st.session_state.mu_cambioP = st.session_state.mu_planktothrix - st.session_state.mu_anteriorP
        st.session_state.mu_anteriorP = st.session_state.mu_planktothrix

        st.session_state.intensidad_actual = intensidad
        st.session_state.cambio_intensidad = st.session_state.intensidad_actual - st.session_state.intensidad_anterior
        st.session_state.intensidad_anterior = st.session_state.intensidad_actual

        #st.session_state.temperatura_actual = temperatura
        st.session_state.temperatura_actual = temperatura
        st.session_state.cambio_temperatura = st.session_state.temperatura_actual - st.session_state.temperatura_anterior
        st.session_state.temperatura_anterior = st.session_state.temperatura_actual

        st.session_state.nitrogeno_actual = nitrogeno
        st.session_state.cambio_nitrogeno = st.session_state.nitrogeno_actual - st.session_state.nitrogeno_anterior
        st.session_state.nitrogeno_anterior = st.session_state.nitrogeno_actual

        st.session_state.encendido = True
        st.session_state.dibujar_grafica = True

    def apagar_simulacion():
        st.session_state.encendido = False
        st.session_state.dibujar_grafica = False

    aplicar_simulacion = st.button("Aplicar cambios y simular", on_click=encender_simulacion, type="primary", key="btn_aplicar", use_container_width=True)
    detener_simulacion = st.button("Detener y reiniciar simulación", on_click=apagar_simulacion, type="secondary", key="btn_detener", use_container_width=True)
    
    




########################################################################################################################################
#                       P   A   N   E   L         D   E        V   I   S   U   A   L   I   Z   A   C   I   Ó   N
#########################################################################################################################################    
with center_column:
        #st.subheader('Visualización')
        st.markdown("<h3 style= 'text-align: center;'>Visualización</h3>", unsafe_allow_html=True)
        pixi_html = f"""
    <div id="canvas-div"></div>
    <script type="module">
        import {{ Application, Assets, Sprite, Ticker }} from 'https://cdn.jsdelivr.net/npm/pixi.js@8.1.0/dist/pixi.mjs';

        (async () => {{
            // Crear App
            const app = new Application();
            await app.init({{ width: 400, height: 600, backgroundAlpha: 0 }});
            document.getElementById("canvas-div").appendChild(app.canvas);

            // Cargar Imagen (usando el texto base64 de Python)
            const textura = await Assets.load('{img_biorreactor1}');       
            // Crear Sprite y mostrarlo
            const biorreactor = new Sprite(textura);
            biorreactor.anchor.set(0.5);          // Centro de la imagen
            biorreactor.scale.set(1,0.8);
            biorreactor.x = app.screen.width / 2; // Centro de la pantalla
            biorreactor.y = 225;      
            // Ajustar tamaño para que quepa (opcional)
            //if (biorreactor.width > 300) biorreactor.scale.set(300 / biorreactor.width);

            const totalMicroalgasC = {cantidadMicroalgasC};
            const totalMicroalgasS = {cantidadMicroalgasS};
            const totalMicroalgasP = {cantidadMicroalgasP};

            const velocidadChlorella = {velocidad_chlorella};
            const velocidadScenedesmus = {velocidad_scenedesmus};
            const velocidadPlanktothrix = {velocidad_planktothrix};


            const textura2 = await Assets.load('{img_lampara1}');
            const lampara = new Sprite(textura2);
            lampara.anchor.set(0.5);
            lampara.scale.set(0.62,0.5);
            lampara.rotation = (Math.PI * 1.5);
            lampara.x = 20;
            lampara.y = 355;
            //if (lampara.width > 300) lampara.scale.set(300 / lampara.width);

            const textura3 = await Assets.load('{img_lampara1}');
            const lampara2 = new Sprite(textura3);
            lampara2.anchor.set(0.5);
            lampara2.scale.set(0.62,0.5);
            lampara2.rotation = (Math.PI * 1.5);
            lampara2.x = 340;
            lampara2.y = 230;
            //if (lampara2.width > 300) lampara2.scale.set(300 / lampara2.width);


            const textura7 = await Assets.load('{img_lampara_amarilla1}');
            const lamp_amarilla = new Sprite(textura7);
            lamp_amarilla.anchor.set(0.5);
            lamp_amarilla.scale.set(0.62,0.5);
            lamp_amarilla.rotation = (Math.PI * 1.5);
            
            const textura8 = await Assets.load('{img_lampara_roja1}');
            const lamp_roja = new Sprite(textura8);
            lamp_roja.anchor.set(0.5);
            lamp_roja.scale.set(0.62,0.5);
            lamp_roja.rotation = (Math.PI * 1.5);

            const textura9 = await Assets.load('{img_lampara_verde1}');
            const lamp_verde = new Sprite(textura9);
            lamp_verde.anchor.set(0.5);
            lamp_verde.scale.set(0.62,0.5);
            lamp_verde.rotation = (Math.PI * 1.5);

            const textura10 = await Assets.load('{img_lampara_violeta1}');
            const lamp_violeta = new Sprite(textura10);
            lamp_violeta.anchor.set(0.5);
            lamp_violeta.scale.set(0.62,0.5);
            lamp_violeta.rotation = (Math.PI * 1.5);

            const imgResplandor = await Assets.load('{img_resplandor1}');
            const resplandor = new Sprite(imgResplandor);
            resplandor.anchor.set(0.5,0);
            resplandor.scale.set(0.2,0.3);
            resplandor.rotation = (Math.PI / 2);
            resplandor.x = 220;
            resplandor.y = 370;

            const imgResplandor2 = await Assets.load('{img_resplandor1}');
            const resplandor2 = new Sprite(imgResplandor2);
            resplandor2.anchor.set(0.5,0);
            resplandor2.scale.set(0.2,0.3);
            resplandor2.rotation = (Math.PI / 2);
            resplandor2.x = 245;
            resplandor2.y = 350;

            const imgResplandor3 = await Assets.load('{img_resplandor1}');
            const resplandor3 = new Sprite(imgResplandor3);
            resplandor3.anchor.set(0.5,0);
            resplandor3.scale.set(0.2,0.3);
            resplandor3.rotation = (Math.PI / 2);
            resplandor3.x = 270;
            resplandor3.y = 335;

            const imgResplandor4 = await Assets.load('{img_resplandor1}');
            const resplandor4 = new Sprite(imgResplandor4);
            resplandor4.anchor.set(0.5,0);
            resplandor4.scale.set(0.2,0.3);
            resplandor4.rotation = (Math.PI / 2);
            resplandor4.x = 500;
            resplandor4.y = 240;

            const imgResplandor5 = await Assets.load('{img_resplandor1}');
            const resplandor5 = new Sprite(imgResplandor5);
            resplandor5.anchor.set(0.5,0);
            resplandor5.scale.set(0.2,0.3);
            resplandor5.rotation = (Math.PI / 2);
            resplandor5.x = 475;
            resplandor5.y = 260;

            const imgResplandor6 = await Assets.load('{img_resplandor1}');
            const resplandor6 = new Sprite(imgResplandor6);
            resplandor6.anchor.set(0.5,0);
            resplandor6.scale.set(0.2,0.3);
            resplandor6.rotation = (Math.PI / 2);
            resplandor6.x = 450;
            resplandor6.y = 280;

            resplandor.visible = false;
            resplandor2.visible = false;
            resplandor3.visible = false;
            resplandor4.visible = false;
            resplandor5.visible = false;
            resplandor6.visible = false;

            app.stage.addChild(biorreactor);
            //app.stage.addChild(lampara);
            //app.stage.addChild(lampara2);
            //
            //
            //
            app.stage.addChild(resplandor);
            app.stage.addChild(resplandor2);
            app.stage.addChild(resplandor3);
            app.stage.addChild(resplandor4);
            app.stage.addChild(resplandor5);
            app.stage.addChild(resplandor6);

            let imagen1 = new Sprite(lampara);
            let imagen2 = new Sprite(lampara2);
            app.stage.addChild(imagen2);
            app.stage.addChild(imagen1);

            //Crear difuminado del resplandor
            const endAlpha = 15000;
            //const steps = 100;
            const niv_intensidad = {nivel_intensidad_js}

            function colorGradiente(){{
                const alpha = niv_intensidad / endAlpha;
                resplandor.alpha = alpha;
                resplandor2.alpha = alpha;
                resplandor3.alpha = alpha;
                resplandor4.alpha = alpha;
                resplandor5.alpha = alpha;
                resplandor6.alpha = alpha;
            }}

            colorGradiente();

            let aplicar_cambios = "{cambios_js}";
            let encender_resplandor = "{encendido_js}";
            let agregar_microalgas = "{encendido_js}";
            let detener_simulacion = "{encendido_js}";

            function efectuar_cambios(){{
                //colorGradiente();
                if(encender_resplandor === "True"){{
                    resplandor.visible = true;
                    resplandor2.visible = true;
                    resplandor3.visible = true;
                    resplandor4.visible = true;
                    resplandor5.visible = true;
                    resplandor6.visible = true;
                }}    
            
                if(aplicar_cambios === "🟡Amarillo"){{
                    imagen1.texture = lamp_amarilla.texture;
                    imagen2.texture = lamp_amarilla.texture;
                    resplandor.tint = 0xffff00;
                    resplandor2.tint = 0xffff00;
                    resplandor3.tint = 0xffff00;
                    resplandor4.tint = 0xffff00;
                    resplandor5.tint = 0xffff00;
                    resplandor6.tint = 0xffff00;
                }}
                else if(aplicar_cambios === "🔴Rojo"){{
                    imagen1.texture = lamp_roja.texture;
                    imagen2.texture = lamp_roja.texture;
                    resplandor.tint=0xff0000;
                    resplandor2.tint = 0xff0000;
                    resplandor3.tint = 0xff0000;
                    resplandor4.tint = 0xff0000;
                    resplandor5.tint = 0xff0000;
                    resplandor6.tint = 0xff0000;
                }}
                else if(aplicar_cambios === "🟢Verde"){{
                    imagen1.texture = lamp_verde.texture;
                    imagen2.texture = lamp_verde.texture;
                    resplandor.tint=0x00ff00;
                    resplandor2.tint = 0x00ff00;
                    resplandor3.tint = 0x00ff00;
                    resplandor4.tint = 0x00ff00;
                    resplandor5.tint = 0x00ff00;
                    resplandor6.tint = 0x00ff00;
                }}
                else if(aplicar_cambios === "🟣Violeta"){{
                    imagen1.texture = lamp_violeta.texture;
                    imagen2.texture = lamp_violeta.texture;
                    resplandor.tint=0x8800ff;
                    resplandor2.tint = 0x8800ff;
                    resplandor3.tint = 0x8800ff;
                    resplandor4.tint = 0x8800ff;
                    resplandor5.tint = 0x8800ff;
                    resplandor6.tint = 0x8800ff;
                }}
            }}

            efectuar_cambios();
            
            const microalgas = [];
            let contadorChlorella = 0;
            let contadorScenedesmus = 0;
            let contadorPlanktothrix = 0;
            if(agregar_microalgas === "True"){{
                try {{
                    const textura4 = await Assets.load('{img_chlorella1}');
                    const textura5 = await Assets.load('{img_scenedesmus1}');
                    const textura6 = await Assets.load('{img_planktothrix1}');
                    const motor_Chlorella = setInterval(() => {{
                        if (contadorChlorella < totalMicroalgasC) {{
                            const chlorella = new Sprite(textura4);
                            chlorella.anchor.set(0.5,0);
                            chlorella.scale.set(0.01,0.01);
                            chlorella.x = 200;
                            chlorella.y = 270;
                            chlorella.vx = (Math.random() - 0.5) * 0.08;
                            chlorella.vy = (Math.random() - 0.5) * 0.08;
                            chlorella.fasebamboleo = Math.random() * 100;
                            chlorella.velocidadbamboleo = 0.01 + Math.random() * 0.2;
                            app.stage.addChild(chlorella);
                            microalgas.push(chlorella);
                            contadorChlorella++;
                        }} else {{
                            clearInterval(motor_Chlorella);
                        }}
                                            
                    }}, velocidadChlorella);

                    const motor_Scenedesmus = setInterval(() => {{
                        if (contadorScenedesmus < totalMicroalgasS) {{
                            const scenedesmus = new Sprite(textura5);
                            scenedesmus.anchor.set(0.5,0);
                            scenedesmus.scale.set(0.01,0.01);
                            scenedesmus.x = 165;
                            scenedesmus.y = 300;
                            scenedesmus.vx = (Math.random() - 0.5) * 0.09;
                            scenedesmus.vy = (Math.random() - 0.5) * 0.09;
                            scenedesmus.fasebamboleo = Math.random() * 100;
                            scenedesmus.velocidadbamboleo = 0.01 + Math.random() * 0.1;
                            app.stage.addChild(scenedesmus);
                            microalgas.push(scenedesmus);
                            contadorScenedesmus++;
                        }} else {{
                            clearInterval(motor_Scenedesmus);
                        }}
                        
                    }}, velocidadScenedesmus);  

                    const motor_Planktothrix = setInterval(() => {{
                        if (contadorPlanktothrix < totalMicroalgasP) {{
                            const planktothrix = new Sprite(textura6);
                            planktothrix.anchor.set(0.5,0);
                            planktothrix.scale.set(0.01,0.01);
                            planktothrix.x = 235;
                            planktothrix.y = 300;
                            planktothrix.vx = (Math.random() - 0.5) * 0.05;
                            planktothrix.vy = (Math.random() - 0.5) * 0.05;
                            planktothrix.fasebamboleo = Math.random() * 100;
                            planktothrix.velocidadbamboleo = 0.1 + Math.random() * 0.2;
                            app.stage.addChild(planktothrix);
                            microalgas.push(planktothrix);
                            contadorPlanktothrix++;
                        }} else {{
                            clearInterval(motor_Planktothrix);
                        }}
                    }}, velocidadPlanktothrix);

                }}  catch (error) {{
                    console.error("Error al cargar la textura de Chlorella:", error);
            }}

            let tiempoInicio = Date.now();
            let simulacionActiva = true;
            let duracionSimulacion = 60000; // 60 segundos

            app.ticker.add(() => {{
                if (simulacionActiva !=true) return;
                microalgas.forEach((celula) => {{
                    celula.x += celula.vx;
                    celula.y += celula.vy;

                    celula.fasebamboleo += celula.velocidadbamboleo;
                    celula.x += Math.sin(celula.fasebamboleo) * 0.3;
                    celula.y += Math.cos(celula.fasebamboleo) * 0.2;

                    celula.rotation += (celula.vx *0.02);

                    // Rebotar en los bordes del biorreactor
                    if (celula.x < 123){{
                        celula.x = 123;
                        celula.vx *= -1;
                    }} else if (celula.x > 275){{
                        celula.x = 275;
                        celula.vx *= -1;
                    }}

                    /*if (celula.y < 250){{
                        celula.y = 250;
                        celula.vy *= -1;
                    }} else if (celula.y > 373){{
                        celula.y = 373;
                        celula.vy *= -1;
                    }}*/

                    let centroX = 199;
                    let radioX = 75;
                    let distanciaAlCentro = (celula.x - centroX) / radioX;

                    let curvatura = 11;
                    let limite_superior = 240 - (curvatura * (distanciaAlCentro * distanciaAlCentro));
                    let limite_inferior = 383 - (curvatura * (distanciaAlCentro * distanciaAlCentro));

                    if (celula.y < limite_superior){{
                        celula.y = limite_superior;
                        celula.vy *= -1;
                    }} else if (celula.y > limite_inferior){{
                        celula.y = limite_inferior;
                        celula.vy *= -1;
                    }}
                }});

                if(detener_simulacion === "False"){{
                    app.ticker.stop();
                    //app.ticker.start();
                }}
            }});
        }}
    }})();
    </script>
    """
        components.html(pixi_html, height=510)


with column_div:
    st.markdown("<div style= 'border-left: 3px solid #cecece; height: 560px; margin: auto; width: 2px;'></div>", unsafe_allow_html=True)







################################################################################################################################
#                      S   I   M   U   L   A   C   I   Ó   N       Y       R   E   S   U   L   T   A   D   O   S
################################################################################################################################
with right_column:
    columna_inf_izq, columna_inf_centro, columna_inf_der = st.columns([0.2,5,0.2])
    with columna_inf_centro:

        with st.expander("índice de gráficas📉"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown("""
                **1️⃣ Gráfica 1:** Crecimiento Exponencial.  
                **2️⃣ Gráfica 2:** Crecimiento Logístico.  
                **3️⃣ Gráfica 3:** Monod.
                """)
            with col_b:
                st.markdown("""
                **4️⃣ Gráfica 4:** Crecimiento con Fotoinhibición.  
                **5️⃣ Gráfica 5:** Ajuste Térmico.  
                **6️⃣ Gráfica 6:** Comparativa entre especies.
                """)
        #--------------------------------------------------------------------------------------------------#
        #     G   R   Á   F   I   C   A   S       D   E       C   R   E   C   I   M   I   E   N   T   O
        #--------------------------------------------------------------------------------------------------#
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'])
        
        with tab1:                        
            st.latex(r'''\footnotesize N(t) = N_0 e^{\mu t}''')
            graph1 = st.empty()
            df_skeleton = pd.DataFrame({
                'Días': [0, 0, 0],
                'Cantidad de células (cel/ml)': [0, 0, 0],
                'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix']
            })
            fig_exp_vacia = px.line(df_skeleton, x='Días', y='Cantidad de células (cel/ml)', color='Especie', color_discrete_sequence=['blue', 'green', 'orange'], hover_data=['Días', 'Cantidad de células (cel/ml)', 'Especie']).update_layout(
                xaxis = dict(
                            range=[0, 30],
                            title='Días'
                            ),
                yaxis = dict(
                            type='log',
                            range=[0, 7],
                            title='Cantidad de células (cel/ml)',
                            exponentformat='power'
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
            )
            graph1.plotly_chart(fig_exp_vacia, use_container_width=True, key="grafica_exponencial")

        with tab2:
            st.latex(r'''\scriptsize N(t) = \frac{K_c}{1 + \left( \frac{K_c - N_0}{N_0} \right) e^{-\mu_{max} t}}''')
            graph2 = st.empty()
            df_skeleton2 = pd.DataFrame({
                'Días': [0, 0, 0],
                'Cantidad de células (cel/ml)': [0, 0, 0],
                'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix']
            })
            fig_log_vacia = px.line(df_skeleton2, x='Días', y='Cantidad de células (cel/ml)', color='Especie', color_discrete_sequence=['blue', 'green', 'orange'], hover_data=['Días', 'Cantidad de células (cel/ml)', 'Especie']).update_layout(
                xaxis = dict(
                            range=[0, 30],
                            title='Días'
                            ),
                yaxis = dict(
                            type='log',
                            range=[0, 7],
                            title='Cantidad de células (cel/ml)',
                            exponentformat='power'
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
            )
            graph2.plotly_chart(fig_log_vacia, use_container_width=True, key="grafica_logistica")
            #with st.expander("Ver ecuación del modelo logístico", expanded=False):
            
        with tab3:
            st.latex(r'''\scriptsize \mu(N) = \mu_{max} \cdot \frac{N}{K_n + N}''')
            graph3 = st.empty()
            nitrogeno_seleccionado = st.session_state.nitrogeno_actual
            rango_nitrogeno = np.linspace(0, 200, 100)
            df_monod_vacio = pd.DataFrame({
                'Nitrógeno (mg/L)': [0, 0, 0],
                'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix'],
                'Tasa de crecimiento': [0, 0, 0]
            })
            
            fig_monod_vacia = px.line(df_monod_vacio, x='Nitrógeno (mg/L)', y='Tasa de crecimiento', color='Especie', color_discrete_sequence=['blue', 'green', 'orange'], hover_data=['Nitrógeno (mg/L)', 'Tasa de crecimiento', 'Especie']).update_layout(
                xaxis = dict(
                            range=[0, 200],
                            title='Concentración de Nitrógeno (mg/L)'
                            ),
                yaxis = dict(
                            #type='log',
                            range=[0, 5],
                            title='Cantidad de Celtulas (mg/L)',
                            #exponentformat='power'
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
            )

            fig_monod_vacia.add_vline(
                x=nitrogeno_seleccionado,
                line_width=2,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{nitrogeno_seleccionado} mg/L",
                annotation_position="top right"
            )
            graph3.plotly_chart(fig_monod_vacia, use_container_width=True)

        with tab4:
            st.latex(r'''\scriptsize \mu(I) = k \cdot \frac{\alpha I}{\tau \alpha I^2 + \alpha I + 1} - R''')
            graph4 = st.empty()
            df4 = pd.DataFrame({
                'Intensidad de Luz (Lux)': [0, 0, 0],
                'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix'],
                'Tasa metabólica ajusada': [0, 0, 0]
            })
            
            grafica_haldane = px.line(df4, x='Intensidad de Luz (Lux)', y='Tasa metabólica ajusada', color='Especie', color_discrete_sequence=['blue', 'green', 'orange'], hover_data=['Intensidad de Luz (Lux)', 'Tasa metabólica ajusada', 'Especie']).update_layout(
                xaxis = dict(
                            range=[0, 15000],
                            title='Intensidad de Luz (Lux)'
                            ),
                yaxis = dict(
                            range=[0, 1.5],
                            title='Tasa metabólica ajustada (día<sup>-1</sup>)',
                            tickformat=".1f"
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
            )

            grafica_haldane.add_vline(
                x=st.session_state.intensidad_actual,
                line_width=2,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{st.session_state.intensidad_actual} Lux",
                annotation_position="top right"
            )
            graph4.plotly_chart(grafica_haldane, use_container_width=True)
            

        with tab5:
            st.latex(r'''\scriptsize R(T) = R_{ref} \cdot Q_{10}^{\frac{T-T_{ref}}{10}}''')
            graph5 = st.empty()
            df_skeleton3 = pd.DataFrame({
                'Temperatura (°C)': [0, 0, 0],
                'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix'],
                'Tasa metabólica ajustada': [0, 0, 0]
            })
            fig_temp_vacia = px.line(df_skeleton3,x='Temperatura (°C)', y='Tasa metabólica ajustada', color='Especie', color_discrete_sequence=['blue', 'green', 'orange'], hover_data=['Temperatura (°C)', 'Tasa metabólica ajustada', 'Especie']).update_layout(
                xaxis = dict(
                            range=[0, 40],
                            title='Temperatura (°C)'
                            ),
                yaxis = dict(
                            range=[0, 0.5],
                            title='Tasa metabólica ajustada (dia<sup>-1</sup>)'
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
            )
            fig_temp_vacia.add_vline(
                x=st.session_state.temperatura_actual,
                line_width=2,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{st.session_state.temperatura_actual} °C",
                annotation_position="top right"
            )
            graph5.plotly_chart(fig_temp_vacia, use_container_width=True, key="grafica_temp")



        with tab6:
            st.latex(r'''\scriptsize \frac{dS}{dt} = -(\frac{\mu_{Chlorella}}{Y_{Chlorella}} N_{Chlorella} + \frac{\mu_{Scenedesmus}}{Y_{Scenedesmus}} N_{Scenedesmus} + \frac{\mu_{Planktothrix}}{Y_{Planktothrix}} N_{Planktothrix})''')
            graph6 = st.empty()
            df_skeleton6 = pd.DataFrame({
                'Dia': [0, 0, 0],
                'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix'],
                'Nitrógeno (mg/L)': [0, 0, 0]
            })

            #fig_mondod_multiespecie_vacia = make_subplots(specs=[[{"secondary_y": True}]])
            fig_mondod_multiespecie_vacia = px.line(df_skeleton6,x='Dia', y='Nitrógeno (mg/L)', color='Especie', color_discrete_sequence=['blue', 'green', 'orange'], hover_data=['Dia', 'Nitrógeno (mg/L)', 'Especie'])


            fig_mondod_multiespecie_vacia.add_trace(
                go.Scatter(
                    x=df_skeleton6['Dia'],
                    y=df_skeleton6['Nitrógeno (mg/L)'],
                    mode='lines',
                    name='Nitrogeno restante',
                    line=dict(color='gray', width=2, dash='dot'),
                    yaxis='y2'
                )
            )

            fig_mondod_multiespecie_vacia.update_layout(
                margin=dict(l=10, r=10, t=20, b=5),
                hovermode='x unified',
                height=300, 
                xaxis = dict(
                            range=[0, 30],
                            title='Días'
                            ),
                yaxis = dict(
                            #range=[0, 200],
                            title='Cantidad de celulas (cel/ml)',
                            exponentformat='power'
                            ),

                yaxis2=dict(
                    title = 'Nitrogeno restante (mg/L)',
                    overlaying = 'y',
                    side = 'right',
                    range=[0, 200]
                ),
                legend = dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                    title = None,
                    font = dict(size = 10)
                ),

            )
            fig_mondod_multiespecie_vacia.add_hline(
                y=st.session_state.nitrogeno_actual,
                line_width=2,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{st.session_state.nitrogeno_actual} mg/L",
                annotation_position="top right"
            )

            fig_mondod_multiespecie_vacia.add_vline(
                x=st.session_state.dia_actual,
                line_width=2,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{st.session_state.dia_actual} d",
                annotation_position="top right"
            )
            graph6.plotly_chart(fig_mondod_multiespecie_vacia, use_container_width=True)


        with tab7:
            st.latex(r'''\scriptsize \mu_{i} = \mu_{max,i} \cdot \frac{I_0 \cdot e^{-\sum_{j=1}^{n} k_j X_j}}{K_I,i + I_0 \cdot e^{-\sum_{j=1}^{n} k_j X_j}}''')
 
            graph7 = st.empty()
            grafica_mondod_vacia = px.line(
                pd.DataFrame({
                    'Dia': [0, 0, 0],
                    'Especie': ['Chlorella', 'Scenedesmus', 'Planktothrix'],
                    'Cantidad de celulas (cel/ml)': [0, 0, 0]
                }),
                x='Dia',
                y='Cantidad de celulas (cel/ml)',
                color='Especie',
                color_discrete_sequence=['blue', 'green', 'orange'],
                hover_data=['Dia', 'Cantidad de celulas (cel/ml)', 'Especie']
            ).update_layout(
                xaxis = dict(
                    range=[0, 30],
                    title='Días',
                ),
                yaxis = dict(
                    title='Cantidad de celulas (cel/ml)',
                    type='log',
                    range=[0, 5],
                    exponentformat='power'
                ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
            )
    
            graph7.plotly_chart(grafica_mondod_vacia, use_container_width=True)

if st.session_state.dibujar_grafica:
    st.session_state.dia_actual = 0

    #/////////////////////
    #  G R A F I C A   1
    #/////////////////////
    #tiempo_horas = np.linspace(0, 24, 100)
    #Crea rango de tiempo en días (0 a 30 días, con 30 puntos)
    
    tiempo_dias = np.linspace(0, dias_simulacion, dias_simulacion + 1) # Esto crea un rango de 0 a 30 días con un punto por cada día (31 puntos en total)
    #tiempo_dias = np.arange(0, 31)
 
    exp_chlorella = cantidad_inicial_chlorella * np.exp(st.session_state.mu_chlorella * tiempo_dias)
    exp_scenedesmus = cantidad_inicial_scenedesmus * np.exp(st.session_state.mu_scenedesmus * tiempo_dias)
    exp_planktothrix = cantidad_inicial_planktothrix * np.exp(st.session_state.mu_planktothrix * tiempo_dias)

    #Dataframe con los resultados de la cantidad de microalgas que se reproducieron en función del tiempo para cada especie
    df = pd.DataFrame({
        'Dias': tiempo_dias,
        'Chlorella': exp_chlorella,
        'Scenedesmus': exp_scenedesmus,
        'Planktothrix': exp_planktothrix
    })


    # Personalización de la gráfica estableciendo colores y títulos a los ejes
    df_melted = df.melt(id_vars='Dias', var_name='Especie', value_name='Cantidad de células (cel/ml)')
    max_dias = df_melted['Dias'].max()
    max_celulas = df_melted['Cantidad de células (cel/ml)'].max()

    #/////////////////////
    #  G R A F I C A   2
    #/////////////////////
    # 1. Preparar los datos (igual que arriba)
    Log_chlorella = Kc_chlorella / (1 + ((Kc_chlorella - cantidad_inicial_chlorella) / cantidad_inicial_chlorella) * np.exp(-mu_maxChlorella* tiempo_dias))
    Log_scenedesmus = Kc_scenedesmus / (1 + ((Kc_scenedesmus - cantidad_inicial_scenedesmus) / cantidad_inicial_scenedesmus) * np.exp(-mu_maxScenedesmus * tiempo_dias))
    Log_planktothrix = Kc_planktothrix / (1 + ((Kc_planktothrix - cantidad_inicial_planktothrix) / cantidad_inicial_planktothrix) * np.exp(-mu_maxPlanktothrix * tiempo_dias))

    df2 = pd.DataFrame({
        'Días': tiempo_dias,
        'Chlorella': Log_chlorella,
        'Scenedesmus': Log_scenedesmus,
        'Planktothrix': Log_planktothrix
    })    

    df_melted2 = df2.melt(id_vars='Días', var_name='Especie', value_name='Cantidad de células (cel/ml)')
    max_dias = df_melted2['Días'].max()
    max_celulas = df_melted2['Cantidad de células (cel/ml)'].max()


    #/////////////////////
    #  G R A F I C A   3
    #/////////////////////
    nitrogeno_seleccionado = st.session_state.nitrogeno_actual
    rango_nitrogeno = np.linspace(0, 200, 101)
    monod_chlorella = monod(mu_maxChlorella, rango_nitrogeno, kn_chlorella)
    monod_scenedesmus = monod(mu_maxScenedesmus, rango_nitrogeno, kn_scenedesmus)
    monod_planktothrix = monod(mu_maxPlanktothrix, rango_nitrogeno, kn_planktothrix)

    df_monod = pd.DataFrame({
        'Nitrógeno (mg/L)': rango_nitrogeno,
        'Chlorella': monod_chlorella,
        'Scenedesmus': monod_scenedesmus,
        'Planktothrix': monod_planktothrix
    })

    #df_melted3 = df_monod.melt(id_vars='Nitrógeno (g/ml)', var_name='Especie', value_name='Tasa de Crecimiento')
    total_dias = int(max_dias)
    total_nitrogeno =len(df_monod['Nitrógeno (mg/L)'])
    nitrogeno_diario = int(total_nitrogeno / total_dias)


    #/////////////////////
    #  G R A F I C A   4
    #/////////////////////
    rango_luz = np.linspace(0, 15000, 101)
    haldane_chlorella = modelo_haldane(mu_maxChlorella, alphaC, rango_luz, tauC, R_chlorella)
    haldane_scenedesmus = modelo_haldane(mu_maxScenedesmus, alphaS, rango_luz, tauS, R_scenedesmus)
    haldane_planktothrix = modelo_haldane(mu_maxPlanktothrix, alphaP, rango_luz, tauP, R_planktothrix)

    df4 = pd.DataFrame({
        'Intensidad de Luz (Lux)': rango_luz,
        'Chlorella': haldane_chlorella,
        'Scenedesmus': haldane_scenedesmus,
        'Planktothrix': haldane_planktothrix
    })
    #df_melted4 = df4.melt(id_vars='Intensidad de Luz (μmol/m²/s)', var_name='Especie', value_name='Tasa metabólica ajustada')
    total_luz = len(df4['Intensidad de Luz (Lux)'])
    haldane_diario = (total_luz / total_dias)

    #/////////////////////
    #  G R A F I C A   5
    #/////////////////////
    rango_temperatura = np.linspace(0, 45, 46)
    ajuste_termico_chlorella = ajuste_termico(resp_refC, q10C, temp_refC, rango_temperatura)
    ajuste_termico_scenedesmus = ajuste_termico(resp_refS, q10S, temp_refS, rango_temperatura)
    ajuste_termico_planktothrix = ajuste_termico(resp_refP, q10P, temp_refP, rango_temperatura)

    df5 = pd.DataFrame({
        'Temperatura (°C)': rango_temperatura,
        'Chlorella': ajuste_termico_chlorella,
        'Scenedesmus': ajuste_termico_scenedesmus,
        'Planktothrix': ajuste_termico_planktothrix
    })
    df_melted5 = df5.melt(id_vars='Temperatura (°C)', var_name='Especie', value_name='Tasa metabólica ajustada')
    #total_temp = len(df5['Temperatura (°C)'])
    #ajuste_temp_diario = (total_temp / total_dias)

    #/////////////////////
    #  G R A F I C A   6
    #/////////////////////
    nitrogeno_hoy = float(st.session_state.nitrogeno_actual)
    N_chlorella = float(cantidad_inicial_chlorella)
    N_scenedesmus = float(cantidad_inicial_scenedesmus)
    N_planktothrix = float(cantidad_inicial_planktothrix)

    Ks_chlorella = float(kn_chlorella)
    Ks_scenedesmus = float(kn_scenedesmus)
    Ks_planktothrix = float(kn_planktothrix)

    mu_maxChlo = float(mu_maxChlorella)
    mu_maxScen = float(mu_maxScenedesmus)
    mu_maxPlank = float(mu_maxPlanktothrix)

    ren_chlo = float(Y_chlorella)
    ren_scen = float(Y_scenedesmus)
    ren_plank = float(Y_planktothrix)

    registro_historico = []
    registro_historico.append({'Dias': 0, 'Nitrógeno (mg/L)': nitrogeno_hoy, 'Chlorella': N_chlorella, 'Scenedesmus': N_scenedesmus, 'Planktothrix': N_planktothrix})
    #max_dias = df_melted6['Dias'].max()
    #consumo = df_melted6['Tasa de consumo'].max()

    #/////////////////////
    #  G R A F I C A   7
    #/////////////////////
    registro_historico2 = []
    registro_historico2.append({'Días': 0, 'Chlorella': N_chlorella, 'Scenedesmus': N_scenedesmus, 'Planktothrix': N_planktothrix})

    # CICLO PARA SIMULAR LA ANIMACIÓN DE CRECIMIENTO EN LAS GRÁFICAS
    for dia in range(1, int(max_dias)+1):
        #GRAFICA 1
        df_filtrado = df_melted[df_melted['Dias'] <= dia]

        #GRAFICA 2
        df_filtrado2 = df_melted2[df_melted2['Días'] <= dia]
        
        #GRAFICA 3
        limite_diario_nitrogeno = (dia*nitrogeno_diario)
        df_filtrado3 = df_monod.iloc[:limite_diario_nitrogeno]
        
        #GRAFICA 4
        limite_diario_haldane = int(dia*haldane_diario)
        df_filtrado4 = df4.iloc[:limite_diario_haldane]   

        #GRAFICA 5
        limite_temp = (dia/int(max_dias))*45
        df_filtrado5 = df_melted5[df_melted5['Temperatura (°C)'] <= limite_temp]

        #GRAFICA 6
        if nitrogeno_hoy > 0:
            mu_chl = mu_maxChlo * (nitrogeno_hoy / (Ks_chlorella + nitrogeno_hoy))
            mu_sce = mu_maxScen * (nitrogeno_hoy / (Ks_scenedesmus + nitrogeno_hoy))
            mu_plk = mu_maxPlank * (nitrogeno_hoy / (Ks_planktothrix + nitrogeno_hoy))
        else:
            mu_chl = mu_sce = mu_plk = 0
        
        crec_chl = mu_chl * N_chlorella
        crec_sce = mu_sce * N_scenedesmus
        crec_plk = mu_plk * N_planktothrix

        cons_chl = crec_chl / Y_chlorella
        cons_sce = crec_sce / Y_scenedesmus 
        cons_plk = crec_plk / Y_planktothrix

        consumo_total_hoy = cons_chl + cons_sce + cons_plk

        if consumo_total_hoy > nitrogeno_hoy:
            reparticion = nitrogeno_hoy / consumo_total_hoy

            cons_chl = cons_chl * reparticion
            cons_sce = cons_sce * reparticion
            cons_plk = cons_plk * reparticion

            consumo_total_hoy = nitrogeno_hoy
            st.session_state.dia_actual = dia

        nitrogeno_hoy = nitrogeno_hoy - consumo_total_hoy
        N_chlorella += crec_chl
        N_scenedesmus += crec_sce
        N_planktothrix += crec_plk

        registro_historico.append({'Dias': dia, 'Nitrógeno (mg/L)': nitrogeno_hoy, 'Chlorella': N_chlorella, 'Scenedesmus': N_scenedesmus, 'Planktothrix': N_planktothrix})
        df_historico = pd.DataFrame(registro_historico)
        df_melted6 = df_historico.melt(id_vars=['Dias', 'Nitrógeno (mg/L)'], value_vars=['Chlorella', 'Scenedesmus', 'Planktothrix'], var_name='Especie', value_name='Consumo de Nitrogeno (mg/L)')
        
        #GRAFICA 7
        luz_disponible = (intensidad * 0.015) * np.exp(-((alphaC*N_chlorella)+(alphaS*N_scenedesmus)+(alphaP*N_planktothrix)))
        tasa_crecimiento_luz_chl = mu_maxChlorella * (luz_disponible/(KI_chlorella + luz_disponible))
        tasa_crecimiento_luz_sce = mu_maxScenedesmus * (luz_disponible/(KI_scenedesmus + luz_disponible))
        tasa_crecimiento_luz_plank = mu_maxPlanktothrix * (luz_disponible/(KI_planktothrix + luz_disponible))

        N_chlorella += (N_chlorella * tasa_crecimiento_luz_chl)
        N_scenedesmus += (N_scenedesmus * tasa_crecimiento_luz_sce)
        N_planktothrix += (N_planktothrix * tasa_crecimiento_luz_plank)
        registro_historico2.append({'Días': dia, 'Chlorella': N_chlorella, 'Scenedesmus': N_scenedesmus, 'Planktothrix': N_planktothrix})
        df_historico2 = pd.DataFrame(registro_historico2)
        df_melted7 = df_historico2.melt(id_vars=['Días'], value_vars=['Chlorella', 'Scenedesmus', 'Planktothrix'], var_name='Especie', value_name='Especie (cel/ml)')
        #################################################################################################
        #I  N  I  C  I  O    D  E    G  E  N  E  R  A  C  I  Ó  N    D  E    G  R  Á  F  I  C  A  S
        #################################################################################################
        fig1 = px.line(
            df_filtrado,
            x='Dias',
            y='Cantidad de células (cel/ml)',
            color='Especie',
            #hover_data=['Dias', 'Cantidad de células (g/ml)', 'Especie'],
            #title='Crecimiento Exponencial de Microalgas',
            labels={'value': 'Cantidad de células (cel/ml)',
                    'variable': 'Especie',
                    'Dias': 'Tiempo (días)'}, # Etiquetas bonitas
            #markers=True, # Poner puntitos en cada dato
            color_discrete_map={
                'Chlorella': 'green',
                'Scenedesmus': 'blue',
                'Planktothrix': 'orange'
            }
        )
        fig1.update_layout(
            margin=dict(l=20, r=20, t=0, b=5),
            hovermode='x unified',
            height=300, 
            xaxis=dict(
                range=[0, dias_simulacion],
                title='Tiempo (días)',
                hoverformat='.0f',
                #dtick=2
            ),
            yaxis=dict(
                type='log',
                #range=[0, 7],
                title='Cantidad de células (cel/ml)',
                exponentformat='power',
                #tickformat=".2e",
                #nticks=6,
                dtick=6
            )
        )
        graph1.plotly_chart(fig1, use_container_width=True,)
        time.sleep(velocidad_simulacion)  # Pausa para simular la animación
        #-----------------------------------------------------------------------------------------------------------------
        
        fig2 = px.line(
            df_filtrado2, 
            x='Días', 
            y='Cantidad de células (cel/ml)',
            color='Especie',
            #hover_data=['Días', 'Cantidad de células (g/ml)', 'Especie'],
            #title='Cinética de Crecimiento de Microalgas',
            labels={'value': 'Cantidad de células (cel/ml)',
                    'variable': 'Especie',
                    'Días': 'Tiempo (días)'}, # Etiquetas bonitas
            #markers=True, # Poner puntitos en cada dato
            color_discrete_map={
                'Chlorella': 'green',
                'Scenedesmus': 'blue',
                'Planktothrix': 'orange'
            }
        )

        fig2.update_layout(
            margin=dict(l=20, r=20, t=0, b=5),
            hovermode='x unified',
            height=300, 
            xaxis=dict(
                range=[0, dias_simulacion],
                title='Tiempo (días)',
                hoverformat='.0f',
                #dtick=2
            ),
            yaxis=dict(
                type='log',
                #range=[0, 7],
                title='Cantidad de células (cel/ml)',
                exponentformat='power',
                #tickformat=".2e",
                #nticks=7
                dtick=1
            )
        )
        
        graph2.plotly_chart(fig2, use_container_width=True)
        time.sleep(velocidad_simulacion)  # Pausa para simular la animación 
        #-----------------------------------------------------------------------------------------------------------------

        df_monod_animado = df_filtrado3.melt(
            id_vars='Nitrógeno (mg/L)',
            var_name='Especie',
            value_name='Tasa de Crecimiento'
        )
        grafica_monod = px.line(
            df_monod_animado, 
            x='Nitrógeno (mg/L)', 
            y='Tasa de Crecimiento', 
            color='Especie', 
            color_discrete_sequence=['blue', 'green', 'orange'], 
            hover_data=['Nitrógeno (mg/L)', 'Tasa de Crecimiento', 'Especie']).update_layout(
                #uirevision='fixed',
                xaxis = dict(
                            range=[0, 200],
                            title='Concentración de Nitrógeno (mg/L)'
                            ),
                yaxis = dict(
                            #type='log',
                            range=[0, 5],
                            title='Cantidad de Celtulas (cel/ml)',
                            #exponentformat='power'
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
        )

        grafica_monod.add_vline(
            x=nitrogeno_seleccionado,
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text=f"{nitrogeno_seleccionado} mg/L",
            annotation_position="top right"
        )
        graph3.plotly_chart(grafica_monod, use_container_width=True)
        time.sleep(velocidad_simulacion)

        #-----------------------------------------------------------------------------------------------------------------

        df_haldane_animado = df_filtrado4.melt(
            id_vars='Intensidad de Luz (Lux)',
            var_name='Especie',
            value_name='Tasa de crecimiento neta'
        )
        
        grafica_haldane = px.line(
            df_haldane_animado, 
            x='Intensidad de Luz (Lux)', 
            y='Tasa de crecimiento neta', 
            color='Especie', 
            color_discrete_sequence=['blue', 'green', 'orange'], 
            hover_data=['Intensidad de Luz (Lux)', 'Tasa de crecimiento neta', 'Especie']).update_layout(
                #uirevision='fixed',
                xaxis = dict(
                            range=[0, 15000],
                            title='Intensidad de Luz (Lux)'
                            ),
                yaxis = dict(
                            #type='log',
                            #range=[0, 1.5],
                            title='Tasa de crecimiento neta (día<sup>-1</sup>)',
                            tickformat=".1f",
                            dtick=0.1
                            #exponentformat='power'
                            ),
                legend = dict(title='Especie'),
                margin=dict(l=20, r=20, t=0, b=5),
                width=350,
                height=300
        )

        grafica_haldane.add_vline(
            x=st.session_state.intensidad_actual,
            line_width=2,
            line_dash="dash",
            line_color="red",
            annotation_text=f"{st.session_state.intensidad_actual} Lux",
            annotation_position="top right"
        )
        graph4.plotly_chart(grafica_haldane, use_container_width=True)
        time.sleep(velocidad_simulacion)

        #-----------------------------------------------------------------------------------------------------------------     

        fig5 = px.line(df_filtrado5, x='Temperatura (°C)', y='Tasa metabólica ajustada', color='Especie',
                    #hover_data=['Días', 'Tasa de Crecimiento', 'Especie'],
                    #title='Crecimiento Exponencial de Microalgas',
                    labels={'value': 'Tasa de Crecimiento',
                            'variable': 'Especie',
                            'Temperatura (°C)': 'Temperatura (°C)'}, # Etiquetas bonitas
                    #markers=True, # Poner puntitos en cada dato
                    color_discrete_map={
                        'Chlorella': 'green',
                        'Scenedesmus': 'blue',
                        'Planktothrix': 'orange'
                    }
                    )
        fig5.update_layout(
            margin=dict(l=20, r=20, t=0, b=5),
            hovermode='x unified',
            height=300, 
            xaxis=dict(
                range=[0, 45],
                title='Temperatura (°C)',
                hoverformat='.0f',
                #dtick=2
            ),
            yaxis=dict(
                #type='log',
                range=[0, 0.5],
                title='Tasa metabólica ajustada (día<sup>-1</sup>)',
                #tickformat=".2e",
                #nticks=7
            )
        )
        fig5.add_vline(
            x=st.session_state.temperatura_actual, 
            line_width=1, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"{st.session_state.temperatura_actual} °C",
            annotation_position="top right"
        )
        graph5.plotly_chart(fig5, use_container_width=True)
        time.sleep(velocidad_simulacion)

        #----------------------------------------------------------------------------------------------------------------- 
        
        fig6 = px.line(df_melted6, x='Dias', y='Consumo de Nitrogeno (mg/L)', color='Especie',
                    #hover_data=['Días', 'Tasa de Crecimiento', 'Especie'],
                    #title='Crecimiento Exponencial de Microalgas',
                    labels={'value': 'Nitrogeno (mg/L)',
                            'variable': 'Especie',
                            'Dias': 'Dias'}, # Etiquetas bonitas
                    #markers=True, # Poner puntitos en cada dato
                    color_discrete_map={
                        'Chlorella': 'green',
                        'Scenedesmus': 'blue',
                        'Planktothrix': 'orange'
                    }
                )

        fig6.add_trace(
            go.Scatter(
                x=df_historico['Dias'],
                y=df_historico['Nitrógeno (mg/L)'],
                mode='lines',
                name='Nitrogeno restante',
                line=dict(color='gray', width=2, dash='dot'),
                yaxis='y2'
            )
        )
        fig6.update_layout(
            margin=dict(l=10, r=10, t=20, b=5),
            hovermode='x unified',
            height=300, 
            xaxis=dict(
                range=[0, dias_simulacion],
                title='Dias',
                hoverformat='.0f',
                #dtick=2
            ),
            yaxis=dict(
                #type='log',
                #range=[0, 200   ],
                title='Cantidad de celulas (cel/ml)',
                exponentformat='power'
                #tickformat=".2e",
                #nticks=7
            ),
            yaxis2=dict(
                title = 'Nitrogeno restante (mg/L)',
                overlaying = 'y',
                side = 'right',
                range=[0, st.session_state.nitrogeno_actual]
            ),
            legend = dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title = None,
                font = dict(size = 10)
            )
            
        )
        fig6.add_hline(
            y=st.session_state.nitrogeno_actual, 
            line_width=1, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"{st.session_state.nitrogeno_actual} mg/L",
            annotation_position="top right"
        )
        if st.session_state.dia_actual != 0 and dia >= st.session_state.dia_actual:
            
            fig6.add_vline(
                x=st.session_state.dia_actual, 
                line_width=1, 
                line_dash="dash", 
                line_color="red",
                annotation_text=f"{st.session_state.dia_actual} dias",
                annotation_position="top right"
            )
        graph6.plotly_chart(fig6, use_container_width=True)
        time.sleep(velocidad_simulacion)
    
   #----------------------------------------------------------------------------------------------------------------- 

        fig7 = px.line(df_melted7, x='Días', y='Especie (cel/ml)', color='Especie',
                    #hover_data=['Días', 'Tasa de Crecimiento', 'Especie'],
                    #title='Crecimiento Exponencial de Microalgas',
                    labels={'value': 'Nitrogeno (mg/L)',
                            'variable': 'Especie',
                            'Dias': 'Dias'}, # Etiquetas bonitas
                    #markers=True, # Poner puntitos en cada dato
                    color_discrete_map={
                        'Chlorella': 'green',
                        'Scenedesmus': 'blue',
                        'Planktothrix': 'orange'
                    }
                )

        fig7.update_layout(
            margin=dict(l=10, r=10, t=20, b=5),
            hovermode='x unified',
            height=300, 
            xaxis=dict(
                range=[0, dias_simulacion],
                title='Dias',
                hoverformat='.0f',
                #dtick=2
            ),
            yaxis=dict(
                #type='log',
                #range=[0, 200   ],
                title='Cantidad de celulas (cel/ml)',
                exponentformat='power'
                #tickformat=".2e",
                #nticks=7
            )
        )    
        fig7.add_vline(
            x = st.session_state.nitrogeno_actual, 
            line_width=1, 
            line_dash="dash", 
            line_color="red",
            annotation_text=f"{st.session_state.nitrogeno_actual} mg/L",
            annotation_position="top right"
        )

        graph7.plotly_chart(fig7, use_container_width=True)
        time.sleep(velocidad_simulacion)
    


    #############################################################################################
    #               G  E  N  E  R  A  C  I  O  N    D  E    T  A  B  L  A  S
    #############################################################################################
    st.session_state.dibujar_grafica = False
    st.toast("Simulación finalizada. Desliza hacia abajo para ver los resultados", icon="✅")
    st.success("Los resultados ya estan disponibles 👇")
    
    with st.expander("Ver resultados"):
        st.markdown("### Tabla de resultados completos")
        
        res_grafica1, res_grafica2, res_grafica3, res_grafica4, res_grafica5, res_grafica6, res_grafica7 = st.tabs(["Grafica 1", "Grafica 2", "Grafica 3", "Grafica 4", "Grafica 5", "Grafica 6", "Grafica 7"])
        with res_grafica1:
            #tabla_excel = archivo_excel(df)
            st.dataframe(df, use_container_width=True)
        with res_grafica2:
            #tabla_excel2 = archivo_excel(df2)
            st.dataframe(df2, use_container_width=True)
        with res_grafica3:
            #tabla_excel3 = archivo_excel(df_monod)
            st.dataframe(df_monod, use_container_width=True)
        with res_grafica4:
            #tabla_excel4 = archivo_excel(df4)
            st.dataframe(df4, use_container_width=True)
        with res_grafica5:
            #tabla_excel5 = archivo_excel(df5)
            st.dataframe(df5, use_container_width=True)
        with res_grafica6:
            #tabla_excel6 = archivo_excel(df6)
            st.dataframe(df_historico, use_container_width=True)
        with res_grafica7:
            #tabla_excel7 = archivo_excel(df7)
            st.dataframe(df_historico2, use_container_width=True)
        tabla_excel = archivo_excel(df, df2, df_monod, df4, df5, df_historico, df_historico2)
        st.download_button(
            label="Descargar todos los resultados",
            data=tabla_excel,
            file_name="tabla_resultados.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
  
    
    
    

###########################################################################################################################################
#                   F   U   N   C   I   O   N   A   L   I   D   A   D        D   E        B   O   T   O   N   E   S
###########################################################################################################################################


