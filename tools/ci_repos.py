"""Forwarding runner for tools/python/ci_repos.py."""
from pathlib import Path

_source = Path(__file__).resolve().parent / "python" / "ci_repos.py"
exec(compile(_source.read_text(encoding="utf-8"), str(_source), "exec"))
