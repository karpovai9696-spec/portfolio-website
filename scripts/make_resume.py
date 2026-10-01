# -*- coding: utf-8 -*-
"""Генерация одностраничного PDF-резюме (заглушка) для public/resume.pdf."""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "resume.pdf"

# Шрифт с поддержкой кириллицы (системный Arial на Windows)
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))

c = canvas.Canvas(str(OUT), pagesize=A4)
W, H = A4
x = 20 * mm
y = H - 25 * mm

BLUE = (0.23, 0.51, 0.96)
VIOLET = (0.55, 0.36, 0.96)
DARK = (0.12, 0.16, 0.23)
GRAY = (0.42, 0.45, 0.50)

# Шапка с градиентной полосой
c.setFillColorRGB(*BLUE)
c.rect(0, H - 8 * mm, W * 0.6, 8 * mm, stroke=0, fill=1)
c.setFillColorRGB(*VIOLET)
c.rect(W * 0.6, H - 8 * mm, W * 0.4, 8 * mm, stroke=0, fill=1)

c.setFillColorRGB(*DARK)
c.setFont("Arial-Bold", 24)
c.drawString(x, y, "Михаил Карпов")
y -= 9 * mm
c.setFillColorRGB(*BLUE)
c.setFont("Arial-Bold", 13)
c.drawString(x, y, "Full Stack Developer")
y -= 7 * mm
c.setFillColorRGB(*GRAY)
c.setFont("Arial", 10)
c.drawString(x, y, "Казань, Россия  ·  mikhail.karpov.03@internet.ru  ·  8 909 308 77 67  ·  t.me/Phoenix9696")
y -= 12 * mm


def section(title):
    global y
    c.setFillColorRGB(*BLUE)
    c.setFont("Arial-Bold", 12)
    c.drawString(x, y, title.upper())
    y -= 2 * mm
    c.setStrokeColorRGB(*VIOLET)
    c.setLineWidth(1.2)
    c.line(x, y, W - x, y)
    y -= 6 * mm


def text(lines, size=10, gap=5.2):
    global y
    c.setFillColorRGB(*DARK)
    c.setFont("Arial", size)
    for line in lines:
        c.drawString(x, y, line)
        y -= gap * mm
    y -= 3 * mm


section("О себе")
text([
    "Full Stack Developer, 23 года. Разрабатываю современные веб-приложения на Vue.js и React,",
    "специализируюсь на производительных и удобных интерфейсах. Люблю чистый код и лучшие практики.",
])

section("Опыт")
c.setFillColorRGB(*DARK)
c.setFont("Arial-Bold", 10.5)
c.drawString(x, y, "Full Stack Developer — Фриланс / собственные проекты")
c.setFillColorRGB(*GRAY)
c.setFont("Arial", 9.5)
c.drawRightString(W - x, y, "2023 — настоящее время")
y -= 5.5 * mm
text([
    "·  Разработка SPA на Vue 3/React с нуля; проектирование REST API на Node.js/Express",
    "·  Адаптивная вёрстка по макетам Figma; интеграция сторонних API (оплата, CRM, карты)",
    "·  Оптимизация производительности: lazy loading, code splitting",
], size=9.5, gap=5)
c.setFillColorRGB(*DARK)
c.setFont("Arial-Bold", 10.5)
c.drawString(x, y, "Техник-программист — обучение и практика")
c.setFillColorRGB(*GRAY)
c.setFont("Arial", 9.5)
c.drawRightString(W - x, y, "2019 — 2023")
y -= 5.5 * mm
text([
    "·  Калачёвский техникум-интернат: основы программирования и БД, учебные проекты на JavaScript",
    "·  Дипломный проект — веб-приложение",
], size=9.5, gap=5)

section("Навыки")
text([
    "Frontend: Vue 3, React, TypeScript, JavaScript, HTML5, CSS3, Tailwind CSS, Sass/SCSS, Nuxt.js",
    "Backend: Node.js, Python, Express, FastAPI",
    "Базы данных: PostgreSQL, MySQL, MongoDB, Redis",
    "Инструменты: Git, Docker, Vite, Webpack, Linux, npm/yarn",
    "CI/CD и облака: GitHub Actions, GitLab CI, AWS, Vercel, Netlify",
], size=9.5, gap=5)

section("Образование")
text([
    "Калачёвский техникум-интернат, «Техник-программист», 2019–2023",
    "Курсы: JavaScript/TypeScript (Stepik, 2022), Vue.js 3 (Udemy, 2023), React (Udemy, 2024)",
], size=9.5, gap=5)

c.setFillColorRGB(*GRAY)
c.setFont("Arial", 8)
c.drawCentredString(W / 2, 12 * mm, "Резюме — Михаил Карпов · mikhail.karpov.03@internet.ru")

c.showPage()
c.save()
print(f"OK: {OUT}")
