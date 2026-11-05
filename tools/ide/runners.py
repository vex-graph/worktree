#!/usr/bin/env python3
"""Regenerate the CLion run list from b.assembly.json.

b is the only runner. CMake in this workspace is IDE metadata: colours, symbol
resolution, inlay hints and debug info. It deliberately creates no executable
or test target, so CLion has nothing else to offer in the run dropdown.

Shared configurations produced here:

    b: build all    one dependency-ordered `b build` per unit
    b: <unit>       `b run <unit>` for every unit of type app or executable

`b build` takes one unit per invocation, so the build-all script chains the
order the assembly already declares instead of inventing a second one.

Usage:
    python3 tools/ide/runners.py            # write .idea/runConfigurations
    python3 tools/ide/runners.py --check    # fail if the files are stale
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from xml.sax.saxutils import escape

RUNNABLE_TYPES = {"app", "executable"}
PREFIX = "b_"
BUILD_ORDER_FILE = "b_build.xml"

TEMPLATE = """<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="{name}" type="ShConfigurationType" factoryName="Shell Script">
    <option name="SCRIPT_TEXT" value="{script}" />
    <option name="INDEPENDENT_SCRIPT_PATH" value="true" />
    <option name="SCRIPT_PATH" value="" />
    <option name="SCRIPT_OPTIONS" value="" />
    <option name="INDEPENDENT_SCRIPT_WORKING_DIRECTORY" value="true" />
    <option name="SCRIPT_WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="INDEPENDENT_INTERPRETER_PATH" value="true" />
    <option name="INTERPRETER_PATH" value="/bin/zsh" />
    <option name="INTERPRETER_OPTIONS" value="" />
    <option name="EXECUTE_IN_TERMINAL" value="true" />
    <option name="EXECUTE_SCRIPT_FILE" value="false" />
    <envs />
    <method v="2" />
  </configuration>
</component>
"""


def configuration(name: str, script: str) -> str:
    quoted = {'"': "&quot;"}
    return TEMPLATE.format(name=escape(name, quoted), script=escape(script, quoted))


def build_order(assembly: dict) -> list[str]:
    """Dependencies before dependents; assembly order breaks ties."""
    order: list[str] = []
    visiting: set[str] = set()

    def visit(unit: str) -> None:
        if unit in order or unit in visiting:
            return
        visiting.add(unit)
        for dep in assembly.get(unit, {}).get("deps", []):
            if dep in assembly:
                visit(dep)
        visiting.discard(unit)
        order.append(unit)

    for unit in assembly:
        visit(unit)
    return order


def wanted(root: Path) -> dict[str, str]:
    assembly = json.loads((root / "b.assembly.json").read_text(encoding="utf-8"))["assembly"]

    steps = [f"./tools/b build {unit}" for unit in build_order(assembly)]
    configs = {BUILD_ORDER_FILE: configuration("b: build all", " && ".join(steps))}

    for unit, record in sorted(assembly.items()):
        if record.get("type") not in RUNNABLE_TYPES:
            continue
        configs[f"{PREFIX}{unit}.xml"] = configuration(f"b: {unit}", f"./tools/b run {unit}")
    return configs


def main(argv: list[str]) -> int:
    check = "--check" in argv
    root = Path(__file__).resolve().parents[2]
    directory = root / ".idea" / "runConfigurations"
    configs = wanted(root)

    stale: list[str] = []
    for filename, body in configs.items():
        path = directory / filename
        if not path.exists() or path.read_text(encoding="utf-8") != body:
            stale.append(filename)
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body, encoding="utf-8")

    if directory.exists():
        for path in sorted(directory.glob(f"{PREFIX}*.xml")):
            if path.name not in configs:
                stale.append(path.name)
                if not check:
                    path.unlink()

    if check and stale:
        print("stale run configurations: " + ", ".join(stale), file=sys.stderr)
        return 1
    print(f"b runners: {len(configs)} ({', '.join(sorted(configs))})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
