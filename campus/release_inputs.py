"""Explicit public download inventory; never recurse into a student's workspace."""
from pathlib import Path

KIT_FILES = (
    'README.md', 'oslab.py', 'web.py', 'Resumen.ps1', 'resumen.bash',
    'resumen.zsh', 'resumen.cmd', 'compose.yaml', 'swarm.yaml',
    'Dockerfile', '.dockerignore',
)


def public_kit_files(directory: Path) -> list[Path]:
    """Allow only reviewed names, with no symlinks or oversized source files."""
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError('El kit debe ser un directorio regular.')
    files = []
    for name in KIT_FILES:
        path = directory / name
        if path.is_symlink() or not path.is_file() or path.stat().st_size > 1_000_000:
            raise ValueError(f'Archivo público del kit ausente o inválido: {name}')
        files.append(path)
    return files
