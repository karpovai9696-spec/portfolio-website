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
    """Инварианты активного кадра: виден, шторка ушла, контент без scale/сдвига;
    для сцены 01 — фото полностью внутри кадра (contain, без обрезки)."""
    st = page.evaluate(
        """() => {
            const idx = parseInt(document.querySelector('.stories .pnum b').textContent, 10) - 1;
            const frames = [...document.querySelectorAll('.stories .frame')];
            const f = frames[idx];
            const cs = getComputedStyle(f);
            const wipe = getComputedStyle(f.querySelector('.wipe'));
            const zoom = getComputedStyle(f.querySelector('.zoom'));
            const out = { idx, vis: cs.visibility, wipe: wipe.transform, zoom: zoom.transform,
                     kicker: document.querySelector('.stories .kicker').textContent };
            if (idx === 0) {
                const fr = f.getBoundingClientRect();
                const img = f.querySelector('.photo').getBoundingClientRect();
                out.photo = { dL: Math.round(img.left - fr.left), dT: Math.round(img.top - fr.top),
                              dR: Math.round(fr.right - img.right), dB: Math.round(fr.bottom - img.bottom) };
            }
            return out;
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
    # фото целиком внутри кадра (все дельты >= -1px)
    if "photo" in st:
        p = st["photo"]
        if min(p["dL"], p["dT"], p["dR"], p["dB"]) < -1:
            ok = False
    status = "OK " if ok else "FAIL"
    print(f"  [{status}] {tag}: idx={st['idx']} vis={st['vis']} wipe={st['wipe']} zoom={st['zoom']}"
          + (f" photo={st['photo']}" if "photo" in st else ""))
    if not ok:
        FAILURES.append(f"{tag}: {st}")


def check_stage_fits(page, tag: str) -> None:
    """Мобильный багфикс: зафиксированный stage целиком во вьюпорте (без обрезки снизу)."""
    st = page.evaluate(
        """() => {
            const stage = document.querySelector('.stories .stage');
            const frames = document.querySelector('.stories .frames');
            const sr = stage.getBoundingClientRect();
            const fr = frames.getBoundingClientRect();
            return { vh: window.innerHeight, stageH: Math.round(sr.height),
                     stageTop: Math.round(sr.top), framesBottom: Math.round(fr.bottom),
                     dvh: CSS.supports('height: 100dvh') };
        }"""
    )
    ok = st["stageH"] <= st["vh"] and st["framesBottom"] <= st["vh"]
    status = "OK " if ok else "FAIL"
    print(f"  [{status}] {tag} stage-fits: {st}")
    if not ok:
        FAILURES.append(f"{tag} stage-fits: {st}")


def run(page, prefix: str) -> None:
    geo = stories_geo(page)
    print(f"{prefix} stories:", geo)
    # --- вниз: 4 сцены ---
    for name, prog in [("scene1", 0.04), ("scene2", 0.30), ("scene3", 0.55), ("scene4", 0.82)]:
        scroll_to_scene(page, geo, prog)
        page.screenshot(path=str(SHOTS / f"{prefix}-{name}.png"))
        check_active_frame(page, f"{prefix}-{name}")
        check_stage_fits(page, f"{prefix}-{name}")
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
            # --- десктоп: hero в обеих темах (контраст текста + частицы) ---
            page = browser.new_page(viewport={"width": 1440, "height": 900})
            page.goto(BASE, wait_until="networkidle")
            page.evaluate("document.documentElement.classList.add('dark')")
            page.wait_for_timeout(5000)  # requestIdleCallback(2.5s) + чанк three + частицы
            page.screenshot(path=str(SHOTS / "d-hero-dark.png"))
            # крупный план зоны основного абзаца (левый нижний блок hero)
            page.screenshot(
                path=str(SHOTS / "d-hero-dark-text.png"),
                clip={"x": 0, "y": 520, "width": 760, "height": 380},
            )
            page.evaluate("document.documentElement.classList.remove('dark')")
            page.wait_for_timeout(1200)
            page.screenshot(path=str(SHOTS / "d-hero-light.png"))
            page.evaluate("document.documentElement.classList.add('dark')")
            page.wait_for_timeout(800)
            run(page, "d")
            # --- десктоп: секция в светлой теме ---
            page.evaluate("document.documentElement.classList.remove('dark')")
            page.wait_for_timeout(600)
            page.evaluate("window.scrollTo(0, 0)")
            run(page, "dl")
            page.close()
            # --- мобильная 390x844: тёмная и светлая ---
            mob = browser.new_page(viewport={"width": 390, "height": 844})
            mob.goto(BASE, wait_until="networkidle")
            mob.wait_for_timeout(2500)
            run(mob, "m")
            mob.evaluate("document.documentElement.classList.remove('dark')")
            mob.wait_for_timeout(600)
            mob.evaluate("window.scrollTo(0, 0)")
            run(mob, "ml")
            mob.close()
            # --- низкий вьюпорт 390x700 (имитация панелей моб. браузера) ---
            low = browser.new_page(viewport={"width": 390, "height": 700})
            low.goto(BASE, wait_until="networkidle")
            low.wait_for_timeout(2500)
            run(low, "m700")
            low.close()
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
