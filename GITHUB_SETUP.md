# Configuración de GitHub

## Pasos para crear el repositorio remoto en GitHub

### 1. Crear repositorio en GitHub

1. Ve a https://github.com
2. Haz clic en el botón "+" en la esquina superior derecha
3. Selecciona "New repository"
4. Completa la información:
   - **Repository name:** `proyecto-datos-accidentalidad-vial` (o el nombre que prefieras)
   - **Description:** Proyecto de Ciencia de Datos - Preparación de Datos sobre Accidentalidad Vial en Colombia
   - **Visibility:** Public o Private (según preferencia del equipo)
   - **NO** marques "Add a README file" (ya lo tenemos)
   - **NO** agregues .gitignore ni licencia (ya los tenemos)
5. Haz clic en "Create repository"

### 2. Conectar el repositorio local con GitHub

Después de crear el repositorio, GitHub te mostrará instrucciones. Usa las siguientes:

```bash
# Agregar el repositorio remoto
git remote add origin https://github.com/TU_USUARIO/proyecto-datos-accidentalidad-vial.git

# Verificar que se agregó correctamente
git remote -v

# Subir los commits al repositorio remoto
git push -u origin main
```

**IMPORTANTE:** Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub.

### 3. Alternativa con SSH (Recomendado para trabajo colaborativo)

Si prefieres usar SSH:

```bash
git remote add origin git@github.com:TU_USUARIO/proyecto-datos-accidentalidad-vial.git
git push -u origin main
```

### 4. Agregar colaboradores

Si el proyecto es grupal:

1. Ve al repositorio en GitHub
2. Haz clic en "Settings"
3. En el menú lateral, selecciona "Collaborators"
4. Haz clic en "Add people"
5. Busca a tus compañeros por usuario o email
6. Envía la invitación

### 5. Comandos útiles para trabajo en equipo

```bash
# Antes de empezar a trabajar, siempre traer cambios del remoto
git pull origin main

# Después de hacer cambios locales
git add .
git commit -m "Descripción del cambio"
git push origin main

# Ver el estado actual
git status

# Ver historial de commits
git log --oneline
```

## Estructura de Branches (Opcional pero recomendado)

Para trabajo colaborativo más organizado:

```bash
# Crear rama para cada integrante
git checkout -b nombre-integrante

# Trabajar en la rama
# ... hacer cambios ...
git add .
git commit -m "Descripción"
git push origin nombre-integrante

# Cuando esté listo para integrar, crear Pull Request en GitHub
```

## Buenas Prácticas

1. **Commits frecuentes:** Haz commits pequeños y descriptivos
2. **Pull antes de Push:** Siempre haz `git pull` antes de `git push`
3. **Mensajes claros:** Usa mensajes de commit descriptivos
4. **No subir datos grandes:** Los archivos CSV grandes pueden excluirse (ya están en .gitignore)
5. **Revisar cambios:** Usa `git status` y `git diff` antes de commit

## Notas

- Si el dataset es muy grande (>100MB), NO lo subas a GitHub
- GitHub tiene límite de 100MB por archivo
- Considera usar Git LFS para archivos grandes o compartir el dataset por otro medio (Drive, OneDrive, etc.)
