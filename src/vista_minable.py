"""
Script de construcción de la vista minable del dataset de accidentalidad vial en Bucaramanga.

Etapa 4 - Construcción de vista minable:
- Lectura del dataset limpio
- Ingeniería de atributos (fecha, hora, franjas horarias, variables derivadas)
- Selección de variables relevantes
- Construcción de una vista minable a nivel de accidente
- Generación opcional de una tabla resumen agregada

Uso recomendado:
from src.vista_minable import construir_vista_minable

df_vista, df_resumen = construir_vista_minable(
    filepath_in="data/processed/accidentes_transito_limpio.csv",
    filepath_out_vista="data/processed/accidentes_transito_vista_minable.csv",
    filepath_out_resumen="data/processed/accidentes_transito_resumen_mes_comuna.csv"
)
"""

import os
from typing import Tuple

import numpy as np
import pandas as pd


def cargar_datos_limpios(filepath: str) -> pd.DataFrame:
    """Carga el dataset limpio desde un archivo CSV."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de entrada: {filepath}")
    df = pd.read_csv(filepath)
    return df


def _parsear_fecha_hora(df: pd.DataFrame) -> pd.DataFrame:
    """
    A partir de las columnas FECHA y HORA crea atributos derivados:

    - fecha (datetime)
    - anio
    - mes_num
    - dia_mes
    - dia_semana (nombre)
    - hora_num (0-23)
    - minuto
    - franja_horaria (Madrugada, Mañana, Tarde, Noche)
    - es_fin_de_semana (True/False)
    """
    df_proc = df.copy()

    # FECHA
    if "FECHA" in df_proc.columns:
        df_proc["FECHA"] = pd.to_datetime(df_proc["FECHA"], errors="coerce")
        df_proc["anio"] = df_proc["FECHA"].dt.year
        df_proc["mes_num"] = df_proc["FECHA"].dt.month
        df_proc["dia_mes"] = df_proc["FECHA"].dt.day
        df_proc["dia_semana_num"] = df_proc["FECHA"].dt.weekday  # 0=Lunes

        # day_name en español puede variar según entorno; si falla, dejamos texto genérico
        try:
            df_proc["dia_semana"] = df_proc["FECHA"].dt.day_name(locale="es_ES")
        except TypeError:
            df_proc["dia_semana"] = df_proc["FECHA"].dt.day_name()
        df_proc["dia_semana"] = df_proc["dia_semana"].fillna("Desconocido")

        df_proc["es_fin_de_semana"] = df_proc["dia_semana_num"].isin([5, 6])
    else:
        # Si no existe FECHA pero sí AÑO, se conserva el año
        if "AÑO" in df_proc.columns:
            df_proc["anio"] = df_proc["AÑO"]
        else:
            df_proc["anio"] = np.nan

    # HORA
    if "HORA" in df_proc.columns:
        # La hora viene como '1899-12-31T12:15:00.000', extraemos la parte de hora
        hora_str = pd.to_datetime(df_proc["HORA"], errors="coerce")
        df_proc["hora_num"] = hora_str.dt.hour
        df_proc["minuto"] = hora_str.dt.minute
    else:
        df_proc["hora_num"] = np.nan
        df_proc["minuto"] = np.nan

    # Franjas horarias
    def clasificar_franja(hora: float) -> str:
        if pd.isna(hora):
            return "Desconocida"
        if 0 <= hora < 6:
            return "Madrugada"
        if 6 <= hora < 12:
            return "Mañana"
        if 12 <= hora < 18:
            return "Tarde"
        return "Noche"

    df_proc["franja_horaria"] = df_proc["hora_num"].apply(clasificar_franja)

    return df_proc


def _procesar_comuna(df: pd.DataFrame) -> pd.DataFrame:
    """
    Descompone la columna COMUNA en código y nombre (si viene en formato '03. SAN FRANCISCO'):

    - comuna_codigo
    - comuna_nombre
    """
    df_proc = df.copy()

    if "COMUNA" in df_proc.columns:
        # Convertir a string y dividir por el primer punto
        def split_comuna(valor: object) -> tuple[str, str]:
            if pd.isna(valor):
                return "", ""
            texto = str(valor)
            if "." in texto:
                partes = texto.split(".", 1)
                codigo = partes[0].strip()
                nombre = partes[1].strip()
                return codigo, nombre
            return "", texto.strip()

        codigos = []
        nombres = []
        for v in df_proc["COMUNA"]:
            c, n = split_comuna(v)
            codigos.append(c)
            nombres.append(n)

        df_proc["comuna_codigo"] = codigos
        df_proc["comuna_nombre"] = nombres
    else:
        df_proc["comuna_codigo"] = ""
        df_proc["comuna_nombre"] = ""

    return df_proc


def _normalizar_periodo_dia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza la columna 'DIURNIO/NOCTURNO' (si existe) a categorías consistentes:

    - 'Diurno'
    - 'Nocturno'
    - 'Mixto/Desconocido'
    """
    df_proc = df.copy()

    col = "DIURNIO/NOCTURNO"
    if col not in df_proc.columns:
        df_proc["periodo_dia"] = "Desconocido"
        return df_proc

    mapping = {
        "Diurno": "Diurno",
        "DIURNO": "Diurno",
        "Nocturno": "Nocturno",
        "NOCTURNO": "Nocturno",
    }

    def map_periodo(valor: object) -> str:
        if pd.isna(valor):
            return "Desconocido"
        texto = str(valor).strip()
        if texto in mapping:
            return mapping[texto]
        # Cualquier otro valor se agrupa como mixto/desconocido
        return "Mixto/Desconocido"

    df_proc["periodo_dia"] = df_proc[col].apply(map_periodo)
    return df_proc


