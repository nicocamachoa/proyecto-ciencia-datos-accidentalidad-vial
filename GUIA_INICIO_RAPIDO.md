# Guía de Inicio Rápido

## Configuración Inicial del Proyecto

### 1. Configurar Git (Si no lo has hecho)

```bash
# Configurar tu nombre y email
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@javeriana.edu.co"
```

### 2. Crear y Conectar Repositorio GitHub

Ver instrucciones detalladas en: `GITHUB_SETUP.md`

Resumen rápido:
```bash
# Crear repo en GitHub primero, luego:
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git
git push -u origin main
```

### 3. Instalar Dependencias Python

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
pip list
```

### 4. Descargar el Dataset

Ver instrucciones en: `data/raw/INSTRUCCIONES_DESCARGA.md`

Resumen:
1. Ir a https://www.datos.gov.co/Transporte/03-ACCIDENTES-DE-TRANSITO-DESDE-ENERO-2012-A-FEBRE/7cci-nqqb
2. Exportar como CSV
3. Guardar como `data/raw/accidentes_transito.csv`

### 5. Iniciar Jupyter Notebook

```bash
# Asegúrate de estar en la carpeta del proyecto
cd /ruta/al/proyecto

# Iniciar Jupyter
jupyter notebook

# O Jupyter Lab (más moderno)
jupyter lab
```

El navegador se abrirá automáticamente. Navega a `notebooks/` y abre `01_planificacion.ipynb`

## Flujo de Trabajo

### Orden de Ejecución de Notebooks

1. **01_planificacion.ipynb** - Etapa 1: Planeación y Recopilación
2. **02_exploracion.ipynb** - Etapa 2: Exploración de Datos (próximo)
3. **03_limpieza.ipynb** - Etapa 3: Limpieza de Datos (próximo)
4. **04_vista_minable.ipynb** - Etapa 4: Vista Minable (próximo)

### Trabajo en Equipo con Git

```bash
# Antes de trabajar
git pull origin main

# Después de trabajar
git add .
git commit -m "Descripción clara de los cambios"
git push origin main
```

## Estructura del Proyecto

```
Proyecto/
├── data/
│   ├── raw/                    # Datos originales (NO modificar)
│   ├── processed/              # Datos después de limpieza
│   └── final/                  # Vista minable final
├── notebooks/
│   ├── 01_planificacion.ipynb      # ← Empezar aquí
│   ├── 02_exploracion.ipynb
│   ├── 03_limpieza.ipynb
│   └── 04_vista_minable.ipynb
├── src/                        # Scripts Python auxiliares
├── visualizations/             # Gráficos generados
├── docs/                       # Documentación
├── README.md                   # Descripción del proyecto
├── requirements.txt            # Dependencias Python
└── .gitignore                 # Archivos ignorados por Git
```

## Entregables del Proyecto

- [ ] **Documento completo** (portada, introducción, desarrollo, conclusiones)
- [ ] **Presentación** (aspectos clave del proyecto)
- [ ] **Infografía** (hallazgos principales)
- [ ] **Fecha límite:** 16 de noviembre, 11:59 PM

## Checklist de Verificación

### Etapa 1 - Planeación
- [ ] Dataset descargado
- [ ] Más de 2000 registros
- [ ] Más de 12 atributos
- [ ] Pregunta guía definida
- [ ] Contexto del problema documentado

### Etapa 2 - Exploración
- [ ] Tabla de diagnóstico de calidad
- [ ] Visualizaciones creadas
- [ ] Análisis de correlación
- [ ] Análisis documentado

### Etapa 3 - Limpieza
- [ ] Valores únicos tratados
- [ ] Valores faltantes tratados
- [ ] Valores atípicos tratados
- [ ] Decisiones justificadas

### Etapa 4 - Vista Minable
- [ ] Al menos 1 normalización
- [ ] Al menos 1 discretización
- [ ] Al menos 1 numerización

### Etapa 5 - Infografía
- [ ] Infografía creada
- [ ] Visualizaciones incluidas
- [ ] Interpretaciones agregadas

## Ayuda y Recursos

- **Profesor:** Luis Carlos Chicaíza
- **Documentación Pandas:** https://pandas.pydata.org/docs/
- **Documentación Seaborn:** https://seaborn.pydata.org/
- **Documentación Matplotlib:** https://matplotlib.org/

## Contacto del Equipo

- Integrante 1: [nombre y email]
- Integrante 2: [nombre y email]
- Integrante 3: [nombre y email]
