"""Разовый снимок нижнего ряда портфолио (десктоп dark/light). Сервер гасится в finally."""
import subprocess
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT = Path(__file__).parent
SHOTS = PROJECT / "verify-shots"
PORT = 7413
BASE = f"http://localhost:{PORT}/"


def wait_server(url: str, timeout: float = 60.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                if r.status == 200 and "Карпов" in r.read().decode("utf-8", "ignore"):
                    return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("dev-сервер не поднялся")


proc = subprocess.Popen(
    ["cmd", "/c", "npm", "run", "dev", "--", "--port", str(PORT), "--strictPort"],
    cwd=str(PROJECT),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)
try:
    wait_server(BASE)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto(BASE, wait_until="networkidle")
        page.wait_for_timeout(2000)
        # тёмная: низ сетки портфолио
        page.evaluate(
            "document.querySelectorAll('#portfolio article')[3].scrollIntoView({block:'start'})"
        )
        page.wait_for_timeout(1500)
        page.screenshot(path=str(SHOTS / "d-portfolio-dark-row2.png"))
        # светлая
        page.evaluate("document.documentElement.classList.remove('dark')")
        page.wait_for_timeout(1000)
        page.screenshot(path=str(SHOTS / "dl-portfolio-row2.png"))
        browser.close()
    print("OK")
finally:
    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    print("dev-сервер остановлен")
