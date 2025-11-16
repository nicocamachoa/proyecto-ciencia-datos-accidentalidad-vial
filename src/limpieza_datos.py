"""
Script de limpieza del dataset de accidentalidad vial en Bucaramanga.

Etapa 3 - Limpieza de datos:
- Reconocimiento y tratamiento de atributos con valores únicos o casi únicos
- Tratamiento de valores faltantes
- Tratamiento de valores atípicos
- Generación de un resumen de las transformaciones aplicadas
"""

import os
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


def cargar_datos(filepath: str) -> pd.DataFrame:
    """Carga el dataset desde un archivo CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo: {filepath}")
    df = pd.read_csv(filepath)
    return df


def diagnostico_calidad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construye una tabla de diagnóstico de calidad de datos por columna.

    Incluye:
    - Tipo de dato
    - Número y porcentaje de nulos
    - Cardinalidad (número de valores distintos)
    - Ejemplo de valores (hasta 3 valores distintos)
    """
    n_filas = len(df)
    resumen = []

    for col in df.columns:
        serie = df[col]
        n_nulos = serie.isna().sum()
        pct_nulos = (n_nulos / n_filas) * 100 if n_filas > 0 else 0
        cardinalidad = serie.nunique(dropna=True)
        ejemplo_vals = serie.dropna().unique()[:3] if cardinalidad > 0 else []

        resumen.append(
            {
                "columna": col,
                "tipo": str(serie.dtype),
                "n_nulos": int(n_nulos),
                "pct_nulos": round(pct_nulos, 2),
                "cardinalidad": int(cardinalidad),
                "ejemplo_valores": ejemplo_vals,
            }
        )

    diagnostico = pd.DataFrame(resumen)
    return diagnostico


