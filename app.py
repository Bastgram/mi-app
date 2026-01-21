import streamlit as st
import pandas as pd
from fpdf import FPDF
import datetime
import tempfile
import os

# ==============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ==============================================================================
st.set_page_config(page_title="Estudio Carga Combustible", layout="wide")

# Título de la app
st.title("🔥 Estudio de Carga Combustible")
st.markdown("Cálculo basado en **NCh1916, NCh1993 y OGUC**.")

# ==============================================================================
# BASE DE DATOS (MATERIALES Y NORMATIVAS)
# ==============================================================================
calor_comb = {
    "aceite comestible": 46, "aceite de alquitrán": 46, "aceite de colza": 41.9, "aceite de creosota": 37.5,
    "aceite de hígado": 37.5, "aceite de lino": 37.5, "aceite de nabo silvestre": 41.9, "aceite de oliva": 41.9,
    "aceite de parafina": 41.9, "aceite de pino": 41.9, "aceite de ricino": 41.9, "aceite de semillas de algodón": 37.5,
    "aceite de soja": 41.9, "aceite diesel": 46, "aceite pesado de petróleo": 42.7, "acenilacetona": 25.1,
    "acetaldehído": 25.1, "acetamida": 20.9, "acetanilida": 33.5, "acetato de amilo": 33.5, "acetato de etilo": 25.5,
    "acetato de metilo": 21.3, "acetato de polivinilo": 20.9, "acetileno": 50.2, "acetileno (gas)": 49.8,
    "acetofenona": 33.5, "acetona": 30.6, "acetonitrilo": 29.3, "acido acético": 16.8, "acido acrílico": 18,
    "acido acroleico": 16.8, "acido adípico": 22.3, "acido benzoico": 25.1, "acido butírico n-": 25.1,
    "acido caprónico": 29.3, "acido cianocético": 16.8, "acido cítrico": 25.1, "acido de canela": 29.3,
    "acido dietilacético": 29.3, "acido etilbutírico": 29.3, "acido fórmico": 5.9, "acido oleico": 37,
    "acido oxálico n-": 29.3, "acido tartárico": 6.7, "acroleína": 29.3, "alanina": 16.8, "albúmina vegetal": 25.1,
    "alcanfor": 37.5, "alcohol alílico": 33.5, "alcohol amílico": 41.9, "alcohol cetílico": 41.9,
    "alcohol de benzilo": 33.5, "alcohol etílico": 29.7, "alcohol hexadehílico": 41.9, "alcohol isopropílico": 30.2,
    "alcohol metílico": 22.2, "alcohol n-butílico": 33.6, "alcohol propílico": 30.7, "aldehido de canela": 33.5,
    "aldehido fórmico": 29.8, "aldehido propílico": 29, "aldol": 25.1, "algodón": 16.8, "almendra": 16.8,
    "almidón": 16.8, "alquitrán de hulla": 37.2, "anhídrido de ácido acético": 16.8, "anhídrido de ácido benzoico": 29.3,
    "anhídrido ftálico": 21.4, "anhídrido propiónico": 22.3, "anilina": 37.5, "anisol": 33.5, "antraceno": 41.9,
    "antracita": 33.5, "antraquinona": 29.3, "arabinosa": 16.8, "asfalto": 40.4, "avellanas": 16.8, "azobenzol": 33.5,
    "azoxibenzol": 33.5, "azúcar": 16.8, "azúcar de caña": 16.8, "azufre": 8.4, "bambú, caña de": 16.8,
    "basuras orgánicas secas": 8.4, "benceno": 41.9, "bencilo": 33.5, "bencina": 41.9, "benzacetona": 33.5,
    "benzaldehído": 33.5, "benzidina": 33.5, "benzil": 33.5, "benzilamina": 37.5, "benzofenona": 33.5,
    "benzoina": 33.5, "benzol": 41.9, "bromuro de etilo": 7.6, "bromuro de metilo": 7.6, "butano": 46,
    "butanol": 33.5, "butano (gas)": 49.4, "cacao en polvo": 16.8, "café": 16.8, "cafeína": 20.9, "calcio": 40.2,
    "carbón briquetas de hulla": 33.5, "carbón coke de hulla": 29.3, "carbón de madera": 29.3, "carbón hulla": 33.5,
    "carbón lignita": 20.9, "carbón mineral": 25.1, "carburo de alúmina": 16.8, "carburo de aluminio": 16.8,
    "carne seca (charqui)": 25.1, "cartón": 16.8, "cartones bituminosos": 25.1, "caucho": 41.9,
    "caucho en planchas": 41.9, "caucho (neumáticos)": 25.1, "celuloide": 16.8, "celulosa": 17.6,
    "cera de parafina": 41.9, "cera mineral": 41.9, "ceras": 39.6, "cereales": 16.8, "cetanol": 41.9,
    "chocolate": 25.1, "cicloheptano": 46, "ciclohexano": 46, "ciclohexanol": 33.5, "ciclopentano": 46,
    "ciclopropano": 50.2, "cloroformo": 3.1, "cloropeno": 44.1, "cloruro de bencilo": 22.7, "cloruro de etilo": 18.9,
    "cloruro de metilo": 13.4, "cloruro de n-propilo": 23.9, "cloruro de polivinilo": 18.8, "coke": 33.5,
    "cola, engrudo": 37.5, "colodión": 16.8, "corcho": 16.8, "corcho (en placas)": 16.8, "corteza de roble": 16.8,
    "cresol": 33.5, "crotonaldehido": 33.5, "cuero": 18.6, "desechos de turba": 16.8, "diamitoléter": 41.9,
    "dicianuro": 20.9, "diclorobenzol": 16.8, "dietilamina": 41.9, "dietilcarbonato": 20.9, "dietilcetona": 33.5,
    "dietilester de ácido carbónico": 20.9, "dietilester de ácido malónico": 20.9, "dietileter de ácido oxálico": 20.9,
    "dietilmalonato": 20.9, "difenil": 41.9, "difenilamina": 37.8, "difeniletano": 41.9, "difenilo": 39.9,
    "dimetilamina": 18.5, "dimetil glicol": 16.8, "dinitro benceno": 16.8, "dipentano": 46, "estearina": 41.9,
    "estireno": 41.9, "etano": 50.2, "eter amílico": 41.9, "eter de petróleo": 41.9, "eter etilénico": 33.5,
    "eter etílico": 33.5, "eter metílico": 30, "etil amina": 34.4, "etil benceno": 41.2, "etileno": 50.2,
    "etilenglicol": 16.8, "extracto de malta": 12.6, "fenilhidracina": 31.3, "fenol": 33.5, "fenol, resina de": 25.1,
    "fenolacroleína": 33.5, "fibras de rafia, heno": 16.8, "fibras natulares": 16.8, "fósforo": 25.1, "furano": 25.1,
    "furfural": 23.5, "gas de alumbrado": 16.8, "gasolina": 47.3, "glicerina": 18, "goma dura": 33.6, "grafito": 31.5,
    "granos o gajos de uva": 16.8, "grasas": 41.9, "gutapercha": 46, "harina": 16.8, "hemetileno": 46,
    "heno comprimido": 16.8, "heno libre": 16.8, "heptano": 46, "hexametileno": 46, "hexano": 46,
    "hidrógeno": 142.3, "hidroquinona": 24.8, "hidróxido de magnesio": 16.8, "hidróxido de sodio": 8.4,
    "hidruro de aluminio": 20.9, "hidruro de magnesio": 16.8, "isobutano": 45.8, "isopentano": 45.4,
    "lana comprimida": 20.9, "lana de madera": 16.8, "lana natural": 22.8, "leche en polvo": 16.8,
    "libros y carpetas": 16.8, "lignito": 24.3, "lino": 16.8, "linóleo": 20.9, "madera de álamo": 16.8,
    "madera de coníferas": 16.8, "madera de contraplaca": 16.8, "madera de haya (helecho)": 20.9,
    "madera de hoguera (fuego)": 16.8, "madera de pino seco": 16.8, "madera de roble": 16.8,
    "madera dura exótica": 16.8, "magnesio": 25.1, "maicena": 16.8, "malta": 16.8, "malta, maíz": 16.8,
    "mantequilla": 37.8, "metracrilato de metilo": 25.5, "metano (gas)": 55.7, "metanol": 20.9,
    "metanol (alcohol metílico)": 20.9, "metilamina": 40.3, "metil butil cetona": 34.9, "metil etil cetona": 31.5,
    "metil propil cetona": 31.5, "monóxido de carbono": 8.4, "monóxido de carbono sulfurado": 8.4,
    "naftaleno": 39.1, "naftalina en cristales": 40.2, "nitrobenceno": 24.4, "nitrocelulosa": 8.4, "nitroetano": 16.4,
    "nitrometano": 10.5, "nueces, avellanas": 16.8, "nuez de coco": 20.9, "octano": 46, "oxido de carbono": 9.2,
    "oxido de etileno": 26.9, "paja natural": 14, "paja de madera": 16.8, "papel": 16.8, "parafina": 46,
    "pentano": 50.2, "pescado seco": 12.6, "petróleo": 41.9, "piperidina": 37.8, "placa de aglomerado de madera": 16.8,
    "poliamida": 29.3, "policarbonato": 29.3, "poliester": 25.1, "poliestierno": 40.2, "poliestireno en espuma": 41.9,
    "polietileno": 46.5, "poliformaldehido": 16.8, "poliisobutileno": 46,
    "poliisopropeno (goma natural sin vulcanizar)": 45.2, "polipropileno": 46, "politetrafluoretileno": 4.2,
    "poliuretano": 25.1, "polivinilo acetato": 20.9, "polyamida": 29.3, "propano": 50.2, "propileno": 45.8,
    "resina de cresol": 25.1, "resina de fenol": 25.1, "resina de urea": 12.6, "resina sintética": 41.9,
    "ron 75%": 20.9, "seda": 20.9, "seda de acetato": 16.8, "sisal": 16.8, "sodio": 4.2, "sulfito de carbonilo": 8.4,
    "sulfuro de carbono": 12.6, "tabaco": 16.8, "té": 16.8, "tejido de algodón": 16.7, "tetrahidrobenzol": 46,
    "tolueno": 42.3, "toluol": 41.9, "triacetato": 16.8, "tributilamina": 40.3, "trietilamina": 39.9,
    "trimetil amina": 37.8, "turba": 25.1, "turba seca y prensada": 16.7, "urea": 8.4, "xilol": 41.9
}

