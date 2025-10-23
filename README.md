# catalogo_peliculas_proyecto_final_grupal

# 🎬 Proyecto Final — Catálogo de Películas (POO · Introducción a Python · ADA)

El objetivo es desarrollar un programa que permita **llevar un registro de películas** aplicando **programación orientada a objetos** (POO).

## ✅ Requerimientos del enunciado (checklist)
- [x] Entrega mediante **repositorio en GitHub** con **≥ 3 commits**.
- [x] **Archivo .txt por catálogo** donde se guardan las películas.
- [x] **POO** con:
  - `Pelicula` (uno de sus atributos es **privado**).
  - `CatalogoPeliculas` (atributos `nombre`, `ruta_archivo`; métodos `agregar`, `listar`, `eliminar`).
- [x] **Menú** con opciones: Agregar, Listar, Eliminar catálogo, Salir.
- [x] **≥ 2 archivos .py**.

## 🗂️ Estructura
catalogo_peliculas/
├─ app.py
├─ catalogo_peliculas.py
├─ pelicula.py
└─ catalogos/ # se crea automáticamente; guarda los .txt


## 🚀 Cómo ejecutar
    1. Asegurate de tener **Python 3.10+**.
    2. Abrí una terminal en la carpeta del proyecto.
    3. Ejecutá:
         ```bash
         python app.py
    4.Ingresá el nombre del catálogo (se creará catalogos/<nombre>.txt si no existe).
    5.Usá el menú para agregar/listar/eliminar.

🧩 Detalles de implementación

    Pelicula guarda el nombre con un atributo privado __nombre y lo expone con una propiedad de solo lectura.

    CatalogoPeliculas maneja la persistencia en archivo .txt (una película por línea).

    El menú valida entradas básicas y confirma antes de eliminar el archivo.

🧪 Sugerencia de pruebas manuales

    1-Crear catálogo mis_pelis, agregar 2–3 títulos, listar.

    2-Cerrar y volver a abrir el programa, listar mis_pelis para verificar persistencia.

    3-Eliminar el catálogo y comprobar que el archivo ya no existe.