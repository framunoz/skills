# Instalación de Comandos Personalizados

Sigue estos pasos para habilitar los comandos `blackp`, `ruffp`, `pyreflyp`, `nbstripoutp` y `format` en tu terminal.

## 1. Localización del Directorio
Identifica la ruta completa hacia el directorio `scripts/` de este repositorio o skill. Puedes obtenerla ejecutando esto dentro de dicha carpeta:
```bash
pwd
```

Para los siguientes pasos, asumiremos que `<SKILL_PATH>` es la ruta donde se encuentra el skill/repositorio.

## 2. Configuración del Shell (Mac/Linux)
Para poder ejecutar estos comandos desde cualquier carpeta, añade el directorio `scripts` a tu `PATH`:

1. Abre tu archivo de configuración (ej. `~/.zshrc` o `~/.bashrc`):
   ```bash
   nano ~/.zshrc
   ```
2. Añade la siguiente línea al final (sustituyendo `<SKILL_PATH>` por tu ruta real):
   ```bash
   export PATH="$PATH:<SKILL_PATH>/scripts"
   ```
3. Guarda los cambios (Ctrl+O, Enter) y sal (Ctrl+X).
4. Recarga la configuración:
   ```bash
   source ~/.zshrc
   ```

## 3. Comandos Disponibles

| Comando | Herramienta | Acción |
| :--- | :--- | :--- |
| `format` | Multi-tool | Ejecuta Black, Ruff y Pyrefly en secuencia. |
| `blackp` | Black | Formatea código (incluyendo Jupyter) con `--preview`. |
| `ruffp` | Ruff | Ejecuta linting y auto-fixes rápidos. |
| `pyreflyp` | Pyrefly | Revisa tipos estructurales y linting avanzado. |
| `nbstripoutp` | nbstripout | Limpia los outputs de los notebooks Jupyter. |

## 4. Uso
Simplemente escribe el comando seguido del archivo o carpeta a procesar:
```bash
format .
blackp mi_archivo.py
```