# Tabla Normativa OGUC
tabla_normativa = {
    1: [(8000, 24000, "aaaaa"), (4000, 16000, "baaaa"), (2000, 10000, "cbaaa"), (-1, -1, "dcbaa")],
    2: [(16000, 32000, "aaaaa"), (8000, 24000, "baaaa"), (4000, 16000, "cbaaa"), (2000, 10000, "ccbaa"), (1000, 6000, "dccba"), (500, 3500, "ddccb"), (-1, -1, "dddcc")],
    3: [(16000, 32000, "baaaa"), (8000, 24000, "bbaaa"), (4000, 16000, "cbbaa"), (2000, 10000, "ccbba"), (1000, 6000, "dccbb"), (-1, -1, "ddccb")],
    4: [(16000, 32000, "bbaaa"), (8000, 24000, "cbbaa"), (4000, 16000, "ccbba"), (2000, 10000, "dccbb"), (1000, 6000, "ddccb"), (500, 3500, "dddcc"), (-1, -1, "ddddc")]
}

# Elementos y Resistencia
elementos_construccion = {
    1: "Muros cortafuego", 2: "Muros zona vertical de seg. y caja escalera",
    3: "Muros caja ascensores", 4: "Muros divisorios entre unidades",
    5: "Elementos soportantes verticales", 6: "Muros no soportantes y tabiques",
    7: "Escaleras", 8: "Elementos soportantes horizontales",
    9: "Techumbre incluido techo falso"
}

