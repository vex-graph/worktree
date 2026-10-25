"""Forwarding runner for tools/python/test_checklist.py."""
from pathlib import Path

_source = Path(__file__).resolve().parent / "python" / "test_checklist.py"
exec(compile(_source.read_text(encoding="utf-8"), str(_source), "exec"))
