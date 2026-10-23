"""Визуальная проверка секции ScrollScenes после багфикса.

- десктоп 1440x900 и мобильная 390x844;
- 4 сцены вниз + реверс вверх (проверка гонок onComplete и сброса yPercent);
- стресс: быстрые прыжки по сегментам (реверсы на лету), затем контрольный кадр;
- для каждого кадра проверяются инварианты: активный .frame виден,
  его .wipe в scaleX(0), .zoom без scale/yPercent.

Запуск: python _verify_scroll_scenes.py
Сервер останавливается по завершении (taskkill /T по дереву процессов).
"""
import re
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

FAILURES: list[str] = []


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


def stories_geo(page):
    return page.evaluate(
        """() => {
            const el = document.querySelector('.stories');
            const r = el.getBoundingClientRect();
            return { top: r.top + window.scrollY, height: el.offsetHeight,
                     vh: window.innerHeight };
        }"""
    )


def scroll_to_scene(page, geo, prog: float, settle_ms: int = 1800) -> None:
    span = geo["height"] - geo["vh"]
    y = geo["top"] + span * prog
    page.evaluate(f"window.scrollTo(0, {y})")
    page.wait_for_timeout(settle_ms)


def check_active_frame(page, tag: str) -> None:
    """Инварианты активного кадра: виден, шторка ушла, контент без scale/сдвига."""
    st = page.evaluate(
        """() => {
            const idx = parseInt(document.querySelector('.stories .pnum b').textContent, 10) - 1;
            const frames = [...document.querySelectorAll('.stories .frame')];
            const f = frames[idx];
            const cs = getComputedStyle(f);
            const wipe = getComputedStyle(f.querySelector('.wipe'));
            const zoom = getComputedStyle(f.querySelector('.zoom'));
            return { idx, vis: cs.visibility, wipe: wipe.transform, zoom: zoom.transform,
                     kicker: document.querySelector('.stories .kicker').textContent };
        }"""
    )
    ok = True
    if st["vis"] != "visible":
        ok = False
    # matrix(a,b,c,d,tx,ty): scaleX(0) -> a==0; scale 1 без сдвига -> a==1, tx==ty==0
    for key, want_a in (("wipe", 0.0), ("zoom", 1.0)):
        t = st[key]
        if t == "none":
            if want_a != 1.0:
                ok = False
            continue
        m = re.match(r"matrix\(([^)]+)\)", t)
        if not m:
            ok = False
            continue
        vals = [float(x) for x in m.group(1).split(",")]
        if abs(vals[0] - want_a) > 0.02:
            ok = False
        if key == "zoom" and (abs(vals[4]) > 2 or abs(vals[5]) > 2):
            ok = False  # остаточный сдвиг контента
    status = "OK " if ok else "FAIL"
    print(f"  [{status}] {tag}: idx={st['idx']} vis={st['vis']} wipe={st['wipe']} zoom={st['zoom']}")
    if not ok:
        FAILURES.append(f"{tag}: {st}")


def run(page, prefix: str) -> None:
    geo = stories_geo(page)
    print(f"{prefix} stories:", geo)
    # --- вниз: 4 сцены ---
    for name, prog in [("scene1", 0.04), ("scene2", 0.30), ("scene3", 0.55), ("scene4", 0.82)]:
        scroll_to_scene(page, geo, prog)
        page.screenshot(path=str(SHOTS / f"{prefix}-{name}.png"))
        check_active_frame(page, f"{prefix}-{name}")
    # --- реверс вверх: сцены 3→2→1 ---
    for name, prog in [("scene3-back", 0.55), ("scene2-back", 0.30), ("scene1-back", 0.04)]:
        scroll_to_scene(page, geo, prog)
        page.screenshot(path=str(SHOTS / f"{prefix}-{name}.png"))
        check_active_frame(page, f"{prefix}-{name}")
    # --- стресс: быстрые прыжки с реверсами на лету (гонки переходов) ---
    span = geo["height"] - geo["vh"]
    for prog in [0.82, 0.30, 0.55, 0.04, 0.55]:
        page.evaluate(f"window.scrollTo(0, {geo['top'] + span * prog})")
        page.wait_for_timeout(120)  # резко, не давая доиграть таймлайнам
    page.wait_for_timeout(2000)  # последний переход доигрывает
    page.screenshot(path=str(SHOTS / f"{prefix}-stress.png"))
    check_active_frame(page, f"{prefix}-stress(ожидается scene3)")


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
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(BASE, wait_until="networkidle")
            page.wait_for_timeout(2500)
            run(page, "d")
            page.close()
            mob = browser.new_page(viewport={"width": 390, "height": 844})
            mob.goto(BASE, wait_until="networkidle")
            mob.wait_for_timeout(2500)
            run(mob, "m")
            mob.close()
            browser.close()
        if FAILURES:
            print("\nИНВАРИАНТЫ НАРУШЕНЫ:")
            for f in FAILURES:
                print(" -", f)
            return 1
        print("\nВсе инварианты кадров выполнены.")
        return 0
    finally:
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
        print("dev-сервер остановлен")


if __name__ == "__main__":
    sys.exit(main())