tabla_resistencia = {
    'a': ["F-180", "F-120", "F-120", "F-120", "F-120", "F-30", "F-60", "F-120", "F-60"],
    'b': ["F-150", "F-120", "F-90",  "F-90",  "F-90",  "F-15", "F-30", "F-90",  "F-60"],
    'c': ["F-120", "F-90",  "F-60",  "F-60",  "F-60",  "-",    "F-15", "F-60",  "F-30"],
    'd': ["F-120", "F-60",  "F-60",  "F-60",  "F-30",  "-",    "-",    "F-30",  "F-15"]
}

# ==============================================================================
# FUNCIÓN DE GENERACIÓN DE PDF MEJORADA (CON TOTALES Y FIRMAS)
# ==============================================================================
class PDF(FPDF):
    def __init__(self, logo_path=None):
        super().__init__()
        self.logo_path = logo_path

    def header(self):
        # Insertar Logo si existe
        if self.logo_path:
            try:
                # x=10, y=10, w=25 (ajustamos tamaño y margen)
                self.image(self.logo_path, 10, 10, 25)
                # Mover el título a la derecha para que no choque con el logo
                self.set_xy(40, 10) 
            except Exception as e:
                print(f"Error cargando imagen: {e}")
                self.set_xy(10, 10) 

        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Memoria de Calculo - Carga Combustible', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        
        if self.logo_path:
            self.set_x(40)
            
        self.cell(0, 10, 'Segun NCh1916, NCh1993 y OGUC', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

def create_pdf(name_area, m2, destino_txt, pisos, dcm, dcpm, clas_final, letra_oguc, lista_media, lista_puntual, lista_resistencia, logo_path=None):
    # Pasamos el path del logo al constructor
    pdf = PDF(logo_path=logo_path)
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    def txt(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    # Sección 1: Datos Generales
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt("1. Datos Generales"), 0, 1)
    pdf.set_font("Arial", size=10)
    
    pdf.cell(50, 8, txt(f"Nombre del Área:"), 0, 0)
    pdf.cell(0, 8, txt(f"{name_area}"), 0, 1)
    pdf.cell(50, 8, txt(f"Superficie:"), 0, 0)
    pdf.cell(0, 8, txt(f"{m2} m2"), 0, 1)
    pdf.cell(50, 8, txt(f"Destino:"), 0, 0)
    # Usamos multi_cell para que si el nombre es muy largo, baje a la siguiente linea
    pdf.multi_cell(0, 8, txt(f"{destino_txt}"))
    
    pdf.cell(50, 8, txt(f"Número de Pisos:"), 0, 0)
    pdf.cell(0, 8, txt(f"{pisos}"), 0, 1)
    pdf.cell(50, 8, txt(f"Fecha de Emisión:"), 0, 0)
    pdf.cell(0, 8, txt(f"{datetime.date.today()}"), 0, 1)
    pdf.ln(5)

    # Sección 2: Resultados
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt("2. Resultados del Cálculo"), 0, 1)
    pdf.set_font("Arial", size=10)
    
    pdf.cell(80, 8, txt("Densidad de Carga Media (Dcm):"), 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, txt(f"{dcm:.2f} MJ/m2"), 0, 1)
    
    pdf.set_font("Arial", size=10)
    pdf.cell(80, 8, txt("Densidad de Carga Puntual (Dcpm):"), 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 8, txt(f"{dcpm:.2f} MJ/m2"), 0, 1)
    pdf.ln(5)

    # Sección 3: Clasificación
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt("3. Clasificación Normativa"), 0, 1)
    pdf.set_font("Arial", size=10)
    
    pdf.cell(80, 8, txt("Clasificación NCh 1993:"), 0, 0)
    pdf.cell(0, 8, txt(f"{clas_final}"), 0, 1)
    
    pdf.cell(80, 8, txt("Clasificación OGUC:"), 0, 0)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(0, 8, txt(f"CLASE {letra_oguc}"), 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # Sección 4: Materiales (Carga Media)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt("4. Detalle de Materiales (Carga Media)"), 0, 1)
    
    # Encabezado Tabla
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(80, 8, "Material", 1)
    pdf.cell(30, 8, "Calor (MJ/kg)", 1, 0, 'C')
    pdf.cell(30, 8, "Masa (kg)", 1, 0, 'C')
    pdf.cell(40, 8, "Total (MJ)", 1, 1, 'C')
    
    pdf.set_font("Arial", size=9)
    suma_mj_media = 0
    if lista_media:
        for item in lista_media:
            pdf.cell(80, 8, txt(item['Material'][:40]), 1)
            pdf.cell(30, 8, str(item['MJ/kg']), 1, 0, 'C')
            pdf.cell(30, 8, str(item['Kg']), 1, 0, 'C')
            pdf.cell(40, 8, str(item['Total MJ']), 1, 1, 'C')
            suma_mj_media += item['Total MJ']
        
        # --- TOTAL MEDIA ---
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(140, 8, txt("TOTAL ENERGIA ACUMULADA"), 1, 0, 'R')
        pdf.cell(40, 8, f"{suma_mj_media:.2f}", 1, 1, 'C')

    else:
        pdf.cell(180, 8, "No se ingresaron materiales", 1, 1, 'C')
    pdf.ln(5)

    # Sección 5: Materiales (Carga Puntual)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt("5. Detalle de Materiales (Carga Puntual Máxima - 4m2)"), 0, 1)
    
    # Encabezado Tabla
    pdf.set_font("Arial", 'B', 9)
    pdf.cell(80, 8, "Material", 1)
    pdf.cell(30, 8, "Calor (MJ/kg)", 1, 0, 'C')
    pdf.cell(30, 8, "Masa (kg)", 1, 0, 'C')
    pdf.cell(40, 8, "Total (MJ)", 1, 1, 'C')
    
    pdf.set_font("Arial", size=9)
    suma_mj_puntual = 0
    if lista_puntual:
        for item in lista_puntual:
            pdf.cell(80, 8, txt(item['Material'][:40]), 1)
            pdf.cell(30, 8, str(item['MJ/kg']), 1, 0, 'C')
            pdf.cell(30, 8, str(item['Kg']), 1, 0, 'C')
            pdf.cell(40, 8, str(item['Total MJ']), 1, 1, 'C')
            suma_mj_puntual += item['Total MJ']
            
        # --- TOTAL PUNTUAL ---
        pdf.set_font("Arial", 'B', 9)
        pdf.cell(140, 8, txt("TOTAL ENERGIA (en 4m2)"), 1, 0, 'R')
        pdf.cell(40, 8, f"{suma_mj_puntual:.2f}", 1, 1, 'C')
    else:
        pdf.cell(180, 8, "No se ingresaron materiales para carga puntual", 1, 1, 'C')
    pdf.ln(5)

    # Sección 6: Exigencias
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, txt("6. Exigencias de Resistencia al Fuego (OGUC)"), 0, 1)
    pdf.set_font("Arial", 'B', 9)

    pdf.cell(10, 8, "#", 1, 0, 'C')
    pdf.cell(140, 8, txt("Elemento de Construcción"), 1)
    pdf.cell(30, 8, "Resistencia", 1, 1, 'C')

    pdf.set_font("Arial", size=9)
    idx = 1
    for row in lista_resistencia:
        pdf.cell(10, 8, str(idx), 1, 0, 'C')
        pdf.cell(140, 8, txt(row['Elemento']), 1)
        pdf.cell(30, 8, txt(row['Resistencia Exigida']), 1, 1, 'C')
        idx += 1
    
    # --- FIRMAS ---
    pdf.ln(30)
    
    # Verificar si necesitamos una pagina nueva para las firmas
    y_actual = pdf.get_y()
    if y_actual > 240: 
        pdf.add_page()
        y_actual = 40
        
    pdf.line(30, y_actual, 90, y_actual)
    pdf.line(120, y_actual, 180, y_actual)
    
    pdf.set_xy(30, y_actual + 2)
    pdf.cell(60, 5, txt("Elaborado por"), 0, 0, 'C')
    
    pdf.set_xy(120, y_actual + 2)
    pdf.cell(60, 5, txt("Aprobado por"), 0, 0, 'C')

    return pdf.output(dest='S').encode('latin-1')

