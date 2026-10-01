# ASSETS-TODO — файлы, которые нужно добавить/восстановить вручную

Этот репозиторий загружен через GitHub API (`push_files`), который принимает
только текстовое содержимое. Бинарные файлы через него передать нельзя —
они будут повреждены. Поэтому следующие файлы нужно добавить вручную
(через `git add` + push, GitHub UI upload или релизы).

## package-lock.json (не загружен)

Файл слишком большой (~147 КБ) для передачи через API сообщения —
попытка загрузки оборвалась, повреждённая копия удалена из репозитория.
Восстановление после клонирования:

```bash
npm install   # package-lock.json будет создан заново автоматически
```

Для точной фиксации версий можно скопировать `package-lock.json` из локальной
копии проекта через обычный `git add package-lock.json && git commit && git push`.

## Сайт (бинарные файлы)

| Путь | Что это | Как получить заново |
| --- | --- | --- |
| `public/images/photo.jpg` | Фото владельца (640×640, ч/б), используется в секции «Обо мне» и Open Graph | Скопировать оригинал фото; имя файла сохранить |
| `public/resume.pdf` | Одностраничное резюме (PDF), кнопка «Скачать резюме» в Hero | Сгенерировать: `python scripts/make_resume.py` (нужен reportlab) или положить свой PDF |

## Визитка (папка `vizitka/`, бинарные файлы)

| Путь | Что это | Как получить заново |
| --- | --- | --- |
| `vizitka/media/photo.jpg` | Фото для печатной визитки | Скопировать вручную |
| `vizitka/media/qr.png` | QR-код на сайт-портфолио | Сгенерировать: `python vizitka/make_assets.py` (нужен пакет qrcode) |
| `vizitka/fonts/JetBrainsMono-Var.ttf` | Шрифт JetBrains Mono (variable) | Скачать с Google Fonts |
| `vizitka/fonts/Manrope-Var.ttf` | Шрифт Manrope (variable) | Скачать с Google Fonts |
| `vizitka/fonts/RussoOne.ttf` | Шрифт Russo One | Скачать с Google Fonts |
| `vizitka/fonts/fa-brands-400.ttf` | Font Awesome 6 Brands | Скачать с fontawesome.com |
| `vizitka/fonts/fa-solid-900.ttf` | Font Awesome 6 Solid | Скачать с fontawesome.com |

## Также не загружены (генерируемые артефакты, не нужны в репозитории)

- `vizitka-story.png`, `vizitka.pdf` — результат `python vizitka/render_vizitka.py` (в `.gitignore`);
- `site-bundle.zip`, `mikhail-karpov-site.zip` — архивы сборки (в `.gitignore`);
- `node_modules/`, `dist/` — ставятся/собираются через `npm install` / `npm run build`.
