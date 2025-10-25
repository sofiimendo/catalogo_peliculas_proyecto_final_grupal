<div align="center">

# 🎬✨ Catálogo de Películas
### Proyecto Final — Introducción a Python (ADA)
👩‍💻 *So + Thel + Yami Edition*

---

![Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)
![ADA](https://img.shields.io/badge/ADA-Women%20in%20Tech-pink?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-Finalizado-success?style=for-the-badge)

</div>

---

## 💡 Descripción del Proyecto

El objetivo del trabajo final fue desarrollar un **programa que permita gestionar catálogos de películas**, aplicando los principales conceptos de **Programación Orientada a Objetos (POO)** aprendidos durante el curso.

Este proyecto incluye **dos modos de ejecución**:
- 🎞️ **Versión por consola** (archivo `app.py`)
- 💻 **Versión gráfica** desarrollada con **Flet** (archivo `gui_flet.py`)

Ambas versiones comparten la misma lógica de negocio y clases internas (`Film`, `Pelicula`, `CatalogoPeliculas`, `utils`).

---

## 🧠 Conceptos Aplicados

| Concepto | Implementación |
|-----------|----------------|
| **POO (Clases y Objetos)** | Clases `Film`, `Pelicula` y `CatalogoPeliculas` |
| **Atributos privados** | En la clase `Film`: atributo `__nombre` |
| **Herencia** | `Pelicula` hereda de `Film` |
| **Decoradores** | En `utils.py`: decoradores de log y medición de tiempo |
| **Funciones lambda** | Normalización de texto y transformaciones de strings |
| **Generadores** | Iteración eficiente de líneas en los catálogos `.txt` |
| **Persistencia de datos** | Archivos `.txt` por catálogo (lectura/escritura) |
| **Interfaz gráfica (Flet)** | Permite manipular catálogos visualmente |

---

## 🗂️ Estructura del Proyecto

```bash
📂 catalogo_peliculas_proyecto_final_grupal
│
├── 🧭 app.py                  → versión de consola (menús e interacción)
├── 💅 gui_flet.py             → interfaz gráfica creada con Flet
├── 📚 catalogo_peliculas.py   → clase para crear, listar y eliminar películas
├── 🎞️ pelicula.py             → clases Film (base) y Pelicula (heredada)
├── 🪄 utils.py                → decoradores, lambdas y utilidades
├── 🎬 main.py                 → archivo principal de ejecución
│
├── 🗂️ catalogos/              → catálogos generados automáticamente
│   ├── infantiles.txt
│   ├── favoritas.txt
│   ├── acciones.log
│   └── tiempos.log
│
├── 👩‍💻 integrantes.txt        → lista de integrantes del grupo
└── 🪶 README.md               → documentación del proyecto

## 🚀 Ejecución

##💻 Modo gráfico (Flet)

1️⃣ Instalar dependencias:
    ```bash
    python -m pip install flet
    ````

2️⃣ Ejecutar la versión gráfica:
    ```bash
    python gui_flet.py
    ```
Se abrirá una ventana con una interfaz amigable para crear, listar y gestionar catálogos de películas.

##🎞️ Modo consola

1️⃣ Ejecutar el programa principal:

python main.py


2️⃣ Seguir las opciones del menú:

1) Crear catálogo nuevo
2) Ver catálogos existentes
3) Trabajar con un catálogo
4) Eliminar un catálogo
5) Salir

##🧩 Funcionamiento General

Cada catálogo se guarda como un archivo .txt dentro de la carpeta catalogos/.

El nombre del catálogo define el género (por ejemplo, “Infantiles”, “Acción”, “Románticas”).

Al agregar una película, solo se solicita el título y año opcional.

Las películas se listan de forma ordenada y pueden eliminarse individualmente.

Los decoradores registran acciones y tiempos de ejecución en archivos .log.

##🎨 Interfaz Flet
Fu
ncionalidades principales:

Crear nuevos catálogos.

Seleccionar catálogos existentes.

Agregar películas (título + año).

Eliminar una o varias películas.

Mostrar los datos actualizados al instante.

Vista general:

| Elemento                     | Descripción                           |
| ---------------------------- | ------------------------------------- |
| 🔽 *Dropdown*                | Selecciona el catálogo activo         |
| ➕ *Botón Crear catálogo*    | Genera un nuevo archivo `.txt`        |
| 🎥 *Botón Agregar*           | Añade una película al catálogo actual |
| 🗑️ *Eliminar seleccionadas*  | Quita películas marcadas de la tabla  |
| 🔄 *Refrescar*               | Actualiza la lista de catálogos       |

##🧪 Pruebas recomendadas

1️⃣ Crear catálogo "Infantiles"
2️⃣ Agregar varias películas con distintos años
3️⃣ Cerrar y volver a abrir para verificar persistencia
4️⃣ Eliminar una película y confirmar actualización
5️⃣ Revisar logs generados en catalogos/acciones.log y catalogos/tiempos.log

##👩‍💻 Integrantes

| Nombre
| --------------------------
| **Sofía Macarena Mendoza**
| **Thelma D. Teileche**
| **Yamila Valdez Aguilar**

## ❤️ Créditos

Proyecto desarrollado en el marco del curso **Introducción a Python — ADA ITW (2025)**, con la guía del **Prof. Enrique Delgado**.

> “Gracias por acompañarnos en cada paso de este proceso de aprendizaje.”

👩‍💻 *So + Thel + Yami*

