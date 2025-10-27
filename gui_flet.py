# gui_flet.py 
import os
import flet as ft
from pelicula import Pelicula
from catalogo_peliculas import CatalogoPeliculas
from utils import BASE_DIR_CATALOGOS, normalizar_espacios

# ===================== helpers de archivos =====================

def listar_catalogos() -> list[str]:
    if not os.path.exists(BASE_DIR_CATALOGOS):
        os.makedirs(BASE_DIR_CATALOGOS, exist_ok=True)
        return []
    return sorted(
        [f[:-4] for f in os.listdir(BASE_DIR_CATALOGOS) if f.endswith(".txt")],
        key=str.lower,
    )

def ruta_catalogo(nombre: str) -> str:
    return os.path.join(BASE_DIR_CATALOGOS, f"{nombre}.txt")

def reescribir_catalogo(catalogo: CatalogoPeliculas, peliculas: list[Pelicula]) -> None:
    with open(catalogo.ruta_archivo, "w", encoding="utf-8") as f:
        for p in peliculas:
            f.write(p.to_line() + "\n")

# ===================== UI principal =====================

PALETTE = {
    "bg": "#FAF7FB",           # fondo general
    "panel": "#FFFFFF",        # tarjetas y paneles
    "accent": "#EC407A",       # rosa fuerte
    "accent_soft": "#F8BBD0",  # rosa pastel
    "mint": "#E0F7FA",
    "lav": "#EDE7F6",
    "text": "#37474F",
    "muted": "#7A8084",
    "shadow": "#00000020",
}

def chip(texto: str, color_bg: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(texto, size=11, weight=ft.FontWeight.W_600, color=PALETTE["text"]),
        padding=ft.padding.symmetric(6, 8),
        bgcolor=color_bg,
        border_radius=16,
    )

def make_toast(page: ft.Page, msg: str, ok: bool = True):
    bg = "#B9F6CA" if ok else "#FF8A80"
    page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor=bg, show_close_icon=True)
    page.snack_bar.open = True
    page.update()

