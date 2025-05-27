import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random
import json
import seaborn as sns
import matplotlib.patches as mpatches
import matplotlib as mpl

# Configuración de la página
st.set_page_config(
    page_title="GraphMind - IA & Grafos",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 20px;
        padding: 10px 25px;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    .stTextArea>div>div>textarea {
        border-radius: 10px;
    }
    .css-1d391kg {
        padding: 2rem 1rem;
    }
    h1 {
        color: #2c3e50;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 2rem !important;
    }
    h2 {
        color: #34495e;
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        margin-top: 2rem !important;
    }
    h3 {
        color: #2c3e50;
        font-size: 1.4rem !important;
        font-weight: 500 !important;
    }
    .stAlert {
        border-radius: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
    }
    </style>
    """, unsafe_allow_html=True)

# Configurar la API de Gemini
GEMINI_API_KEY = 'AIzaSyDxJ1EQDwHIkBfRhY28q9FdCS2wC7_NMQk'
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# Título principal con emoji y estilo
st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🧠 GraphMind - Inteligencia Artificial & Grafos</h1>
        <p style='font-size: 1.2rem; color: #666;'>
            Explora la teoría de grafos con el poder de la IA
        </p>
    </div>
""", unsafe_allow_html=True)

# Sidebar con estilo mejorado
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h2 style='color: white;'>Opciones</h2>
        </div>
    """, unsafe_allow_html=True)
    
    opcion = st.selectbox(
        "Selecciona una operación:",
        ["Crear Grafo", "Añadir Nodo", "Añadir Arista", "Propiedades del Grafo", "Algoritmos", 
         "Análisis con IA", "Generar desde Descripción", "Predecir Evolución", "Historia del Grafo"]
    )

# Crear un grafo
def crear_grafo():
    G = nx.Graph()
    return G

# Función para visualizar el grafo con estilo mejorado
def visualizar_grafo(G):
    # Paleta suave y minimalista
    palette = sns.color_palette("pastel", len(G.nodes()))
    node_colors = palette
    edge_colors = sns.color_palette("crest", len(G.edges()))
    
    # Crear la figura
    fig, ax = plt.subplots(figsize=(13, 9))
    ax.set_facecolor('#fcfcfc')
    fig.patch.set_facecolor('#fcfcfc')
    
    # Mejor distribución
    pos = nx.spring_layout(G, k=2.5, iterations=200, seed=42)
    
    # Dibujar aristas más delgadas y suaves
    for i, (u, v) in enumerate(G.edges()):
        nx.draw_networkx_edges(
            G, pos,
            edgelist=[(u, v)],
            width=1.8,
            alpha=0.35,
            edge_color=[edge_colors[i]],
            style='solid',
            ax=ax,
            connectionstyle='arc3,rad=0.12'
        )
    
    # Nodos más pequeños, con borde blanco y leve sombra
    for i, (nodo, (x, y)) in enumerate(pos.items()):
        circ = mpatches.Circle((x, y), 0.06, color=node_colors[i], ec='white', lw=2.5, zorder=2, alpha=0.95)
        ax.add_patch(circ)
        # Sombra sutil
        shadow = mpatches.Circle((x+0.008, y-0.008), 0.06, color='#bbb', alpha=0.10, zorder=1)
        ax.add_patch(shadow)
    
    # Etiquetas minimalistas, cerca del nodo, sin fondo ni borde
    for i, (nodo, (x, y)) in enumerate(pos.items()):
        ax.text(x, y+0.08, str(nodo), fontsize=13, fontweight='medium', ha='center', va='center',
                color='#222', zorder=3, alpha=0.85)
    
    # Eliminar leyenda y título
    # Márgenes y ejes
    plt.margins(0.18)
    plt.axis('off')
    plt.tight_layout()
    return plt

# Función para analizar el grafo con IA
def analizar_grafo_ia(G):
    nodos = list(G.nodes())
    aristas = list(G.edges())
    descripcion = f"Grafo con {len(nodos)} nodos y {len(aristas)} aristas. Nodos: {nodos}. Aristas: {aristas}"
    
    prompt = f"""
    Analiza este grafo y proporciona:
    1. Un resumen de su estructura
    2. Posibles aplicaciones prácticas
    3. Sugerencias de algoritmos que podrían ser útiles
    
    Grafo: {descripcion}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al analizar el grafo: {str(e)}"

