"""
Script de generación de infografía a partir de la vista minable
del dataset de accidentalidad vial en Bucaramanga.

Etapa 5 - Infografía final:
- Lectura de la vista minable y tabla resumen
- Cálculo de métricas clave de negocio
- Construcción de una infografía con varias visualizaciones
  (distribuciones por gravedad, comuna, año y franja horaria)

Uso recomendado:

from src.infografia import (
    cargar_vista_minable,
    cargar_resumen_accidentes,
    calcular_metricas_resumen,
    crear_infografia,
    exportar_infografia,
)

df_vista = cargar_vista_minable("data/processed/accidentes_transito_vista_minable.csv")
df_resumen = cargar_resumen_accidentes("data/processed/accidentes_transito_resumen_mes_comuna.csv")
metricas = calcular_metricas_resumen(df_vista, df_resumen)
fig = crear_infografia(df_vista, df_resumen, metricas)
exportar_infografia(fig, "visualizations/infografia_accidentes.png")
"""

import os
from typing import Dict, Optional

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def cargar_vista_minable(filepath: str) -> pd.DataFrame:
    """Carga la vista minable desde un archivo CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de vista minable: {filepath}")
    return pd.read_csv(filepath)


def cargar_resumen_accidentes(filepath: str) -> pd.DataFrame:
    """Carga la tabla resumen de accidentes desde un archivo CSV (si existe)."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de resumen: {filepath}")
    return pd.read_csv(filepath)


def calcular_metricas_resumen(
    df_vista: pd.DataFrame,
    df_resumen: Optional[pd.DataFrame] = None,
) -> Dict[str, object]:
    """
    Calcula métricas básicas para el contexto de negocio a partir de la vista minable.

    Devuelve un diccionario con:
    - total_accidentes
    - anio_min, anio_max
    - n_anios
    - n_comunas
    - gravedad_mas_frecuente
    - comuna_top (nombre y número de accidentes)
    """
    metricas: Dict[str, object] = {}

    # Total accidentes
    metricas["total_accidentes"] = int(len(df_vista))

    # Rango de años
    if "anio" in df_vista.columns:
        anios_validos = df_vista["anio"].dropna().astype(int)
        if not anios_validos.empty:
            metricas["anio_min"] = int(anios_validos.min())
            metricas["anio_max"] = int(anios_validos.max())
            metricas["n_anios"] = int(len(anios_validos.unique()))
        else:
            metricas["anio_min"] = None
            metricas["anio_max"] = None
            metricas["n_anios"] = 0
    else:
        metricas["anio_min"] = None
        metricas["anio_max"] = None
        metricas["n_anios"] = 0

    # Número de comunas distintas
    if "comuna_nombre" in df_vista.columns:
        metricas["n_comunas"] = int(df_vista["comuna_nombre"].nunique(dropna=True))
    else:
        metricas["n_comunas"] = 0

    # Gravedad más frecuente
    if "GRAVEDAD" in df_vista.columns:
        conteo_gravedad = df_vista["GRAVEDAD"].value_counts()
        if not conteo_gravedad.empty:
            metricas["gravedad_mas_frecuente"] = conteo_gravedad.idxmax()
        else:
            metricas["gravedad_mas_frecuente"] = None
    else:
        metricas["gravedad_mas_frecuente"] = None

    # Comuna con más accidentes
    if "comuna_nombre" in df_vista.columns:
        conteo_comunas = df_vista["comuna_nombre"].value_counts()
        if not conteo_comunas.empty:
            metricas["comuna_top_nombre"] = conteo_comunas.idxmax()
            metricas["comuna_top_accidentes"] = int(conteo_comunas.max())
        else:
            metricas["comuna_top_nombre"] = None
            metricas["comuna_top_accidentes"] = 0
    else:
        metricas["comuna_top_nombre"] = None
        metricas["comuna_top_accidentes"] = 0

    return metricas


