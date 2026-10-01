# Сайт-визитка — Михаил Карпов

Персональный сайт-визитка фрилансера (Full Stack Developer): услуги, навыки, портфолио, опыт и контактная форма. Тёмная/светлая тема, glassmorphism-дизайн, плавные анимации, полная адаптивность.

## Стек

- **Vue 3** (Composition API, `<script setup>`) + **TypeScript**
- **Vite 5** — сборка и dev-сервер
- **Tailwind CSS 3** — стили (`darkMode: 'class'`)
- **Pinia** — централизованное хранилище контента (`src/stores/portfolio.ts`)
- **Vue Router 4** — маршрутизация (одна страница, якорная навигация)
- **lucide-vue-next** — иконки
- Анимации — CSS + IntersectionObserver (`src/composables/useScrollAnimation.ts`)

## Требования

- Node.js **18.18+** или **20.x** (проверено также на Node 24)
- npm 9+

## Установка и запуск

```bash
npm install        # установка зависимостей
npm run dev        # dev-сервер (по умолчанию http://localhost:5173)
npm run build      # production-сборка в dist/
npm run preview    # предпросмотр production-сборки
npm run lint       # проверка кода ESLint (не ломает сборку)
npm run format     # форматирование Prettier
```

Dev-серверу можно передать другой порт/хост через CLI:

```bash
npm run dev -- --port 7100
npm run dev -- --host 0.0.0.0 --port 7100
```

## Структура проекта

```
public/
  favicon.svg          # SVG-фавикон с инициалами «МК»
  resume.pdf           # резюме (PDF-заглушка, см. ниже)
  images/photo.jpg     # фото владельца
src/
  assets/styles/main.css     # Tailwind + кастомные стили (glassmorphism, анимации)
  components/common/         # Button, Card, SectionTitle
  components/layout/         # Header, Footer, Navigation
  components/sections/       # Hero, About, Services, Skills, Portfolio, Experience, Contact
  composables/useScrollAnimation.ts  # анимация появления при скролле
  router/index.ts            # роутер с плавной прокруткой к якорям
  stores/portfolio.ts        # ВЕСЬ контент сайта (Pinia)
  views/Home.vue
  App.vue, main.ts
```

## Как редактировать контент

Практически весь текст сайта лежит в одном файле — **`src/stores/portfolio.ts`**:

- `person` — имя, контакты, описание, качества;
- `services` — карточки услуг (поле `icon` — имя иконки из [lucide](https://lucide.dev/icons), зарегистрируйте её в `iconMap` в `src/components/sections/Services.vue`);
- `skillCategories` / `skillLevels` — навыки и прогресс-бары;
- `projects` — портфолио;
- `experience` / `education` — таймлайн опыта и образование.

### Как заменить демо-проекты портфолио на реальные

1. Откройте `src/stores/portfolio.ts`, массив `projects`.
2. Замените `title`, `description`, `stack`, `category` (`vue` / `react` / `fullstack` — влияет на фильтр).
3. Пропишите реальные ссылки в `demoUrl` и `codeUrl`.
4. В `src/components/sections/Portfolio.vue` у кнопок «Демо»/«Код» уберите `@click.prevent` и класс `cursor-not-allowed`, чтобы ссылки стали активными.
5. Чтобы использовать настоящий скриншот вместо градиентной заглушки: положите изображение в `public/images/`, добавьте поле `image` в объект проекта и в шаблоне замените блок с градиентом на `<img :src="project.image" ...>`.

### Как заменить резюме

Просто перезапишите файл **`public/resume.pdf`** своим PDF (имя файла сохраните). Ссылка «Скачать резюме» в Hero уже указывает на `/resume.pdf`.

### Как заменить фото

Перезапишите файл **`public/images/photo.jpg`** (рекомендуется квадратное фото, например 640×640). Имя файла сохраните — оно используется в секции «Обо мне» и в Open Graph.

## Тема оформления

Тёмная тема включена по умолчанию. Переключатель — в шапке сайта; выбор сохраняется в `localStorage` (ключ `theme`). Класс `dark` применяется inline-скриптом в `index.html` до отрисовки страницы, поэтому мигания при загрузке нет.

## Анимации и интерактив

Сайт — демонстрация анимационных возможностей (CSS + IntersectionObserver + pointer events; WebGL — Three.js, инертный скролл — Lenis, оба грузятся динамически отдельными чанками):

- **Hero WebGL:** интерактивное поле частиц с волновой деформацией и repel-эффектом от курсора (`ParticleField.vue`); Three.js подгружается async, DPR ≤ 2, пауза при скрытой вкладке / вне viewport / в светлой теме, на мобильных — уменьшенная сетка;
- **Кинетическая типографика:** имя в Hero появляется по буквам с маской, заголовки секций — по словам; ghost-заголовки («УСЛУГИ», «НАВЫКИ»…) с scroll-параллаксом;
- **Инертный скролл:** Lenis (`useLenis.ts`), якорная навигация через `scrollToTarget`; при reduced-motion — нативный скролл;
- **Hero:** aurora/gradient-mesh фон, печатающийся текст (ротация специализаций), магнитные кнопки, анимированный scroll-индикатор;
- **Cursor-glow:** световое пятно за курсором (только устройства с мышью);
- **Scroll-reveal:** появление секций с направлениями (снизу/слева/справа) и staggered-задержками (`useScrollAnimation.ts` + `staggerStyle`);
- **Текстура:** film-grain noise overlay (SVG feTurbulence, opacity ~0.04);
- **Параллакс:** фото в «Обо мне» и превью проектов при скролле (`useParallax.ts`);
- **Marquee:** бесконечная бегущая строка технологий с паузой при наведении;
- **Услуги:** 3D-tilt карточек и spotlight-эффект за курсором;
- **Навыки/статистика:** прогресс-бары и счётчики, анимирующиеся при попадании в viewport;
- **Опыт:** таймлайн с «прорисовывающейся» линией и светящимися узлами;
- **Навигация:** scrollspy-подсветка активной секции, прогресс-бар чтения в шапке, градиентный underline у ссылок;
- **Контакты:** плавающие лейблы и градиентные focus-рамки полей;
- **Footer:** плавающая кнопка «Наверх», появляющаяся после прокрутки.

Все анимации отключаются при `prefers-reduced-motion` (WebGL не инициализируется вовсе); pointer-эффекты (tilt, magnetic, cursor-glow) — на тач-устройствах.

## Деплой

Сборка `npm run build` создаёт статические файлы в `dist/` — их можно разместить на любом статическом хостинге (Vercel, Netlify, GitHub Pages, nginx и т.д.).
