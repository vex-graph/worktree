"""Forwarding runner for tools/python/spv_header.py."""
from pathlib import Path

_source = Path(__file__).resolve().parent / "python" / "spv_header.py"
exec(compile(_source.read_text(encoding="utf-8"), str(_source), "exec"))
