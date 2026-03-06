import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components
import base64
from io import BytesIO
import os
from PIL import Image
import altair as alt

st.set_page_config(page_title='DigitalTwinLab', layout="wide")
st.markdown("""
    <style>
        /* Esto reduce el padding superior del contenedor principal */
        .block-container {
            padding-top: 1.4rem; /* Valor original es como 5rem o 6rem */
            padding-bottom: 0rem;
        }
    </style>
""",
    unsafe_allow_html=True
)
#st.title("DINÁMICA POBLACIONAL DE MICROALGAS🧫")
st.markdown("<h1 style= 'text-align: center;'>DINÁMICA POBLACIONAL DE MICROALGAS🧫</h1>", unsafe_allow_html=True)
#st.header('Columnas')
center_column, right_column = st.columns(2)

#encendido = 'False'
if 'encendido' not in st.session_state:
    st.session_state.encendido = "False"

if 'color' not in st.session_state:
    st.session_state.color = "Ninguno"
    
if 'nivel' not in st.session_state:
    st.session_state.nivel = 0
#if 'cambios' not in st.session_state:
#    st.session_state.cambios = False



#ESTADO DE LAS VARIABLES DE LOS SLIDERS
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



#ESTADO DE LAS VARIABLES DE ECUACIONES Y LAS ESPECIES
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

cantidadMicroalgasC = st.session_state.mu_chlorella
cantidadMicroalgasS = st.session_state.mu_scenedesmus
cantidadMicroalgasP = st.session_state.mu_planktothrix

cambios_js = st.session_state.color
encendido_js = st.session_state.encendido
nivel_intensidad_js = st.session_state.nivel
#cambios_js = "true" if st.session_state.cambios else "false"

#FUNCIÓN PARA CARGAR IMÁGENES
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

#with open(img_biorreactor,"rb") as f:
#    datos = f.read()
#    b64 = base64.b64encode(datos).decode()
#    # Preparamos el string para que el navegador lo entienda
#    fuente_imagen = f"data:image/png;base64,{b64}"