def ingenieria_atributos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica transformaciones de ingeniería de atributos sobre el dataset limpio:

    - Fecha y hora -> anio, mes_num, dia_semana, franja_horaria, etc.
    - COMUNA -> comuna_codigo, comuna_nombre
    - DIURNIO/NOCTURNO -> periodo_dia
    """
    df_proc = _parsear_fecha_hora(df)
    df_proc = _procesar_comuna(df_proc)
    df_proc = _normalizar_periodo_dia(df_proc)

    return df_proc


def construir_vista_minable(
    filepath_in: str = "data/processed/accidentes_transito_limpio.csv",
    filepath_out_vista: str = "data/processed/accidentes_transito_vista_minable.csv",
    filepath_out_resumen: str = "data/processed/accidentes_transito_resumen_mes_comuna.csv",
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Construye la vista minable a partir del dataset limpio.

    - Lee el dataset limpio.
    - Aplica ingeniería de atributos.
    - Selecciona columnas relevantes para análisis.
    - Genera y guarda:
      (1) Vista minable a nivel de accidente.
      (2) Tabla resumen agregada por año, mes, comuna y gravedad.

    Devuelve:
    - df_vista: vista minable a nivel de registro
    - df_resumen: tabla agregada de resumen
    """
    df_limpio = cargar_datos_limpios(filepath_in)

    # Aplicar ingeniería de atributos
    df_feat = ingenieria_atributos(df_limpio)

    # Seleccionar columnas relevantes para la vista minable
    columnas_vista: list[str] = []

    # Mantener algunas columnas originales clave si existen
    for col in ["AÑO", "MES", "DÍA", "GRAVEDAD", "BARRIO", "COMUNA", "ENTIDAD", "Propietario de Vehículo"]:
        if col in df_feat.columns:
            columnas_vista.append(col)

    # Añadir columnas derivadas
    derivadas = [
        "anio",
        "mes_num",
        "dia_mes",
        "dia_semana",
        "es_fin_de_semana",
        "hora_num",
        "franja_horaria",
        "periodo_dia",
        "comuna_codigo",
        "comuna_nombre",
    ]
    for col in derivadas:
        if col in df_feat.columns:
            columnas_vista.append(col)

    df_vista = df_feat[columnas_vista].copy()

    # Guardar vista minable
    os.makedirs(os.path.dirname(filepath_out_vista), exist_ok=True)
    df_vista.to_csv(filepath_out_vista, index=False, encoding="utf-8")

    # Construir tabla resumen agregada por año, mes, comuna y gravedad
    group_cols: list[str] = []
    for col in ["anio", "mes_num", "comuna_nombre", "GRAVEDAD"]:
        if col in df_feat.columns:
            group_cols.append(col)

    if group_cols:
        df_resumen = (
            df_feat
            .groupby(group_cols)
            .size()
            .reset_index(name="n_accidentes")
        )
    else:
        # Si por alguna razón no se encuentran las columnas, se crea tabla vacía
        df_resumen = pd.DataFrame(columns=["anio", "mes_num", "comuna_nombre", "GRAVEDAD", "n_accidentes"])

    # Guardar resumen
    os.makedirs(os.path.dirname(filepath_out_resumen), exist_ok=True)
    df_resumen.to_csv(filepath_out_resumen, index=False, encoding="utf-8")

    return df_vista, df_resumen


if __name__ == "__main__":
    in_path = "data/processed/accidentes_transito_limpio.csv"
    out_vista = "data/processed/accidentes_transito_vista_minable.csv"
    out_resumen = "data/processed/accidentes_transito_resumen_mes_comuna.csv"

    try:
        print("=" * 80)
        print(" ETAPA 4 - CONSTRUCCIÓN DE VISTA MINABLE")
        print("=" * 80)
        print(f"Archivo de entrada: {in_path}")

        df_vista, df_resumen = construir_vista_minable(
            filepath_in=in_path,
            filepath_out_vista=out_vista,
            filepath_out_resumen=out_resumen,
        )

        print("\n✓ Vista minable creada correctamente")
        print(f" - Registros (vista): {len(df_vista):,}")
        print(f" - Columnas (vista):  {df_vista.shape[1]}")

        print("\n✓ Tabla resumen creada correctamente")
        print(f" - Registros (resumen): {len(df_resumen):,}")
        print(f" - Columnas (resumen):  {df_resumen.shape[1]}")

        print("\nArchivos generados:")
        print(f" - Vista minable: {out_vista}")
        print(f" - Resumen:       {out_resumen}")
        print("=" * 80)
    except FileNotFoundError as e:
        print(f"❌ {e}")
