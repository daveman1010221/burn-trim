"""Takes the backends Polar never builds out of the published manifests (README.md).

    python3 trim.py

For each crate below, removes the named optional dependencies' tables and every feature entry that names them
(`dep`, `dep:dep`, `dep/feature`, `dep?/feature`), keeping each feature, emptied if need be, so that every crate that
names a feature still resolves. Run it on pristine published crates; the result is the manifest change, nothing else.
"""

import pathlib
import re

TRIM = {
    "cubecl-0.11.4": ["cubecl-cpu", "cubecl-cuda", "cubecl-hip"],
    "burn-dispatch-0.22.1": ["burn-tch"],
    "burn-signal-0.22.1": ["burn-tch"],
}


def names(entry: str, dep: str) -> bool:
    return entry in (dep, f"dep:{dep}") or entry.startswith((f"{dep}/", f"{dep}?/"))


def trim(text: str, deps: list[str]) -> str:
    out, skipping, in_features = [], False, False
    for line in text.splitlines(keepends=True):
        header = re.match(r"^\[([^\]]+)\]\s*$", line)
        if header:
            table = header.group(1)
            in_features = table == "features"
            skipping = any(re.fullmatch(rf"(target\..+\.)?(dev-|build-)?dependencies\.{re.escape(d)}", table) for d in deps)
        if skipping:
            continue
        if in_features:
            quoted = re.findall(r'"([^"]*)"', line)
            if quoted and any(names(q, d) for q in quoted for d in deps):
                key = re.match(r"^(\s*[\w-]+\s*=\s*\[)(.*?)(\]\s*)$", line)
                if key:
                    kept = [q for q in re.findall(r'"([^"]*)"', key.group(2)) if not any(names(q, d) for d in deps)]
                    line = key.group(1) + ", ".join(f'"{q}"' for q in kept) + key.group(3)
                else:
                    continue
        out.append(line)
    return "".join(out)


for crate, deps in TRIM.items():
    path = pathlib.Path(crate) / "Cargo.toml"
    before = path.read_text()
    after = trim(before, deps)
    left = [d for d in deps if re.search(rf'(^|["\[.:]){re.escape(d)}([/?"\]]|$)', after, re.M)]
    if left:
        raise SystemExit(f"{crate}: still names {left}")
    path.write_text(after)
    print(f"{crate}: removed {', '.join(deps)}")