# ==============================================================================
# LÓGICA DE ESTADO
# ==============================================================================
if 'lista_media' not in st.session_state:
    st.session_state.lista_media = []
if 'lista_puntual' not in st.session_state:
    st.session_state.lista_puntual = []

# ==============================================================================
# BARRA LATERAL (Con Upload de Logo)
# ==============================================================================
with st.sidebar:
    st.header("🏢 Datos del Edificio")
    name_area = st.text_input("Nombre de área a evaluar:", "Bodega Principal")
    
    # --- CORRECCIÓN DE NOMBRE LARGO ---
    opciones_destino = {
        1: "1. Combustibles, lubricantes, aceites minerales y naturales",
        2: "2. Establecimientos industriales",
        3: "3. Supermercados y Centros Comerciales",
        4: "4. Establecimientos de bodegaje"
    }
    destino_val = st.selectbox("Destino del edificio:", options=list(opciones_destino.keys()), format_func=lambda x: opciones_destino[x])
    destino_str = opciones_destino[destino_val]
    
    cant_pisos = st.number_input("Número de pisos:", min_value=1, step=1, value=1)
    
    st.subheader("Dimensiones")
    largo = st.number_input("Largo (m):", min_value=0.1, value=10.0)
    ancho = st.number_input("Ancho (m):", min_value=0.1, value=10.0)
    m2 = largo * ancho
    st.info(f"Área Total: **{m2:.2f} m²**")
    
    st.divider()
    st.subheader("🖼️ Logo del Reporte")
    uploaded_logo = st.file_uploader("Subir imagen (PNG/JPG)", type=['png', 'jpg', 'jpeg'])

