from pathlib import Path
from io import BytesIO

import requests
from PIL import Image
from tqdm import tqdm
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from .browser import (
    build_driver,
    dynamic_sleep,
    handle_privacy_popup,
    handle_location_prompt,
)


def _clean_image_url(url: str | None) -> str | None:
    if not url:
        return None
    return url.split("?")[0] if "?" in url else url


def _find_image_url_for_sku(driver, wait, sku: str) -> str | None:
    xpath = f"//img[contains(@data-gtm-id, 'hawksearchResults-{sku}')]"
    el = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    return _clean_image_url(el.get_attribute("src"))


def _download_and_save_png(image_url: str, out_path: Path, timeout: int = 30) -> None:
    r = requests.get(image_url, timeout=timeout)
    r.raise_for_status()

    img = Image.open(BytesIO(r.content))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")


def scrape_images_for_skus(
    skus: list[str],
    out_dir: str | Path,
    headless: bool = True,
    base_url: str = "https://www.hp.com/us-en/shop/sitesearch?keyword={sku}",
) -> dict[str, str]:
    out = Path(out_dir)
    results: dict[str, str] = {}

    driver, wait = build_driver(headless=headless)

    try:
        with tqdm(total=len(skus), desc="Downloading images", unit="sku") as pbar:
            for i, sku in enumerate(skus, start=1):
                step = f"[{i}/{len(skus)}] SKU {sku}"

                try:
                    pbar.set_postfix_str(f"{sku} | open page")
                    tqdm.write(f"{step} – opening search page")
                    driver.get(base_url.format(sku=sku))

                    if i == 1:
                        pbar.set_postfix_str(f"{sku} | popups")
                        tqdm.write(f"{step} – handling initial popups")
                        dynamic_sleep(0.8, 1.5)
                        handle_privacy_popup(wait)
                        handle_location_prompt(wait)
                    else:
                        dynamic_sleep(0.5, 1.2)

                    pbar.set_postfix_str(f"{sku} | locate image")
                    tqdm.write(f"{step} – locating image")
                    try:
                        image_url = _find_image_url_for_sku(driver, wait, sku)
                    except Exception as e:
                        results[sku] = f"not_found: {e}"
                        tqdm.write(f"{step} – image not found")
                        pbar.update(1)
                        continue

                    if not image_url:
                        results[sku] = "not_found: empty_url"
                        tqdm.write(f"{step} – empty image URL")
                        pbar.update(1)
                        continue

                    pbar.set_postfix_str(f"{sku} | download")
                    tqdm.write(f"{step} – downloading image")
                    try:
                        _download_and_save_png(image_url, out / f"{sku}.png")
                        results[sku] = "downloaded"
                        tqdm.write(f"{step} – saved successfully")
                    except Exception as e:
                        results[sku] = f"download_failed: {e}"
                        tqdm.write(f"{step} – download failed")

                    dynamic_sleep(0.5, 1.0)
                    pbar.update(1)

                except Exception as e:
                    results[sku] = f"error: {e}"
                    tqdm.write(f"{step} – unexpected error: {e}")
                    pbar.update(1)

    finally:
        tqdm.write("Closing browser")
        driver.quit()

    tqdm.write("Scraping finished")
    return results