# Nueva función: Generar grafo desde descripción
def generar_grafo_desde_descripcion(descripcion):
    prompt = f"""
    Basado en esta descripción, sugiere una estructura de grafo en formato JSON con nodos y aristas.
    La respuesta debe ser solo el JSON, sin texto adicional.
    Formato: {{"nodos": ["nodo1", "nodo2", ...], "aristas": [["nodo1", "nodo2"], ...]}}
    
    Descripción: {descripcion}
    """
    
    try:
        response = model.generate_content(prompt)
        # Procesar la respuesta JSON
        try:
            # Limpiar la respuesta para obtener solo el JSON
            json_str = response.text.strip()
            if json_str.startswith('```json'):
                json_str = json_str[7:]
            if json_str.endswith('```'):
                json_str = json_str[:-3]
            json_str = json_str.strip()
            
            # Parsear el JSON
            grafo_data = json.loads(json_str)
            
            # Crear nuevo grafo
            nuevo_grafo = nx.Graph()
            
            # Añadir nodos
            for nodo in grafo_data['nodos']:
                nuevo_grafo.add_node(nodo)
            
            # Añadir aristas
            for arista in grafo_data['aristas']:
                nuevo_grafo.add_edge(arista[0], arista[1])
            
            # Actualizar el grafo en la sesión
            st.session_state.grafo = nuevo_grafo
            
            return "Grafo generado exitosamente. ¡Mira la visualización abajo!"
        except json.JSONDecodeError:
            return "Error al procesar la respuesta JSON. Respuesta recibida: " + response.text
    except Exception as e:
        return f"Error al generar el grafo: {str(e)}"

# Nueva función: Predecir evolución del grafo
def predecir_evolucion_grafo(G):
    nodos = list(G.nodes())
    aristas = list(G.edges())
    descripcion = f"Grafo actual con {len(nodos)} nodos y {len(aristas)} aristas. Nodos: {nodos}. Aristas: {aristas}"
    
    prompt = f"""
    Basado en este grafo, predice:
    1. Qué nodos podrían ser importantes en el futuro
    2. Qué nuevas conexiones podrían ser beneficiosas
    3. Qué patrones podrían emerger
    
    Grafo: {descripcion}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al predecir evolución: {str(e)}"

# Nueva función: Generar historia del grafo
def generar_historia_grafo(G):
    nodos = list(G.nodes())
    aristas = list(G.edges())
    
    prompt = f"""
    Crea una historia corta y creativa sobre este grafo, donde:
    1. Los nodos son personajes o lugares
    2. Las aristas son relaciones o conexiones
    3. La historia debe ser coherente y entretenida
    
    Grafo: Nodos: {nodos}, Aristas: {aristas}
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error al generar historia: {str(e)}"

# Inicializar el grafo en la sesión
if 'grafo' not in st.session_state:
    st.session_state.grafo = crear_grafo()