# ==============================================================================
# PESTAÑAS PRINCIPALES
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["1. Carga Combustible Media", "2. Carga Puntual Máxima (4m²)", "3. Resultados e Informe"])

# --- TAB 1: CARGA MEDIA ---
with tab1:
    st.subheader("Ingreso de materiales (Carga Media)")
    col1, col2 = st.columns([3, 1])
    with col1:
        material_seleccionado = st.selectbox("Seleccione material:", sorted(calor_comb.keys()), key="mat_media")
    with col2:
        cantidad_input = st.number_input("Cantidad (kg):", min_value=0.0, step=1.0, key="cant_media")
    
    if st.button("Agregar Material (Media)"):
        if cantidad_input > 0:
            mj_val = calor_comb[material_seleccionado]
            total_mj = round(mj_val * cantidad_input, 3)
            st.session_state.lista_media.append({
                "Material": material_seleccionado, "MJ/kg": mj_val, "Kg": cantidad_input, "Total MJ": total_mj
            })
            st.success(f"Agregado: {material_seleccionado}")
        else:
            st.warning("Cantidad debe ser > 0")

    if st.session_state.lista_media:
        df_media = pd.DataFrame(st.session_state.lista_media)
        st.dataframe(df_media, use_container_width=True)
        suma_total_media = df_media["Total MJ"].sum()
        if st.button("Borrar último (Media)"):
            st.session_state.lista_media.pop()
            st.rerun()
        Dcm = suma_total_media / m2
        st.metric("Densidad Carga Media (Dcm)", f"{Dcm:.3f} MJ/m²")
    else:
        Dcm = 0
        st.info("Sin datos.")

