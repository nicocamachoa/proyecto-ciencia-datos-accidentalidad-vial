# Instrucciones para Descargar el Dataset

## Dataset Seleccionado: Accidentes de Tránsito en Colombia

### Opción 1: Dataset de Bucaramanga (2012-2023) - RECOMENDADO

**URL:** https://www.datos.gov.co/Transporte/03-ACCIDENTES-DE-TRANSITO-DESDE-ENERO-2012-A-FEBRE/7cci-nqqb

**Pasos:**
1. Accede a la URL arriba mencionada
2. En la parte superior derecha, busca el botón "Exportar" o "Export"
3. Selecciona el formato **CSV**
4. Descarga el archivo
5. Renombra el archivo a: `accidentes_transito.csv`
6. Guarda el archivo en esta carpeta: `data/raw/`

### Opción 2: Dataset Nacional (2017-2022)

**URL:** https://www.datos.gov.co/Transporte/ACCIDENTES-DE-TRANSITO-DESDE-MARZO-2017-A-DICIEMBR/wacd-xkg8

**Pasos:** (Mismos que la opción 1)

### Opción 3: ANSV (Agencia Nacional de Seguridad Vial)

**URL:** https://ansv.gov.co/observatorio/estadisticas

**Pasos:**
1. Navega por la sección de "Estadísticas"
2. Busca datasets de "Siniestralidad Vial"
3. Descarga el archivo más reciente disponible
4. Convierte a CSV si es necesario
5. Guarda en esta carpeta

---

## Verificación

Después de descargar, verifica que el archivo:
- ✓ Tenga al menos **2,000 registros**
- ✓ Tenga al menos **12 columnas/atributos**
- ✓ Incluya variables numéricas y categóricas
- ✓ Esté en formato CSV
- ✓ Tenga el nombre: `accidentes_transito.csv`

## Columnas Esperadas

El dataset debería incluir columnas como:
- Fecha/Año/Mes/Día
- Tipo de accidente
- Gravedad
- Tipo de vehículo
- Ubicación (dirección, comuna, barrio, coordenadas)
- Hora del accidente
- Clase de accidente
- Y otras variables relevantes

---

**NOTA:** Una vez descargado el archivo, ejecuta el notebook `notebooks/01_planificacion.ipynb` para cargar y verificar el dataset.
