import argparse
from .io import read_skus
from .scraper import scrape_images_for_skus

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="hp-sku-scraper")
    p.add_argument("--skus", required=True, help="Path to txt file with SKUs (one per line).")
    p.add_argument("--out", default="images", help="Output directory for images.")
    p.add_argument("--headless", action="store_true", help="Run browser headless.")
    return p

def main() -> int:
    args = build_parser().parse_args()
    skus = read_skus(args.skus)

    results = scrape_images_for_skus(skus, out_dir=args.out, headless=args.headless)

    ok = sum(1 for v in results.values() if v == "downloaded")
    print(f"Done. downloaded={ok}/{len(results)}")

    for sku, status in results.items():
        if status != "downloaded":
            print(f"{sku}: {status}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
