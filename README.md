# mov2mp4
Script que convierte `.mov` a `.mp4` usando **ffmpeg** (vía subprocess)

## Cómo usarlo

Requisito: tener **ffmpeg** instalado y en el PATH.

### Casos típicos:

* Convertir un archivo:

`python mov2mp4.py video.mov`

* Especificar salida y ajustar calidad/preset:

`python mov2mp4.py entrada.mov -o salida.mp4 --crf 20 --preset slow`

* Copiar streams (sin re-encode) si ya son H.264/AAC:

`python mov2mp4.py entrada.mov --copy`

* Convertir todos los `.mov` en una carpeta (recursivo):

`python mov2mp4.py /ruta/a/carpeta --recursive`

* Pasar flags extra directamente a **ffmpeg** (lo que se ponga después de `--extra` se pasa tal cual):

`python mov2mp4.py entrada.mov --extra -vf scale=1280:-2`

## Qué hace por defecto

* Re-codifica a H.264 (libx264) + AAC para máxima compatibilidad.

* Usa `-movflags +faststart` para que el MP4 cargue más rápido en la web.

* Mantiene subtítulos si existen (`-c:s copy`).

* Se puede ajustar la calidad con `--crf` (18–23 recomendado) y velocidad/eficiencia con `--preset` (de `ultrafast` a `placebo`).
