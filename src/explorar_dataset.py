"""
Script de Exploración Inicial del Dataset
Proyecto: Accidentalidad Vial en Bucaramanga
"""

import pandas as pd
import numpy as np

def explorar_dataset(filepath='data/raw/accidentes_transito.csv'):
    """Realiza exploración inicial del dataset de accidentes"""

    # Cargar datos
    print("Cargando dataset...")
    df = pd.read_csv(filepath)

    print("\n" + "="*80)
    print("EXPLORACIÓN INICIAL - DATASET ACCIDENTES DE TRÁNSITO BUCARAMANGA")
    print("="*80)

    # 1. Información básica
    print(f"\n📊 INFORMACIÓN GENERAL")
    print(f"   Registros: {len(df):,}")
    print(f"   Columnas: {len(df.columns)}")
    print(f"   Tamaño en memoria: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

    # 2. Periodo temporal
    print(f"\n📅 PERIODO TEMPORAL")
    print(f"   Desde: {df['AÑO'].min()}")
    print(f"   Hasta: {df['AÑO'].max()}")
    print(f"   Total años: {df['AÑO'].nunique()}")

    # 3. Valores faltantes
    print(f"\n🔍 CALIDAD DE DATOS")
    missing = df.isnull().sum().sum()
    print(f"   Valores faltantes: {missing} ({missing/df.size*100:.2f}%)")
    print(f"   Filas duplicadas: {df.duplicated().sum()}")

    # 4. Variables categóricas principales
    print(f"\n📑 VARIABLES CATEGÓRICAS PRINCIPALES")
    print(f"   Tipos de gravedad: {df['GRAVEDAD'].nunique()}")
    print(f"   Barrios: {df['BARRIO'].nunique()}")
    print(f"   Comunas: {df['COMUNA'].nunique()}")

    # 5. Distribución de gravedad
    print(f"\n⚠️  DISTRIBUCIÓN POR GRAVEDAD")
    gravedad_counts = df['GRAVEDAD'].value_counts()
    for gravedad, count in gravedad_counts.items():
        pct = count / len(df) * 100
        print(f"   {gravedad:20s}: {count:6,} ({pct:5.2f}%)")

    # 6. Vehículos más involucrados
    print(f"\n🚗 VEHÍCULOS INVOLUCRADOS (Total acumulado)")
    vehiculos = ['PEATON', 'AUTOMOVIL', 'CAMPERO', 'CAMIONETA', 'MICRO',
                 'BUSETA', 'BUS', 'CAMION', 'VOLQUETA', 'MOTO', 'BICICLETA', 'OTRO']

    vehiculos_total = {}
    for veh in vehiculos:
        total = df[veh].sum()
        vehiculos_total[veh] = total

    # Ordenar de mayor a menor
    for veh, total in sorted(vehiculos_total.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"   {veh:15s}: {total:6,}")

    # 7. Accidentes diurnos vs nocturnos
    print(f"\n🌞 DIURNO VS NOCTURNO")
    diurno_counts = df['DIURNIO/NOCTURNO'].value_counts()
    for tipo, count in diurno_counts.items():
        pct = count / len(df) * 100
        print(f"   {tipo:15s}: {count:6,} ({pct:5.2f}%)")

    # 8. Top 5 barrios con más accidentes
    print(f"\n📍 TOP 5 BARRIOS CON MÁS ACCIDENTES")
    top_barrios = df['BARRIO'].value_counts().head(5)
    for i, (barrio, count) in enumerate(top_barrios.items(), 1):
        pct = count / len(df) * 100
        print(f"   {i}. {barrio:30s}: {count:4,} ({pct:4.2f}%)")

    # 9. Años con más accidentes
    print(f"\n📈 ACCIDENTES POR AÑO")
    accidentes_año = df['AÑO'].value_counts().sort_index()
    for año, count in accidentes_año.items():
        print(f"   {año}: {'█' * int(count/500)} {count:,}")

    print("\n" + "="*80)
    print("✓ Exploración completada")
    print("="*80)

    return df

if __name__ == "__main__":
    df = explorar_dataset()
