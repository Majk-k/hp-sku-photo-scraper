# HP SKU Photo Scraper

Python CLI tool for downloading product images for HP SKUs from HP Shop search results.

## Features
- Reads SKUs from a text file
- Handles HP privacy and location popups
- Downloads product images as PNG
- Headless or visible browser mode
- Simple CLI

## Project structure
```
TBD
```

## Requirements
- Python 3.10+
- Google Chrome
- ChromeDriver is downloaded automatically via webdriver-manager

## Installation
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate

pip install -U pip
pip install .
```

## Uninstallation
```bash
pip uninstall hp-sku-photo-scraper
# To remove the virtual environment entirely:
deactivate
rm .venv -r -fo
```

## Usage

Create a file with SKUs, e.g. `data/skus.txt`:
```
40Q51A
6GX01F
```

Run:
```bash
hp-sku-scraper --skus data/skus.txt --out images --headless
```

Arguments:
- `--skus` : path to text file with SKUs (required)
- `--out` : output directory for images (default: `images`)
- `--headless` : run browser in headless mode

## Output
Images are saved as:
```
images/
├─ 40Q51A.png
└─ 6GX01F.png
```

## Notes
- The scraper depends on the current HP Shop HTML structure.
- XPath selectors may need updates if the website changes.
- Intended for educational and portfolio use.

## License
MIT
