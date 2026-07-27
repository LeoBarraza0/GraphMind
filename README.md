# GraphMind - IA & Grafos

Esta es una aplicación web interactiva para trabajar con grafos, analizar su estructura y aplicar Algoritmos e Inteligencia Artificial usando la API de Gemini.

## Características

- Creación y visualización interactiva de grafos.
- Añadir nodos y aristas.
- Cálculo de propiedades del grafo (nodos, aristas, grados).
- Algoritmos de grafos (Camino más corto, recorrido, etc.).
- Integración con IA (Análisis de estructura, generación desde descripción, predicción de evolución e historias).

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Clona este repositorio o descarga los archivos:
```bash
git clone https://github.com/LeoBarraza0/GraphMind.git
cd GraphMind
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Configura tu variable de entorno:
   - Crea un archivo `.env` basado en `.env.example`.
   - Agrega tu clave de API de Gemini:
```env
GEMINI_API_KEY=tu_api_key_aqui
```

## Uso

1. Ejecuta la aplicación:
```bash
streamlit run app.py
```

2. Abre tu navegador web en la dirección que se muestra en la terminal (generalmente http://localhost:8501).

## Licencia

Este proyecto está bajo la Licencia MIT.