def main(page: ft.Page):
    # ---------- page setup ----------
    page.title = "Catálogo de Películas — So · Thel · Yami"
    page.bgcolor = PALETTE["bg"]
    page.padding = 0
    page.window_width = 1080
    page.window_height = 720
    page.scroll = "auto"

    # ---------- estado ----------
    seleccionadas_keys: set[str] = set()  # para selección múltiple
    grid = ft.GridView(
        expand=True,
        runs_count=4,              # cuántas columnas aprox (se adapta)
        max_extent=None,           # usar runs_count
        child_aspect_ratio=1.6,    # ancho/alto de cada tarjeta
        spacing=14,
        run_spacing=14,
        padding=16,
    )

    def peli_key(p: Pelicula) -> str:
        return f"{p.nombre}|{getattr(p, 'anio', 0)}"

    # ---------- header "hero" ----------
    hero = ft.Container(
        padding=ft.padding.symmetric(18, 20),
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#FFE3EC", "#E8F7FF", "#F3E8FF"],   # pastel
        ),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Column(
                    spacing=2,
                    controls=[
                        ft.Text("Catálogo de Películas", size=24, weight=ft.FontWeight.W_700, color=PALETTE["text"]),
                        ft.Text("Proyecto Final · ADA", size=12, color=PALETTE["muted"]),
                    ],
                ),
                chip("So + Thel + Yami", PALETTE["mint"]),
            ],
        ),
    )

    # ---------- panel lateral (catálogos) ----------
    catalogos = listar_catalogos()
    dd_catalogo = ft.Dropdown(
        label="Catálogo",
        hint_text="Elegí un catálogo…",
        options=[ft.dropdown.Option(c) for c in catalogos],
        width=280,
    )
    btn_refresh = ft.IconButton(icon="refresh")
    tf_new_cat = ft.TextField(label="Nuevo catálogo", width=220, bgcolor=PALETTE["panel"])
    btn_crear_cat = ft.ElevatedButton("Crear", icon="add", bgcolor=PALETTE["accent"], color="white")

    # inputs película (género se deriva del catálogo)
    tf_titulo = ft.TextField(label="Título", width=280, bgcolor=PALETTE["panel"])
    tf_anio = ft.TextField(label="Año (opcional)", width=130, bgcolor=PALETTE["panel"])
    btn_add = ft.FilledButton("Agregar", icon="movie", bgcolor=PALETTE["accent"], color="white")

    btn_delete_sel = ft.OutlinedButton("Eliminar seleccionadas", icon="delete_outline")

    info_label = ft.Text("", size=12, color=PALETTE["muted"])

    side_panel = ft.Container(
        width=340,
        bgcolor=PALETTE["panel"],
        padding=16,
        border_radius=20,
        shadow=ft.BoxShadow(blur_radius=16, color=PALETTE["shadow"]),
        content=ft.Column(
            spacing=14,
            controls=[
                ft.Row([dd_catalogo, btn_refresh], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([tf_new_cat, btn_crear_cat], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text("Agregar película", size=14, weight=ft.FontWeight.W_600, color=PALETTE["text"]),
                ft.Row([tf_titulo], alignment=ft.MainAxisAlignment.START),
                ft.Row([tf_anio], alignment=ft.MainAxisAlignment.START),
                btn_add,
                ft.Divider(),
                btn_delete_sel,
                info_label,
            ],
        ),
    )

    # ---------- tarjeta de película (estilo pinterest) ----------
    def tarjeta_pelicula(p: Pelicula) -> ft.Container:
        k = peli_key(p)
        checked = k in seleccionadas_keys

        def toggle_select(e):
            if k in seleccionadas_keys:
                seleccionadas_keys.remove(k)
                btn_sel.icon = "check_box_outline_blank"
            else:
                seleccionadas_keys.add(k)
                btn_sel.icon = "check_box"
            page.update()

        btn_sel = ft.IconButton(icon=("check_box" if checked else "check_box_outline_blank"))
        title = ft.Text(p.nombre, size=16, weight=ft.FontWeight.W_700, color=PALETTE["text"], no_wrap=False)
        badge_gen = chip(getattr(p, "genero", ""), PALETTE["lav"])
        badge_year = chip(str(getattr(p, "anio", "") or "—"), PALETTE["mint"])

        return ft.Container(
            bgcolor=PALETTE["panel"],
            border_radius=20,
            padding=14,
            shadow=ft.BoxShadow(blur_radius=16, color=PALETTE["shadow"]),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Row([title, btn_sel], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START),
                    ft.Container(height=2, bgcolor=PALETTE["accent_soft"]),
                    ft.Row([badge_gen, badge_year], spacing=8),
                ],
            ),
        )

    # ---------- carga del grid ----------
    def cargar_grid(nombre_cat: str):
        seleccionadas_keys.clear()
        grid.controls = []
        if not nombre_cat:
            info_label.value = "Elegí o creá un catálogo para comenzar."
            page.update()
            return
        cat = CatalogoPeliculas(nombre_cat)
        pelis = cat.listar()
        for p in pelis:
            grid.controls.append(tarjeta_pelicula(p))
        info_label.value = f"Archivo: {cat.ruta_archivo} — {len(pelis)} película(s)"
        page.update()

    # ===================== eventos =====================

    def on_refresh(e):
        dd_catalogo.options = [ft.dropdown.Option(c) for c in listar_catalogos()]
        page.update()
        if dd_catalogo.value:
            cargar_grid(dd_catalogo.value)

    def on_change_catalogo(e):
        cargar_grid(dd_catalogo.value)

    def on_create_catalogo(e):
        nombre = normalizar_espacios(tf_new_cat.value or "")
        if not nombre:
            make_toast(page, "El nombre del catálogo no puede estar vacío.", ok=False)
            return
        path = ruta_catalogo(nombre)
        if os.path.exists(path):
            make_toast(page, "Ya existe un catálogo con ese nombre.", ok=False)
            return
        open(path, "w", encoding="utf-8").close()
        make_toast(page, f"Catálogo '{nombre}' creado.")
        dd_catalogo.options = [ft.dropdown.Option(c) for c in listar_catalogos()]
        dd_catalogo.value = nombre
        tf_new_cat.value = ""
        page.update()
        cargar_grid(nombre)

    def on_add_pelicula(e):
        if not dd_catalogo.value:
            make_toast(page, "Elegí un catálogo primero.", ok=False)
            return
        titulo = normalizar_espacios(tf_titulo.value or "")
        if not titulo:
            make_toast(page, "El título no puede estar vacío.", ok=False)
            return
        anio_str = (tf_anio.value or "").strip()
        anio = 0
        if anio_str:
            try:
                anio = int(anio_str)
            except ValueError:
                make_toast(page, "Año inválido. Se guardará sin año.", ok=False)
                anio = 0

        genero = normalizar_espacios(dd_catalogo.value).capitalize()
        p = Pelicula(titulo, genero, anio)
        cat = CatalogoPeliculas(dd_catalogo.value)
        if cat.agregar(p):
            make_toast(page, f"'{p.nombre}' agregada.")
            tf_titulo.value = ""
            tf_anio.value = ""
            page.update()
            cargar_grid(dd_catalogo.value)
        else:
            make_toast(page, "Esa película ya existe en el catálogo.", ok=False)

    def on_delete_selected(e):
        if not dd_catalogo.value:
            make_toast(page, "Elegí un catálogo primero.", ok=False)
            return
        if not seleccionadas_keys:
            make_toast(page, "No hay tarjetas seleccionadas.", ok=False)
            return

        cat = CatalogoPeliculas(dd_catalogo.value)
        actuales = cat.listar()
        restantes = [p for p in actuales if peli_key(p) not in seleccionadas_keys]
        reescribir_catalogo(cat, restantes)
        make_toast(page, f"Eliminadas {len(seleccionadas_keys)} película(s).")
        cargar_grid(dd_catalogo.value)

    # bind
    btn_refresh.on_click = on_refresh
    dd_catalogo.on_change = on_change_catalogo
    btn_crear_cat.on_click = on_create_catalogo
    btn_add.on_click = on_add_pelicula
    btn_delete_sel.on_click = on_delete_selected

    # ---------- layout raíz ----------
    page.add(
        ft.Column(
            expand=True,
            controls=[
                hero,
                ft.Container(
                    padding=16,
                    content=ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.START,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            side_panel,
                            ft.Container(width=12),
                            ft.Container(
                                expand=True,
                                bgcolor="transparent",
                                content=grid,
                            ),
                        ],
                    ),
                ),
            ],
        )
    )

    # estado inicial
    if catalogos:
        dd_catalogo.value = catalogos[0]
        cargar_grid(catalogos[0])
    else:
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
