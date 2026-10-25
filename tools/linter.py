"""Forwarding runner for tools/python/linter.py."""
from pathlib import Path

_source = Path(__file__).resolve().parent / "python" / "linter.py"
exec(compile(_source.read_text(encoding="utf-8"), str(_source), "exec"))
