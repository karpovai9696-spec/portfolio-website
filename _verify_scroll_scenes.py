"""Временная визуальная проверка секции ScrollScenes: dev-сервер + скриншоты 4 сцен и мобильной версии.

Запуск: python _verify_scroll_scenes.py
Сервер останавливается по завершении (taskkill /T по дереву процессов).
"""
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

PROJECT = Path(__file__).parent
SHOTS = PROJECT / "verify-shots"
SHOTS.mkdir(exist_ok=True)
PORT = 7413
BASE = f"http://localhost:{PORT}/"


def wait_server(url: str, timeout: float = 60.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as r:
                body = r.read().decode("utf-8", "ignore")
                if r.status == 200 and "Карпов" in body:
                    return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("dev-сервер не поднялся за 60с (или порт занят чужим приложением)")


def shoot_scenes(page, prefix: str) -> None:
    geo = page.evaluate(
        """() => {
            const el = document.querySelector('.stories');
            const r = el.getBoundingClientRect();
            return { top: r.top + window.scrollY, height: el.offsetHeight,
                     vh: window.innerHeight, scrollMax: document.body.scrollHeight };
        }"""
    )
    print("stories:", geo)
    span = geo["height"] - geo["vh"]  # диапазон скролла, где stage липнет
    # прогресс внутри секции для каждой сцены (после границы сегмента + запас на анимацию)
    for name, prog in [("scene1", 0.04), ("scene2", 0.30), ("scene3", 0.55), ("scene4", 0.82)]:
        y = geo["top"] + span * prog
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(1800)  # wipe 0.7s + zoom 1.1s + запас
        page.screenshot(path=str(SHOTS / f"{prefix}-{name}.png"))
        state = page.evaluate(
            """() => ({
                y: Math.round(window.scrollY),
                kicker: document.querySelector('.stories .kicker')?.textContent,
                counter: document.querySelector('.stories .pnum b')?.textContent,
            })"""
        )
        print(name, state)


def main() -> int:
    proc = subprocess.Popen(
        ["cmd", "/c", "npm", "run", "dev", "--", "--port", str(PORT), "--strictPort"],
        cwd=str(PROJECT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_server(BASE)
        print("dev-сервер поднят")
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # --- десктоп 1440x900 ---
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(BASE, wait_until="networkidle")
            page.wait_for_timeout(2500)  # gsap/lenis динамическими чанками + шрифты
            shoot_scenes(page, "d")
            page.close()
            # --- мобильная 390x844 ---
            mob = browser.new_page(viewport={"width": 390, "height": 844})
            mob.goto(BASE, wait_until="networkidle")
            mob.wait_for_timeout(2500)
            shoot_scenes(mob, "m")
            mob.close()
            browser.close()
        return 0
    finally:
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
            capture_output=True,
        )
        print("dev-сервер остановлен")


if __name__ == "__main__":
    sys.exit(main())
