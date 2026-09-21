"""Attribute a build only to an identified clean checkout, including new inputs."""
from pathlib import Path
import re
import subprocess


def source_commit(root: Path) -> str | None:
    """Unknown, dirty or ignored curricular inputs never receive a clean Git SHA."""
    options = dict(cwd=root, check=True, capture_output=True, text=True, timeout=5)
    try:
        status = subprocess.run(['git', 'status', '--porcelain=v1', '--untracked-files=all'], **options)
        if status.stdout.strip():
            return None
        ignored = subprocess.run(
            ['git', 'ls-files', '--others', '--ignored', '--exclude-standard', '-z', '--',
             'formacion', 'campus'], **options)
        for name in ignored.stdout.split('\0'):
            path = Path(name)
            parts = path.parts
            if '__pycache__' in parts:
                continue
            if (name.startswith('formacion/')
                    and path.suffix.lower() in {'.md', '.json', '.py', '.yaml', '.bash', '.ps1', '.cmd', '.zsh'}):
                return None
            if (name.startswith('campus/locales/')
                    or name.startswith('campus/assets/')
                    or (len(parts) == 2 and parts[0] == 'campus' and path.suffix in {'.py', '.html'})):
                return None
        head = subprocess.run(['git', 'rev-parse', 'HEAD'], **options).stdout.strip()
        return head if re.fullmatch(r'[0-9a-f]{40}', head) else None
    except (OSError, subprocess.SubprocessError):
        return None
