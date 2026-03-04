# mov2mp4

Script **CLI en Python** para convertir archivos **`.mov` → `.mp4`** usando **ffmpeg** (vía `subprocess`).

- Soporta **archivo único** o **conversión por lote** (carpeta).
- Por defecto **re-codifica** a **H.264 (libx264) + AAC** para máxima compatibilidad.
- Opción para **copiar streams** (`--copy`) cuando el `.mov` ya trae códecs compatibles.
- Incluye `-movflags +faststart` para que el MP4 **cargue más rápido en la web**.

---

## Requisitos

- **Python 3.10+**  
- **ffmpeg** instalado y disponible en el `PATH`

Verifica ffmpeg:

```bash
ffmpeg -version
```

---

## Instalación

1) Clona el repositorio:

```bash
git clone https://github.com/isantosruiz/mov2mp4.git
cd mov2mp4
```

2) Instala **ffmpeg** (elige tu sistema):

### macOS (Homebrew)

```bash
brew install ffmpeg
```

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg
```

### Windows

Opciones típicas:

```powershell
winget install Gyan.FFmpeg
```

o con Chocolatey:

```powershell
choco install ffmpeg
```

> Importante: tras instalar, abre una nueva terminal y confirma `ffmpeg -version`.

---

## Uso

### Sintaxis

```bash
python mov2mp4.py INPUT [opciones]
```

- `INPUT` puede ser un **archivo `.mov`** o una **carpeta** que contenga `.mov`.

---

## Ejemplo rápido

Convierte un archivo y genera el `.mp4` junto al original:

```bash
python mov2mp4.py video.mov
```

Esto creará `video.mp4` en la misma carpeta (sobrescribe si ya existe).

---

## Casos típicos

### 1) Convertir un archivo

```bash
python mov2mp4.py video.mov
```

### 2) Especificar salida (solo para archivo único)

```bash
python mov2mp4.py entrada.mov -o salida.mp4
```

> Si `-o` no termina en `.mp4`, el script ajusta la extensión automáticamente.

### 3) Ajustar calidad y velocidad (CRF / preset)

```bash
python mov2mp4.py entrada.mov --crf 20 --preset slow
```

- `--crf` controla calidad/tamaño (típico: **18–23**; menor = mejor calidad y mayor tamaño).
- `--preset` controla velocidad/eficiencia (`ultrafast … placebo`).

### 4) Copiar streams (sin re-encode) si ya son compatibles

```bash
python mov2mp4.py entrada.mov --copy
```

- Mucho más rápido y sin pérdida.
- Si el `.mov` trae códecs no compatibles con MP4, ffmpeg puede fallar: en ese caso, quita `--copy`.

### 5) Convertir todos los `.mov` en una carpeta

```bash
python mov2mp4.py /ruta/a/carpeta
```

Genera cada `.mp4` junto a su `.mov`.

### 6) Buscar `.mov` en subcarpetas (recursivo)

```bash
python mov2mp4.py /ruta/a/carpeta --recursive
```

### 7) Pasar flags extra directamente a ffmpeg

Todo lo que pongas después de `--extra` se pasa **tal cual** a ffmpeg:

```bash
python mov2mp4.py entrada.mov --extra -vf scale=1280:-2
```

Otro ejemplo (limitar FPS):

```bash
python mov2mp4.py entrada.mov --extra -r 30
```

> Nota: `--extra` debe ir al final (porque captura el “resto” de argumentos).

---

## Qué hace por defecto

Si **NO** usas `--copy`, el script ejecuta ffmpeg con estas decisiones principales:

- Video: `libx264` con `--crf` y `--preset` (default `crf=20`, `preset=medium`)
- Audio: `aac` a `192k`
- Subtítulos: intenta mantenerlos con `-c:s copy`
- Web playback: `-movflags +faststart`
- Sobrescritura: usa `-y` (si el `.mp4` ya existe, lo sobrescribe)
- Salida: si no indicas `-o`, usa el mismo nombre con extensión `.mp4`

---

## Ver ayuda

```bash
python mov2mp4.py --help
```

---

## Troubleshooting

- **`ERROR: ffmpeg no está instalado o no está en el PATH.`**  
  Instala ffmpeg y verifica con `ffmpeg -version`.

- **Falla con `--copy`**  
  `--copy` solo funciona cuando los streams ya son compatibles con MP4. Si falla, vuelve a intentar **sin** `--copy` para re-codificar.

- **Rutas con espacios (Windows/macOS)**  
  Usa comillas:
  ```bash
  python mov2mp4.py "C:\Videos\Mi video.mov"
  ```

---

## Licencia

MIT (ver `LICENSE`).
