#!/usr/bin/env python3
"""
mov2mp4.py — Convert .mov to .mp4 (H.264 + AAC) using ffmpeg

Requirements:
  - ffmpeg installed and available in PATH (https://ffmpeg.org/)

Features:
  - Single file or whole directory conversion
  - Re-encodes video to H.264 (libx264) and audio to AAC for broad compatibility
  - Adds +faststart (moves moov atom) for web playback
  - Optional stream copy when input already uses H.264/AAC (-c copy)
  - Customizable CRF and preset
Usage:
  python mov2mp4.py input.mov
  python mov2mp4.py /path/to/folder --recursive
  python mov2mp4.py input.mov -o output.mp4 --crf 20 --preset slow
  python mov2mp4.py input.mov --copy
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

def which_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if not exe:
        sys.stderr.write("ERROR: ffmpeg no está instalado o no está en el PATH.\n")
        sys.stderr.write("Instálalo desde https://ffmpeg.org/ y vuelve a intentar.\n")
        sys.exit(1)
    return exe

def build_cmd(ffmpeg: str, inp: Path, out: Path, *, copy: bool, crf: int, preset: str, extra: list[str]) -> list[str]:
    # Base command
    cmd = [ffmpeg, "-y", "-i", str(inp)]

    if copy:
        # Stream copy when codecs are already compatible
        cmd += ["-c", "copy"]
    else:
        # Re-encode: H.264 + AAC for maximum compatibility
        cmd += [
            "-c:v", "libx264",
            "-crf", str(crf),
            "-preset", preset,
            "-c:a", "aac",
            "-b:a", "192k",
        ]

    # Keep subtitles if present (copy is fine for text subs)
    cmd += ["-c:s", "copy"]
    # Optimize for web: place moov atom at the front
    cmd += ["-movflags", "+faststart"]

    # Any extra raw ffmpeg args
    if extra:
        cmd += extra

    cmd += [str(out)]
    return cmd

def convert_file(inp: Path, out: Path | None, *, copy: bool, crf: int, preset: str, extra: list[str]) -> bool:
    ffmpeg = which_ffmpeg()

    if out is None:
        out = inp.with_suffix(".mp4")
    else:
        out = Path(out)

    # Ensure output directory exists
    out.parent.mkdir(parents=True, exist_ok=True)

    cmd = build_cmd(ffmpeg, inp, out, copy=copy, crf=crf, preset=preset, extra=extra)
    print("Ejecutando:", " ".join(map(str, cmd)))

    try:
        subprocess.run(cmd, check=True)
        print(f"✔ Convertido: {inp.name}  →  {out.name}")
        return True
    except subprocess.CalledProcessError as e:
        sys.stderr.write(f"✖ Falló la conversión de {inp}: {e}\n")
        return False

def iter_mov_files(root: Path, recursive: bool) -> list[Path]:
    if root.is_file():
        return [root]
    if recursive:
        return [p for p in root.rglob("*.mov")]
    else:
        return [p for p in root.glob("*.mov")]

def main():
    parser = argparse.ArgumentParser(description="Convierte .mov a .mp4 (H.264 + AAC) usando ffmpeg.")
    parser.add_argument("input", help="Archivo .mov o carpeta con .mov")
    parser.add_argument("-o", "--output", help="Archivo .mp4 de salida (solo en modo de archivo único)")
    parser.add_argument("--copy", action="store_true", help="Intentar copia de streams (-c copy) si ya son H.264/AAC")
    parser.add_argument("--crf", type=int, default=20, help="Calidad CRF (18-23 es un rango típico). Default: 20")
    parser.add_argument("--preset", default="medium", help="Preset de x264 (ultrafast..placebo). Default: medium")
    parser.add_argument("--recursive", action="store_true", help="Buscar .mov recursivamente en subcarpetas (si input es carpeta)")
    parser.add_argument("--extra", nargs=argparse.REMAINDER, help="Argumentos extra para ffmpeg (todo lo que siga se pasa tal cual)")

    args = parser.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        sys.stderr.write(f"ERROR: No existe la ruta: {inp}\n")
        sys.exit(1)

    # If input is a file, allow -o
    if inp.is_file():
        if args.output:
            out = Path(args.output)
            if out.suffix.lower() != ".mp4":
                out = out.with_suffix(".mp4")
        else:
            out = None

        extra = args.extra if args.extra else []
        ok = convert_file(inp, out, copy=args.copy, crf=args.crf, preset=args.preset, extra=extra)
        sys.exit(0 if ok else 2)

    # If input is a directory, batch convert
    movs = iter_mov_files(inp, recursive=args.recursive)
    if not movs:
        print("No se encontraron archivos .mov.")
        sys.exit(0)

    failures = 0
    for f in movs:
        # Output file alongside input, same name with .mp4
        ok = convert_file(f, None, copy=args.copy, crf=args.crf, preset=args.preset, extra=(args.extra or []))
        failures += (0 if ok else 1)

    if failures:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