# --- TAB 2: CARGA PUNTUAL ---
with tab2:
    st.subheader("Ingreso de materiales (Carga Puntual - 4m²)")
    col1, col2 = st.columns([3, 1])
    with col1:
        material_puntual = st.selectbox("Seleccione material:", sorted(calor_comb.keys()), key="mat_puntual")
    with col2:
        cantidad_puntual = st.number_input("Cantidad (kg):", min_value=0.0, step=1.0, key="cant_puntual")
    
    if st.button("Agregar Material (Puntual)"):
        if cantidad_puntual > 0:
            mj_val = calor_comb[material_puntual]
            total_mj = round(mj_val * cantidad_puntual, 3)
            st.session_state.lista_puntual.append({
                "Material": material_puntual, "MJ/kg": mj_val, "Kg": cantidad_puntual, "Total MJ": total_mj
            })
            st.success(f"Agregado: {material_puntual}")

    if st.session_state.lista_puntual:
        df_puntual = pd.DataFrame(st.session_state.lista_puntual)
        st.dataframe(df_puntual, use_container_width=True)
        suma_total_puntual = df_puntual["Total MJ"].sum()
        if st.button("Borrar último (Puntual)"):
            st.session_state.lista_puntual.pop()
            st.rerun()
        Dcpm = round(suma_total_puntual / 4, 3)
        st.metric("Densidad Carga Puntual (Dcpm)", f"{Dcpm:.3f} MJ/m²")
    else:
        Dcpm = 0
        st.info("Sin datos.")