#PROCESO PARA CREAR COLUMA DE LA IZQUIERDA QUE ES EL PANEL DE CONTROL Y SUS RERPECTIVOS ELEMENTOS
#Left column
with st.sidebar:
    st.header('Panel de control')

    color_de_luz = st.radio(
        'Elige el color de luz',
        ("🟡Amarillo","🔴Rojo","🟢Verde","🟣Violeta"),
        horizontal=True
    )  

    intensidad = st.slider("☀️Seleccione la Intensidad de luz (lx)", 0, 15000, 300, step=1)
    temperatura = st.slider("🌡️Seleccione la Temperatura (°C)", 0, 45, 25, step=1)
    nitrogeno = st.slider("🧪Seleccione la cantidad de Nitrógeno (g/ml)", 0, 200, 100, step=1)
    
    if color_de_luz == "🟡Amarillo":
        st.session_state.color_actual = "🟡"
    elif color_de_luz == "🔴Rojo":
        st.session_state.color_actual = "🔴"
    elif color_de_luz == "🟢Verde":
        st.session_state.color_actual = "🟢"
    elif color_de_luz == "🟣Violeta":
        st.session_state.color_actual = "🟣"
    #st.session_state.color_anterior = st.session_state.color_actual

    #cambio_intensidad = st.session_state.intensidad_actual - st.session_state.intensidad_anterior

    st.divider()
    #st.write("--------------------")
    
    with st.expander("📈Tasa máxima de crecimiento (1/días)", expanded=False):
        mu_maxChlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=5.0, value=1.2, step=0.01)
        mu_maxScenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=5.0, value=1.5, step=0.01)
        mu_maxPlanktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=5.0, value=2.0, step=0.01)

    with st.expander("🔋Coeficiente de sustrato", expanded=False):
        kn_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
        kn_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
        kn_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=10.0, value=2.5, step=0.1)

    with st.expander("⚡Rendimiento", expanded=False):
        Y_chlorella = st.number_input(":green[Chlorella]", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
        Y_scenedesmus = st.number_input(":blue[Scenedesmus]", min_value=0.0, max_value=10.0, value=0.5, step=0.1)
        Y_planktothrix = st.number_input(":orange[Planktothrix]", min_value=0.0, max_value=10.0, value=0.5, step=0.1)

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

        const textura2 = await Assets.load('{img_lampara1}');
        const lampara = new Sprite(textura2);
        lampara.anchor.set(0.5);
        lampara.scale.set(0.62,0.5);
        lampara.rotation = (Math.PI * 1.5);
        lampara.x = 15;
        lampara.y = 380;
        //if (lampara.width > 300) lampara.scale.set(300 / lampara.width);

        const textura3 = await Assets.load('{img_lampara1}');
        const lampara2 = new Sprite(textura3);
        lampara2.anchor.set(0.5);
        lampara2.scale.set(0.62,0.5);
        lampara2.rotation = (Math.PI * 1.5);
        lampara2.x = 350;
        lampara2.y = 250;
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
        resplandor.x = 225;
        resplandor.y = 380;

        const imgResplandor2 = await Assets.load('{img_resplandor1}');
        const resplandor2 = new Sprite(imgResplandor2);
        resplandor2.anchor.set(0.5,0);
        resplandor2.scale.set(0.2,0.3);
        resplandor2.rotation = (Math.PI / 2);
        resplandor2.x = 250;
        resplandor2.y = 360;

        const imgResplandor3 = await Assets.load('{img_resplandor1}');
        const resplandor3 = new Sprite(imgResplandor3);
        resplandor3.anchor.set(0.5,0);
        resplandor3.scale.set(0.2,0.3);
        resplandor3.rotation = (Math.PI / 2);
        resplandor3.x = 275;
        resplandor3.y = 345;

        const imgResplandor4 = await Assets.load('{img_resplandor1}');
        const resplandor4 = new Sprite(imgResplandor4);
        resplandor4.anchor.set(0.5,0);
        resplandor4.scale.set(0.2,0.3);
        resplandor4.rotation = (Math.PI / 2);
        resplandor4.x = 495;
        resplandor4.y = 250;

        const imgResplandor5 = await Assets.load('{img_resplandor1}');
        const resplandor5 = new Sprite(imgResplandor5);
        resplandor5.anchor.set(0.5,0);
        resplandor5.scale.set(0.2,0.3);
        resplandor5.rotation = (Math.PI / 2);
        resplandor5.x = 470;
        resplandor5.y = 270;

        const imgResplandor6 = await Assets.load('{img_resplandor1}');
        const resplandor6 = new Sprite(imgResplandor6);
        resplandor6.anchor.set(0.5,0);
        resplandor6.scale.set(0.2,0.3);
        resplandor6.rotation = (Math.PI / 2);
        resplandor6.x = 445;
        resplandor6.y = 290;

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
        if(agregar_microalgas === "True"){{
            try {{
                const textura4 = await Assets.load('{img_chlorella1}');
                const textura5 = await Assets.load('{img_scenedesmus1}');
                const textura6 = await Assets.load('{img_planktothrix1}');
                for (let i = 0; i < totalMicroalgasC * 1000; i++) {{
                    const chlorella = new Sprite(textura4);
                    chlorella.anchor.set(0.5,0);
                    chlorella.scale.set(0.01,0.01);
                    chlorella.x = 200;
                    chlorella.y = 270;
                    chlorella.vx = (Math.random() - 0.5) * 0.5;
                    chlorella.vy = (Math.random() - 0.5) * 0.5;
                    app.stage.addChild(chlorella);
                    microalgas.push(chlorella);

                    const scenedesmus = new Sprite(textura5);
                    scenedesmus.anchor.set(0.5,0);
                    scenedesmus.scale.set(0.01,0.01);
                    scenedesmus.x = 165;
                    scenedesmus.y = 300;
                    scenedesmus.vx = (Math.random() - 0.5) * 0.5;
                    scenedesmus.vy = (Math.random() - 0.5) * 0.5;
                    app.stage.addChild(scenedesmus);
                    microalgas.push(scenedesmus);

                    const planktothrix = new Sprite(textura6);
                    planktothrix.anchor.set(0.5,0);
                    planktothrix.scale.set(0.01,0.01);
                    planktothrix.x = 235;
                    planktothrix.y = 300;
                    planktothrix.vx = (Math.random() - 0.5) * 0.05;
                    planktothrix.vy = (Math.random() - 0.5) * 0.05;
                    app.stage.addChild(planktothrix);
                    microalgas.push(planktothrix);
               }}

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
                    celula.rotation += 0.01;

                    // Rebotar en los bordes del biorreactor
                    if (celula.x < 123 || celula.x > 275) celula.vx *= -1;  
                    if (celula.y < 250 || celula.y > 330) celula.vy *= -1;
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

#Right column
with right_column:
    #st.subheader('Experimentación y Resultados')
    st.markdown("<h3 style= 'text-align: center;'>Experimentación y Resultados</h3>", unsafe_allow_html=True)
    sub_col1, sub_col2, sub_col3, sub_col4 = st.columns(4)
    with sub_col1:
        with st.container(border=True, height=125):
        #st.write("Color de luz: ", color_de_luz)
            st.metric(
                st.markdown("<h4 text-align: center;'>Color de luz</h4>", unsafe_allow_html=True),
                value=st.session_state.color_actual,
                delta=st.session_state.color_anterior
            )
    with sub_col2:
        with st.container(border=True, height=125):
        #st.write("Intensidad de luz:", intensidad)
        #st.write("Células Chlorella: ", st.session_state.mu)
            st.metric(
                label="<h4 text-align: center;'>Intensidad de luz</h4>",
                value=f"{intensidad}",
                delta=f"{st.session_state.cambio_intensidad} lx"
            )
    with sub_col3:
        with st.container(border=True, height=125):
        #st.write("Temperatura: ", temperatura)
            st.metric(
                label="<h4 text-align: center;'>Temperatura</h4>",
                value=temperatura,
                delta=f"{st.session_state.cambio_temperatura}"
            )
    with sub_col4:
        with st.container(border=True, height=125):
        #st.write("Nitrógeno: ", nitrogeno)
            st.metric(
                label="<h4>Nitrógeno</h4>",
                value=nitrogeno,
                delta=f"{st.session_state.cambio_nitrogeno}"
            )
    
    st.divider()

    tab_1, tab_2= st.tabs([ "📋Datos", "📊Gráficas"])
    #st.caption(f"el color es: {st.session_state.color}")

    
    #valor = st.number_input("Ingresa el valor", min_value=0, max_value=15000, value=K)

    #t = np.linspace(0, 20, 200)
    #N0 = 5
    #N = nitrogeno / (1 + ((nitrogeno-N0)/N0) * np.exp(-nitrogeno*t))
    #N = intensidad / (1 + ((intensidad-N0)/N0) * np.exp(-nitrogeno*t))
    #st.write(N)
    
    #mu = 0
    

    #E     C     U     A     C     I     Ó     N               D     E               M     O     N     O     D               P     A     R     A               C     H     L     O     R     E     L     L     A
    def monod(mu_max, N, Kn): 
        mu_max = 1.2
        s = 0.1
        Ks = 0.5
        mu = mu_max * (N/(Kn + N))
        return mu
    
    cantidad_inicial = 100
    
    def monod2(mu_max, y, N, Kn): 
        mu = ( (mu_max/-y) * (N/(Kn + N)) * cantidad_inicial)
        return mu
    st.divider()



    #B     O     T     O     N     E     S
    sub_columnaBoton1, sub_columnaBoton2 = st.columns(2)
    with sub_columnaBoton1:
    #st.button("Instrucciones para el usuario", type="secondary", key="btn_instrucciones")

        if st.button("Aplicar", type="primary", key="btn_aplicar"):
            st.session_state.color = color_de_luz
            st.session_state.encendido = "True"
            st.session_state.nivel = intensidad
            #C    H    L    O    R    E    L    L    A
            st.session_state.mu_chlorella = monod(mu_maxChlorella, nitrogeno, kn_chlorella)
            st.session_state.mu_cambioC = st.session_state.mu_chlorella - st.session_state.mu_anteriorC
            st.session_state.mu_anteriorC = st.session_state.mu_chlorella
            #S    C    E    N    E    D    E    S    M    U    S
            st.session_state.mu_scenedesmus = monod(mu_maxScenedesmus, nitrogeno, kn_scenedesmus)
            st.session_state.mu_cambioS = st.session_state.mu_scenedesmus - st.session_state.mu_anteriorS
            st.session_state.mu_anteriorS = st.session_state.mu_scenedesmus
            #P    L    A    N    K    T    O    T    H    R    I    X
            st.session_state.mu_planktothrix = monod(mu_maxPlanktothrix, nitrogeno, kn_planktothrix)
            st.session_state.mu_cambioP = st.session_state.mu_planktothrix - st.session_state.mu_anteriorP
            st.session_state.mu_anteriorP = st.session_state.mu_planktothrix

            st.session_state.intensidad_actual = intensidad
            st.session_state.cambio_intensidad = st.session_state.intensidad_actual - st.session_state.intensidad_anterior
            st.session_state.intensidad_anterior = st.session_state.intensidad_actual

            st.session_state.temperatura_actual = temperatura
            st.session_state.cambio_temperatura = st.session_state.temperatura_actual - st.session_state.temperatura_anterior
            st.session_state.temperatura_anterior = st.session_state.temperatura_actual

            st.session_state.nitrogeno_actual = nitrogeno
            st.session_state.cambio_nitrogeno = st.session_state.nitrogeno_actual - st.session_state.nitrogeno_anterior
            st.session_state.nitrogeno_anterior = st.session_state.nitrogeno_actual
            #monod(nitrogeno,Kn=0.5)
            #st.session_state.color = color_de_luz
            #cambios_js = st.session_state.color
            st.rerun()


    
    with sub_columnaBoton2:
    
        if st.button("Detener simulación", type="primary", key="btn_apagar"):
            st.session_state.encendido = "False"
            st.rerun()

            st.divider()




    #I   N   D   I   C   A   D   O   R   E   S               D   E               R   E   S   U   L   T   A   D   O   S
    sub_col5, sub_col6, sub_col7 = st.columns(3)

    with sub_col5:
        st.metric(
            label="Chlorella",
            value=f"{st.session_state.mu_chlorella:.4f}",
            delta=f"{st.session_state.mu_cambioC:.4f}"
        )
        #st.write("Chlorella ", st.session_state.mu)
    with sub_col6:
        st.metric(
            label="Scenedesmus",
            value=f"{st.session_state.mu_scenedesmus:.4f}",
            delta=f"{st.session_state.mu_cambioS:.4f}"
        )
    with sub_col7:
        st.metric(
            label="Planktohrix",
            value=f"{st.session_state.mu_planktothrix:.4f}",
            delta=f"{st.session_state.mu_cambioP:.4f}"
        )




    #A     N     Á     L     I     S     I     S               D     E               R     E     S     U     L     T     A     D     O     S

    tab1, tab2, tab3 = st.tabs(['Gráfica 1', 'Gráfica 2', 'Gráfica 3'])
    #G R A F I C A     1

    #tiempo_horas = np.linspace(0, 24, 100)
    tiempo_dias = np.linspace(0, 10, 10)
    

    exp_chlorella = cantidad_inicial * np.exp(st.session_state.mu_chlorella * tiempo_dias)
    exp_scenedesmus = cantidad_inicial * np.exp(st.session_state.mu_scenedesmus * tiempo_dias)
    exp_planktothrix = cantidad_inicial * np.exp(st.session_state.mu_planktothrix * tiempo_dias)

    df = pd.DataFrame({
        'Dias': tiempo_dias,
        'Chlorella': exp_chlorella,
        'Scenedesmus': exp_scenedesmus,
        'Planktothrix': exp_planktothrix
    })

    df_melted = df.melt(id_vars='Dias', var_name='Especie', value_name='Cantidad de células (g/ml)')

    grafica_exp = alt.Chart(df_melted).mark_line().encode(
        x=alt.X('Dias', 
                title='Tiempo (días)',
                scale=alt.Scale(domain=[0, 10])
        ),
        y=alt.Y('Cantidad de células (g/ml)', 
                title='Cantidad de células (g/ml)',
                scale=alt.Scale(domain=[0, 10000])
        ),

        color =alt.Color(
            'Especie',
            title='Especie',
            scale=alt.Scale(domain=['Chlorella', 'Scenedesmus', 'Planktothrix'],
                            range=['green', 'blue', 'orange'])
        ),
        #color='Especie',
        tooltip=['Dias', 'Cantidad de células (g/ml)']

    ).interactive()


    tab1.altair_chart(grafica_exp, use_container_width=True)



    #G R A F I C A     2
    # 1. Preparar los datos (igual que arriba)
    df = pd.DataFrame({
        'Días': tiempo_dias,
        'Chlorella': exp_chlorella,
        'Scenedesmus': exp_scenedesmus,
        'Planktothrix': exp_planktothrix
    })

    # 2. Crear la gráfica con Plotly
    # En 'y' pones una LISTA con los nombres de las columnas que quieres que sean líneas
    fig = px.line(
        df, 
        x='Días', 
        y=['Chlorella', 'Scenedesmus', 'Planktothrix'],
        title='Cinética de Crecimiento de Microalgas',
        labels={'value': 'Cantidad de células (g/ml)',
                'variable': 'Especie',
                'Días': 'Tiempo (días)'}, # Etiquetas bonitas
        markers=True, # Poner puntitos en cada dato
        color_discrete_map={
            'Chlorella': 'green',
            'Scenedesmus': 'blue',
            'Planktothrix': 'orange'
        }
    )


    # 3. Mostrar en Streamlit
    tab2.plotly_chart(fig, use_container_width=True)



    #G R A F I C A     3
    nitrogeno_seleccionado = st.session_state.nitrogeno_actual
    rango_nitrogeno = np.linspace(0, 200, 100)
    monod_chlorella = monod(mu_maxChlorella, rango_nitrogeno, kn_chlorella)
    monod_scenedesmus = monod(mu_maxScenedesmus, rango_nitrogeno, kn_scenedesmus)
    monod_planktothrix = monod(mu_maxPlanktothrix, rango_nitrogeno, kn_planktothrix)

    df_monod = pd.DataFrame({
        'Nitrógeno (g/ml)': np.linspace(0, 200, 100),
        'Chlorella': monod_chlorella,
        'Scenedesmus': monod_scenedesmus,
        'Planktothrix': monod_planktothrix
    })

    df_melted = df_monod.melt(id_vars='Nitrógeno (g/ml)', var_name='Especie', value_name='Tasa de Crecimiento')

    grafica_monod = alt.Chart(df_melted).mark_line().encode(
        x=alt.X('Nitrógeno (g/ml)', 
                title='Concentración de Nitrógeno (g/ml)',
                scale=alt.Scale(domain=[0, 200])
        ),
        y=alt.Y('Tasa de Crecimiento', 
                title='Cantidad de células (g/ml)',
                scale=alt.Scale(domain=[0, 1.5])
        ),  
        color =alt.Color(
            'Especie',
            title='Especie',
            scale=alt.Scale(domain=['Chlorella', 'Scenedesmus', 'Planktothrix'],
                            range=['green', 'blue', 'orange'])
        ),
    )

    df_identificador = pd.DataFrame({"Nitrogeno seleccionado": [nitrogeno_seleccionado]})
    capa_marcador = alt.Chart(df_identificador).mark_rule(
        color='red',
        strokeWidth=2,
        strokeDash=[5,5]
    ).encode(
        x="Nitrogeno seleccionado"
    )

    grafica_resultante = (grafica_monod + capa_marcador).interactive()
    
    tab3.altair_chart(grafica_resultante, use_container_width=True)