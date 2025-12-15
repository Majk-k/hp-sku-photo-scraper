from pathlib import Path

def read_skus(path: str | Path) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"SKU file not found: {p}")

    skus: list[str] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        skus.append(s)

    if not skus:
        raise ValueError("No SKUs found in the file.")
    return skus