# Contenedor principal con estilo
with st.container():
    if opcion == "Crear Grafo":
        st.markdown("### 📊 Crear Nuevo Grafo")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            if st.button("Crear Grafo Vacío", key="crear_grafo"):
                st.session_state.grafo = crear_grafo()
                st.success("¡Grafo creado exitosamente! 🎉")

    elif opcion == "Añadir Nodo":
        st.markdown("### ➕ Añadir Nodo")
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            nuevo_nodo = st.text_input("Nombre del nodo:", key="nuevo_nodo")
            if st.button("Añadir Nodo", key="añadir_nodo"):
                if nuevo_nodo:
                    st.session_state.grafo.add_node(nuevo_nodo)
                    st.success(f"✨ Nodo '{nuevo_nodo}' añadido exitosamente!")

    elif opcion == "Añadir Arista":
        st.markdown("### 🔗 Añadir Arista")
        col1, col2 = st.columns(2)
        with col1:
            nodo1 = st.text_input("Primer nodo:", key="nodo1")
        with col2:
            nodo2 = st.text_input("Segundo nodo:", key="nodo2")
        if st.button("Añadir Arista", key="añadir_arista"):
            if nodo1 and nodo2:
                st.session_state.grafo.add_edge(nodo1, nodo2)
                st.success(f"✨ Arista entre '{nodo1}' y '{nodo2}' añadida exitosamente!")

    elif opcion == "Propiedades del Grafo":
        st.markdown("### 📈 Propiedades del Grafo")
        if st.session_state.grafo.number_of_nodes() > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Número de nodos", st.session_state.grafo.number_of_nodes())
                st.metric("Número de aristas", st.session_state.grafo.number_of_edges())
            with col2:
                st.markdown("### Grados de los nodos")
                for nodo in st.session_state.grafo.nodes():
                    st.markdown(f"- **{nodo}**: {st.session_state.grafo.degree(nodo)}")
        else:
            st.warning("⚠️ El grafo está vacío. Añade algunos nodos y aristas primero.")

    elif opcion == "Algoritmos":
        st.markdown("### 🔍 Algoritmos de Grafos")
        algoritmo = st.selectbox(
            "Selecciona un algoritmo:",
            ["Camino más corto", "Recorrido en profundidad", "Recorrido en anchura"]
        )
        
        if algoritmo == "Camino más corto":
            col1, col2 = st.columns(2)
            with col1:
                inicio = st.text_input("Nodo inicial:", key="inicio")
            with col2:
                fin = st.text_input("Nodo final:", key="fin")
            if st.button("Calcular camino más corto", key="calcular_camino"):
                if inicio and fin and inicio in st.session_state.grafo and fin in st.session_state.grafo:
                    try:
                        camino = nx.shortest_path(st.session_state.grafo, inicio, fin)
                        st.success(f"🎯 Camino más corto: {' → '.join(camino)}")
                    except nx.NetworkXNoPath:
                        st.error("❌ No existe un camino entre los nodos seleccionados.")
                else:
                    st.error("❌ Por favor, selecciona nodos válidos que existan en el grafo.")

    elif opcion == "Análisis con IA":
        st.markdown("### 🤖 Análisis del Grafo con IA")
        if st.session_state.grafo.number_of_nodes() > 0:
            if st.button("Analizar Grafo", key="analizar_grafo"):
                with st.spinner("🧠 Analizando el grafo con IA..."):
                    analisis = analizar_grafo_ia(st.session_state.grafo)
                    st.markdown("### 📊 Análisis de IA")
                    st.write(analisis)
        else:
            st.warning("⚠️ El grafo está vacío. Añade algunos nodos y aristas primero.")

    elif opcion == "Generar desde Descripción":
        st.markdown("### 🎨 Generar Grafo desde Descripción")
        descripcion = st.text_area(
            "Describe el tipo de grafo que quieres generar:",
            "Por ejemplo: 'Un grafo que represente una red social de amigos'",
            height=100
        )
        if st.button("Generar Grafo", key="generar_grafo"):
            with st.spinner("🎨 Generando grafo con IA..."):
                resultado = generar_grafo_desde_descripcion(descripcion)
                st.markdown("### ✨ Resultado")
                st.write(resultado)

    elif opcion == "Predecir Evolución":
        st.markdown("### 🔮 Predecir Evolución del Grafo")
        if st.session_state.grafo.number_of_nodes() > 0:
            if st.button("Predecir Evolución", key="predecir_evolucion"):
                with st.spinner("🔮 Analizando posibles evoluciones..."):
                    prediccion = predecir_evolucion_grafo(st.session_state.grafo)
                    st.markdown("### 📈 Predicción de Evolución")
                    st.write(prediccion)
        else:
            st.warning("⚠️ El grafo está vacío. Añade algunos nodos y aristas primero.")

    elif opcion == "Historia del Grafo":
        st.markdown("### 📚 Historia del Grafo")
        if st.session_state.grafo.number_of_nodes() > 0:
            if st.button("Generar Historia", key="generar_historia"):
                with st.spinner("📝 Creando una historia creativa..."):
                    historia = generar_historia_grafo(st.session_state.grafo)
                    st.markdown("### 📖 Historia Generada")
                    st.write(historia)
        else:
            st.warning("⚠️ El grafo está vacío. Añade algunos nodos y aristas primero.")

# Visualización del grafo con estilo mejorado
st.markdown("### 📊 Visualización del Grafo")
if st.session_state.grafo.number_of_nodes() > 0:
    fig = visualizar_grafo(st.session_state.grafo)
    st.pyplot(fig)
else:
    st.info("ℹ️ El grafo está vacío. Usa las opciones del menú para añadir nodos y aristas.") 