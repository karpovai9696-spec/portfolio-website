# Подключение GitHub Pages (зеркало сайта)

Цель: сайт будет доступен по адресу `https://karpovai9696-spec.github.io/portfolio-website`
как запасное зеркало основного https://yq2no6cpbdyom.kimi.page

## Почему нужны ручные шаги

OAuth-токен GitHub-плагина не имеет scope `workflow` (GitHub запрещает пушить
`.github/workflows/*` без него), а настройки репозитория (видимость, Pages)
через плагин недоступны. Файл workflow уже подготовлен локально:
`.github/workflows/deploy.yml` — осталось добавить его в репозиторий.

## Путь A — через браузер (~5 минут, без установки чего-либо)

1. **Загрузить workflow**: открыть https://github.com/karpovai9696-spec/portfolio-website
   → Add file → Upload files → перетащить локальный файл
   `Сайт Визитка/.github/workflows/deploy.yml` (важно: он должен лечь именно в
   `.github/workflows/deploy.yml` — при загрузке в поле имени можно вписать
   `.github/workflows/deploy.yml`). Commit changes.
2. **Загрузить бинарные файлы** (без них на зеркале не будет фото и резюме):
   - `public/images/photo.jpg` → загрузить в папку `public/images/`
   - `public/resume.pdf` → в папку `public/`
   (Add file → Upload files внутри нужной папки репозитория)
3. **Сделать репозиторий публичным**: Settings → General → внизу Danger Zone →
   Change repository visibility → Make public → подтвердить.
4. **Включить Pages**: Settings → Pages → Source: **GitHub Actions**.
5. Перейти во вкладку **Actions** — workflow «Deploy to GitHub Pages» запустится
   автоматически после пушей (или запустить вручную: Run workflow).
   Через ~2 минуты сайт будет на `https://karpovai9696-spec.github.io/portfolio-website`.

## Путь B — через GitHub CLI (я всё сделаю сам)

```bash
winget install GitHub.cli
gh auth login   # выбрать GitHub.com → HTTPS → Login via browser
```

После этого скажите «готово» — я сам запушу workflow и бинарные файлы,
сделаю репозиторий публичным (`gh repo edit --visibility public`),
включу Pages (`gh api repos/karpovai9696-spec/portfolio-website/pages`)
и проверю, что зеркало открылось.

## Примечание

В workflow используется `vite build --base=/portfolio-website/`, чтобы ассеты
работали по подпути проекта. Основная сборка для kimi.page (base `/`) не затрагивается.