def crear_infografia(
    df_vista: pd.DataFrame,
    df_resumen: Optional[pd.DataFrame],
    metricas: Dict[str, object],
    titulo: str = "Infografía de accidentalidad vial en Bucaramanga",
):
    """
    Construye una infografía compuesta por varias visualizaciones:

    - Panel superior: título y métricas clave (KPI).
    - Panel medio izquierdo: distribución de accidentes por gravedad.
    - Panel medio derecho: top 5 comunas con más accidentes.
    - Panel inferior izquierdo: evolución anual del número de accidentes.
    - Panel inferior derecho: cruce gravedad vs. franja horaria (heatmap).

    La infografía se construye dinámicamente a partir de los datos provistos.
    Devuelve el objeto Figure de Matplotlib.
    """
    sns.set_palette("Set2")
    plt.style.use("seaborn-v0_8-whitegrid")

    fig = plt.figure(figsize=(16, 9))
    grid = fig.add_gridspec(3, 4)

    # ---------------------------------------------------------------------
    # Panel superior: título + KPIs
    # ---------------------------------------------------------------------
    ax_title = fig.add_subplot(grid[0, :])
    ax_title.axis("off")

    # Título principal
    ax_title.text(
        0.5,
        0.8,
        titulo,
        ha="center",
        va="center",
        fontsize=18,
        fontweight="bold",
    )

    # Subtítulo con contexto temporal
    if metricas.get("anio_min") is not None and metricas.get("anio_max") is not None:
        rango_anios = f"{metricas['anio_min']} - {metricas['anio_max']}"
    else:
        rango_anios = "N/D"

    subtitulo = (
        f"Total accidentes: {metricas.get('total_accidentes', 0):,} | "
        f"Rango de años: {rango_anios} | "
        f"Comunas analizadas: {metricas.get('n_comunas', 0)}"
    )
    ax_title.text(
        0.5,
        0.55,
        subtitulo,
        ha="center",
        va="center",
        fontsize=11,
    )

    # KPIs en recuadros
    gravedad_top = metricas.get("gravedad_mas_frecuente", "N/D")
    comuna_top = metricas.get("comuna_top_nombre", "N/D")
    comuna_top_acc = metricas.get("comuna_top_accidentes", 0)

    kpi_texts = [
        f"Gravedad más frecuente:\n{gravedad_top}",
        f"Comuna con más accidentes:\n{comuna_top}",
        f"Nº de accidentes en la comuna líder:\n{comuna_top_acc:,}",
    ]

    x_positions = [0.2, 0.5, 0.8]
    for x, text in zip(x_positions, kpi_texts):
        ax_title.text(
            x,
            0.15,
            text,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8),
        )

    # ---------------------------------------------------------------------
    # Panel medio izquierdo: distribución por gravedad
    # ---------------------------------------------------------------------
    ax_gravedad = fig.add_subplot(grid[1, 0:2])

    if "GRAVEDAD" in df_vista.columns:
        conteo_grav = (
            df_vista["GRAVEDAD"]
            .value_counts()
            .sort_values(ascending=False)
        )
        sns.barplot(
            x=conteo_grav.index,
            y=conteo_grav.values,
            ax=ax_gravedad,
        )
        ax_gravedad.set_title("Distribución de accidentes por gravedad")
        ax_gravedad.set_xlabel("Gravedad")
        ax_gravedad.set_ylabel("Número de accidentes")
        ax_gravedad.tick_params(axis="x", rotation=30)
    else:
        ax_gravedad.text(0.5, 0.5, "No se encontró la columna GRAVEDAD", ha="center")
        ax_gravedad.axis("off")

    # ---------------------------------------------------------------------
    # Panel medio derecho: top 5 comunas
    # ---------------------------------------------------------------------
    ax_comunas = fig.add_subplot(grid[1, 2:4])

    if "comuna_nombre" in df_vista.columns:
        conteo_comunas = (
            df_vista["comuna_nombre"]
            .value_counts()
            .head(5)
            .sort_values(ascending=True)  # para barh ordenado
        )
        sns.barplot(
            x=conteo_comunas.values,
            y=conteo_comunas.index,
            ax=ax_comunas,
        )
        ax_comunas.set_title("Top 5 comunas con más accidentes")
        ax_comunas.set_xlabel("Número de accidentes")
        ax_comunas.set_ylabel("Comuna")
    else:
        ax_comunas.text(0.5, 0.5, "No se encontró la columna comuna_nombre", ha="center")
        ax_comunas.axis("off")

    # ---------------------------------------------------------------------
    # Panel inferior izquierdo: evolución anual
    # ---------------------------------------------------------------------
    ax_anio = fig.add_subplot(grid[2, 0:2])

    if "anio" in df_vista.columns:
        df_anio = (
            df_vista
            .groupby("anio")
            .size()
            .reset_index(name="n_accidentes")
            .sort_values("anio")
        )
        ax_anio.plot(
            df_anio["anio"],
            df_anio["n_accidentes"],
            marker="o",
        )
        ax_anio.set_title("Evolución anual del número de accidentes")
        ax_anio.set_xlabel("Año")
        ax_anio.set_ylabel("Número de accidentes")
    else:
        ax_anio.text(0.5, 0.5, "No se encontró la columna anio", ha="center")
        ax_anio.axis("off")

    # ---------------------------------------------------------------------
    # Panel inferior derecho: heatmap gravedad vs. franja horaria
    # ---------------------------------------------------------------------
    ax_heatmap = fig.add_subplot(grid[2, 2:4])

    if all(col in df_vista.columns for col in ["GRAVEDAD", "franja_horaria"]):
        tabla = (
            df_vista
            .groupby(["GRAVEDAD", "franja_horaria"])
            .size()
            .reset_index(name="n_accidentes")
        )
        pivot = tabla.pivot(
            index="GRAVEDAD",
            columns="franja_horaria",
            values="n_accidentes",
        ).fillna(0)

        # Orden opcional de columnas
        orden_franjas = ["Madrugada", "Mañana", "Tarde", "Noche", "Desconocida"]
        cols_presentes = [c for c in orden_franjas if c in pivot.columns]
        pivot = pivot[cols_presentes]

        sns.heatmap(
            pivot,
            annot=True,
            fmt=".0f",
            linewidths=0.5,
            ax=ax_heatmap,
        )
        ax_heatmap.set_title("Accidentes por gravedad y franja horaria")
        ax_heatmap.set_xlabel("Franja horaria")
        ax_heatmap.set_ylabel("Gravedad")
    else:
        ax_heatmap.text(
            0.5,
            0.5,
            "No se encontraron las columnas GRAVEDAD y/o franja_horaria",
            ha="center",
        )
        ax_heatmap.axis("off")

    fig.tight_layout()
    return fig


def exportar_infografia(fig, output_path: str) -> None:
    """Guarda la figura de la infografía en la ruta especificada."""
    carpeta = os.path.dirname(output_path)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    fig.savefig(output_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    # Rutas por defecto (relativas a la raíz del proyecto)
    vista_path = "data/processed/accidentes_transito_vista_minable.csv"
    resumen_path = "data/processed/accidentes_transito_resumen_mes_comuna.csv"
    salida_img = "visualizations/infografia_accidentes.png"

    try:
        print("=" * 80)
        print(" ETAPA 5 - INFOGRAFÍA FINAL")
        print("=" * 80)

        df_vista = cargar_vista_minable(vista_path)
        df_resumen = cargar_resumen_accidentes(resumen_path)

        metricas = calcular_metricas_resumen(df_vista, df_resumen)
        fig = crear_infografia(df_vista, df_resumen, metricas)
        exportar_infografia(fig, salida_img)

        print("✓ Infografía generada correctamente.")
        print(f"Archivo de salida: {salida_img}")
        print("=" * 80)
    except FileNotFoundError as e:
        print(f"❌ {e}")