def tratar_atributos_unicos(
    df: pd.DataFrame,
    columnas_forzadas_a_eliminar: List[str] = None,
    umbral_unicidad: float = 0.95,
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Identifica y trata atributos con valores únicos o casi únicos.

    Criterios:
    - Se eliminan columnas ID explícitas definidas en `columnas_forzadas_a_eliminar`.
    - Se marcan como de alta unicidad aquellas columnas donde
      (cardinalidad / número de filas) >= umbral_unicidad.

    Devuelve:
    - DataFrame resultante
    - Diccionario {columna: accion}
    """
    if columnas_forzadas_a_eliminar is None:
        columnas_forzadas_a_eliminar = ["ORDEN"]  # ID del registro

    n_filas = len(df)
    decisiones: Dict[str, str] = {}

    df_proc = df.copy()

    # Eliminar columnas forzadas
    for col in columnas_forzadas_a_eliminar:
        if col in df_proc.columns:
            df_proc = df_proc.drop(columns=[col])
            decisiones[col] = "eliminada (columna ID explícita)"

    # Detectar columnas de alta unicidad
    for col in df_proc.columns:
        cardinalidad = df_proc[col].nunique(dropna=True)
        ratio_unico = cardinalidad / n_filas if n_filas > 0 else 0.0

        if ratio_unico >= umbral_unicidad and col not in decisiones:
            # No eliminamos automáticamente, pero dejamos justificación
            decisiones[col] = (
                "alta unicidad, se mantiene por posible relevancia temporal/espacial"
            )

    return df_proc, decisiones


def tratar_valores_faltantes(
    df: pd.DataFrame,
    umbral_eliminacion_columna: float = 0.5,
) -> Tuple[pd.DataFrame, Dict[str, str]]:
    """
    Trata valores faltantes por columna.

    Estrategia:
    - Si pct de nulos > umbral_eliminacion_columna: eliminar la columna.
    - Si la columna es numérica: imputar mediana.
    - Si la columna es categórica (object): imputar moda.

    Devuelve:
    - DataFrame resultante
    - Diccionario {columna: accion}
    """
    n_filas = len(df)
    df_proc = df.copy()
    decisiones: Dict[str, str] = {}

    for col in list(df_proc.columns):
        serie = df_proc[col]
        n_nulos = serie.isna().sum()
        if n_filas == 0:
            continue

        pct_nulos = n_nulos / n_filas

        if pct_nulos == 0:
            decisiones[col] = "sin nulos"
            continue

        if pct_nulos > umbral_eliminacion_columna:
            df_proc = df_proc.drop(columns=[col])
            decisiones[col] = (
                f"eliminada (pct_nulos={pct_nulos:.2%} > {umbral_eliminacion_columna:.0%})"
            )
            continue

        # Imputación
        if pd.api.types.is_numeric_dtype(serie):
            mediana = serie.median()
            df_proc[col] = serie.fillna(mediana)
            decisiones[col] = (
                f"imputación con mediana ({mediana}) - pct_nulos={pct_nulos:.2%}"
            )
        else:
            # Categórica u otro tipo
            moda = serie.mode(dropna=True)
            if len(moda) > 0:
                valor = moda.iloc[0]
            else:
                valor = "SIN_DATO"
            df_proc[col] = serie.fillna(valor)
            decisiones[col] = (
                f"imputación con moda ('{valor}') - pct_nulos={pct_nulos:.2%}"
            )

    return df_proc, decisiones


def tratar_atipicos_iqr(
    df: pd.DataFrame,
    factor: float = 1.5,
) -> Tuple[pd.DataFrame, Dict[str, Dict[str, float]]]:
    """
    Trata valores atípicos en columnas numéricas usando el método IQR.

    Estrategia: *winsorización* (recorte/clipping):
    - Calcula Q1, Q3 e IQR.
    - Define límites inferior/superior = Q1 - factor*IQR, Q3 + factor*IQR.
    - Recorta valores por debajo/encima de los límites.

    Devuelve:
    - DataFrame resultante
    - Diccionario con resumen por columna:
      {col: {"q1":..., "q3":..., "lim_inf":..., "lim_sup":..., "n_modificados":...}}
    """
    df_proc = df.copy()
    resumen_atipicos: Dict[str, Dict[str, float]] = {}

    columnas_numericas = df_proc.select_dtypes(include=["number"]).columns

    for col in columnas_numericas:
        serie = df_proc[col].dropna()
        if serie.empty:
            continue

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)
        iqr = q3 - q1

        if iqr == 0:
            # No hay variación, no se identifican atípicos vía IQR
            continue

        lim_inf = q1 - factor * iqr
        lim_sup = q3 + factor * iqr

        # Contar atípicos antes
        mask_atipicos = (df_proc[col] < lim_inf) | (df_proc[col] > lim_sup)
        n_atipicos = int(mask_atipicos.sum())

        if n_atipicos > 0:
            df_proc[col] = df_proc[col].clip(lower=lim_inf, upper=lim_sup)

        resumen_atipicos[col] = {
            "q1": float(q1),
            "q3": float(q3),
            "lim_inf": float(lim_inf),
            "lim_sup": float(lim_sup),
            "n_modificados": n_atipicos,
        }

    return df_proc, resumen_atipicos


def normalizar_texto_categorico(df: pd.DataFrame, columnas: List[str]) -> pd.DataFrame:
    """
    Limpia valores categóricos aplicando strip() y normalización básica de espacios.
    Útil para reducir inconsistencias leves (espacios, mayúsculas/minúsculas).
    """
    df_proc = df.copy()
    for col in columnas:
        if col in df_proc.columns and df_proc[col].dtype == "object":
            df_proc[col] = (
                df_proc[col]
                .astype(str)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
            )
    return df_proc


def ejecutar_pipeline_limpieza(
    filepath_in: str = "data/raw/accidentes_transito.csv",
    filepath_out: str = "data/processed/accidentes_transito_limpio.csv",
) -> Tuple[pd.DataFrame, Dict[str, Dict]]:
    """
    Ejecuta de principio a fin la etapa de limpieza de datos.

    Devuelve:
    - DataFrame limpio
    - Reporte (diccionario) con decisiones y resúmenes de cada etapa
    """
    reporte: Dict[str, Dict] = {}

    # 1. Carga
    df_raw = cargar_datos(filepath_in)
    reporte["forma_inicial"] = {
        "filas": int(len(df_raw)),
        "columnas": int(df_raw.shape[1]),
    }

    # 2. Diagnóstico de calidad (solo análisis, sin modificar df)
    diag = diagnostico_calidad(df_raw)
    reporte["diagnostico_calidad"] = diag

    # 3. Tratamiento de atributos únicos / casi únicos
    df_proc, dec_unicos = tratar_atributos_unicos(df_raw)
    reporte["atributos_unicos"] = dec_unicos

    # 4. Tratamiento de valores faltantes
    df_proc, dec_nulos = tratar_valores_faltantes(df_proc)
    reporte["valores_faltantes"] = dec_nulos

    # 5. Normalización básica de texto en algunas columnas clave
    columnas_texto = [
        "BARRIO",
        "COMUNA",
        "GRAVEDAD",
        "MES",
        "DÍA",
        "ENTIDAD",
        "Propietario de Vehículo",
        "DIURNIO/NOCTURNO",
    ]
    df_proc = normalizar_texto_categorico(df_proc, columnas_texto)

    # 6. Tratamiento de valores atípicos numéricos
    df_proc, resumen_atipicos = tratar_atipicos_iqr(df_proc)
    reporte["valores_atipicos"] = resumen_atipicos

    # 7. Guardar resultado
    os.makedirs(os.path.dirname(filepath_out), exist_ok=True)
    df_proc.to_csv(filepath_out, index=False, encoding="utf-8")

    reporte["forma_final"] = {
        "filas": int(len(df_proc)),
        "columnas": int(df_proc.shape[1]),
    }
    return df_proc, reporte


if __name__ == "__main__":
    # Permite ejecutar el script directamente desde la línea de comandos
    in_path = "data/raw/accidentes_transito.csv"
    out_path = "data/processed/accidentes_transito_limpio.csv"

    try:
        print("🚀 Iniciando pipeline de limpieza...")
        df_limpio, reporte = ejecutar_pipeline_limpieza(in_path, out_path)
        print("✅ Limpieza completada.")
        print("Forma inicial:", reporte["forma_inicial"])
        print("Forma final:  ", reporte["forma_final"])
    except FileNotFoundError as e:
        print(f"❌ {e}")