# --- TAB 3: RESULTADOS Y PDF ---
with tab3:
    st.header("Resultados de la Evaluación")
    
    if st.button("Calcular Clasificación Final", type="primary"):
        # Funciones de clasificación
        def clasificar_media(valor):
            if valor <= 500: return "DC1"
            elif valor <= 1000: return "DC2"
            elif valor <= 2000: return "DC3"
            elif valor <= 4000: return "DC4"
            elif valor <= 8000: return "DC5"
            elif valor <= 16000: return "DC6"
            else: return "DC7"

        def clasificar_puntual(valor):
            if valor <= 3500: return "DC1"
            elif valor <= 6000: return "DC2"
            elif valor <= 10000: return "DC3"
            elif valor <= 16000: return "DC4"
            elif valor <= 24000: return "DC5"
            elif valor <= 32000: return "DC6"
            else: return "DC7"

        clas_media = clasificar_media(Dcm)
        clas_puntual = clasificar_puntual(Dcpm)
        
        prioridad = {"DC1": 1, "DC2": 2, "DC3": 3, "DC4": 4, "DC5": 5, "DC6": 6, "DC7": 7}
        mas_restrictiva = clas_media if prioridad[clas_media] > prioridad[clas_puntual] else clas_puntual

        if destino_val in tabla_normativa:
            filas = tabla_normativa[destino_val]
            idx_media = len(filas) - 1
            for i, (lim_m, _, _) in enumerate(filas):
                if Dcm > lim_m: idx_media = i; break
            
            idx_puntual = len(filas) - 1
            for i, (_, lim_p, _) in enumerate(filas):
                if Dcpm > lim_p: idx_puntual = i; break
            
            idx_final = min(idx_media, idx_puntual)
            fila_datos = filas[idx_final]
            letra_resultado = fila_datos[2][min(int(cant_pisos)-1, 4) if int(cant_pisos)-1 >=0 else 0]
            letra_upper = letra_resultado.upper()
            
            # MOSTRAR RESULTADOS
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.info(f"📍 Área: {name_area} ({m2} m²)")
                st.write(f"**Dcm:** {Dcm:.2f} MJ/m² ({clas_media})")
                st.write(f"**Dcpm:** {Dcpm:.2f} MJ/m² ({clas_puntual})")
                st.write(f"**Clasificación NCh1993:** {mas_restrictiva}")
            with col_res2:
                st.success(f"📌 CLASIFICACIÓN OGUC: CLASE {letra_upper}")
            
            st.divider()
            
            clave_letra = letra_resultado.lower()
            data_res = []
            if clave_letra in tabla_resistencia:
                resistencias = tabla_resistencia[clave_letra]
                for i in range(1, 10):
                    data_res.append({"Elemento": elementos_construccion[i], "Resistencia Exigida": resistencias[i-1]})
                st.table(pd.DataFrame(data_res))
            
            # --- GENERACIÓN DE PDF ---
            st.write("---")
            st.subheader("📄 Generar Reporte")
            
            # Manejo del Logo temporal CORRECTO
            logo_path_temp = None
            if uploaded_logo is not None:
                # Obtenemos extension (.jpg, .png)
                ext = os.path.splitext(uploaded_logo.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
                    tmp_file.write(uploaded_logo.getvalue())
                    logo_path_temp = tmp_file.name
            
            pdf_bytes = create_pdf(
                name_area, m2, destino_str, cant_pisos, Dcm, Dcpm, mas_restrictiva, letra_upper,
                st.session_state.lista_media, st.session_state.lista_puntual, data_res, logo_path_temp
            )
            
            # Borrar temp
            if logo_path_temp:
                try: os.remove(logo_path_temp)
                except: pass
            
            st.download_button(
                label="⬇️ Descargar Memoria de Cálculo (PDF)",
                data=pdf_bytes,
                file_name=f"Memoria_{name_area}.pdf",
                mime="application/pdf"
            )

        else:
            st.error("Error en selección de destino.")
            
    st.markdown("---")
    url_minvu = "https://www.minvu.gob.cl/wp-content/uploads/2025/02/Listado-Oficial-de-Comportamiento-al-Fuego-de-Elementos-y-Componentes-de-la-Construccion_-ED17-2025.pdf"
    st.link_button("📄 Ver Listado Oficial (MINVU)", url_minvu)