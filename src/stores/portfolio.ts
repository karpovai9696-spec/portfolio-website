import { defineStore } from 'pinia'

/* ============================ Типы ============================ */

export interface Project {
  id: number
  title: string
  description: string
  stack: string[]
  category: 'vue' | 'react' | 'fullstack'
  /** Тип CSS-превью: тёмная админка или терминал с логами */
  mock: 'admin' | 'terminal'
  demoUrl: string
  codeUrl: string
}

export interface SkillCategory {
  title: string
  items: string[]
}

export interface SkillLevel {
  name: string
  level: number
  label: 'Expert' | 'Advanced' | 'Intermediate' | 'Basic'
}

export interface Service {
  id: number
  title: string
  description: string
  icon: string
}

export interface ExperienceItem {
  id: number
  role: string
  place: string
  period: string
  location: string
  points: string[]
}

export interface EducationItem {
  id: number
  title: string
  organization: string
  period: string
}

/* ============================ Store ============================ */

export const usePortfolioStore = defineStore('portfolio', {
  state: () => ({
    /* ---------- Личная информация ---------- */
    person: {
      name: 'Михаил Карпов',
      fullName: 'Карпов Михаил Андреевич',
      role: 'Full Stack Developer',
      age: 23,
      city: 'Казань, Россия',
      languages: 'Русский (родной)',
      email: 'mikhail.karpov.03@internet.ru',
      telegram: 'https://t.me/Phoenix9696',
      telegramNick: '@Phoenix9696',
      phone: '8 909 308 77 67',
      phoneHref: 'tel:+79093087767',
      workHours: 'Пн–Пт, 10:00–19:00 МСК',
      photo: 'images/photo.png',
      resume: 'resume.pdf',
      tagline:
        'Разрабатываю современные веб-приложения на Vue.js и React — от лендингов до сложных SPA. ' +
        'Специализируюсь на производительных и удобных интерфейсах, которые нравятся пользователям и приносят результат бизнесу. ' +
        'Люблю чистый код, следую лучшим практикам и всегда довожу проекты до результата.',
      aboutText: [
        'Меня зовут Михаил, я Full Stack Developer из Казани. Занимаюсь разработкой веб-приложений более двух лет: проектирую интерфейсы на Vue 3 и React, создаю серверную часть на Node.js и Python, работаю с базами данных.',
        'Начинал с учебных проектов в техникуме, сейчас работаю на фрилансе и развиваю собственные проекты. За это время реализовал SPA с нуля, проектировал REST API, подключал сторонние сервисы — платёжные системы, CRM и карты.',
        'Постоянно учусь: слежу за развитием экосистемы Vue и React, изучаю инструменты DevOps и облачные технологии. Верю, что хороший код — это код, который легко читать и поддерживать.',
      ],
      qualities: [
        'Ответственность',
        'Коммуникабельность',
        'Внимание к деталям',
        'Постоянное обучение',
      ],
    },

    /* ---------- Услуги ---------- */
    services: [
      {
        id: 1,
        title: 'Лендинги и сайты-визитки',
        description:
          'Быстрые и эффектные одностраничные сайты для презентации услуг, продукта или личного бренда. Адаптивная вёрстка и высокая скорость загрузки.',
        icon: 'Globe',
      },
      {
        id: 2,
        title: 'Веб-приложения (SPA)',
        description:
          'Одностраничные приложения на Vue 3 или React с продуманной архитектурой, управлением состоянием и удобным интерфейсом.',
        icon: 'MonitorSmartphone',
      },
      {
        id: 3,
        title: 'Интернет-магазины',
        description:
          'Каталог, корзина, оформление заказа и подключение оплаты. Магазин, которым удобно пользоваться и легко управлять.',
        icon: 'ShoppingCart',
      },
      {
        id: 4,
        title: 'Доработка и поддержка проектов',
        description:
          'Разберусь в существующем коде, исправлю ошибки, добавлю новый функционал и возьму проект на регулярную поддержку.',
        icon: 'Wrench',
      },
      {
        id: 5,
        title: 'Адаптивная вёрстка',
        description:
          'Pixel-perfect вёрстка по макетам Figma. Сайт будет одинаково хорошо выглядеть на телефоне, планшете и десктопе.',
        icon: 'Smartphone',
      },
      {
        id: 6,
        title: 'Интеграция с API / CRM',
        description:
          'Подключение платёжных систем, CRM, карт, служб доставки и других сторонних сервисов к вашему сайту или приложению.',
        icon: 'Blocks',
      },
      {
        id: 7,
        title: 'SEO-оптимизация',
        description:
          'Техническая оптимизация: мета-теги, семантическая разметка, скорость загрузки — чтобы сайт лучше ранжировался в поиске.',
        icon: 'Search',
      },
    ] as Service[],

    /* ---------- Навыки по категориям ---------- */
    skillCategories: [
      {
        title: 'Frontend',
        items: [
          'Vue 3',
          'React',
          'TypeScript',
          'JavaScript',
          'HTML5',
          'CSS3',
          'Tailwind CSS',
          'Sass/SCSS',
          'Nuxt.js',
        ],
      },
      {
        title: 'Backend',
        items: ['Node.js', 'Python', 'Express', 'FastAPI'],
      },
      {
        title: 'Базы данных',
        items: ['PostgreSQL', 'MySQL', 'MongoDB', 'Redis'],
      },
      {
        title: 'Инструменты',
        items: ['Git', 'Docker', 'Vite', 'Webpack', 'Linux', 'npm/yarn'],
      },
      {
        title: 'CI/CD и облака',
        items: ['GitHub Actions', 'GitLab CI', 'AWS', 'Vercel', 'Netlify'],
      },
    ] as SkillCategory[],

    /* ---------- Уровни владения (прогресс-бары) ---------- */
    skillLevels: [
      { name: 'JavaScript', level: 95, label: 'Expert' },
      { name: 'TypeScript', level: 92, label: 'Expert' },
      { name: 'Vue.js', level: 90, label: 'Expert' },
      { name: 'React', level: 85, label: 'Advanced' },
      { name: 'Node.js', level: 80, label: 'Advanced' },
      { name: 'Python', level: 75, label: 'Advanced' },
      { name: 'Docker', level: 65, label: 'Intermediate' },
      { name: 'PostgreSQL', level: 60, label: 'Intermediate' },
      { name: 'AWS', level: 55, label: 'Intermediate' },
      { name: 'Go', level: 45, label: 'Basic' },
      { name: 'Kubernetes', level: 40, label: 'Basic' },
      { name: 'GraphQL', level: 35, label: 'Basic' },
    ] as SkillLevel[],

    /* ---------- Портфолио ---------- */
    projects: [
      {
        id: 1,
        title: 'Агрегатор АМДЛП',
        description:
          'Система мониторинга движения лекарственных препаратов. Криптография, УКЭП, логирование.',
        stack: ['Web', 'Integration', 'Sec'],
        category: 'fullstack',
        mock: 'admin',
        demoUrl: '#',
        codeUrl: 'https://github.com/karpovai9696-spec',
      },
      {
        id: 2,
        title: 'Интеграционные шлюзы',
        description:
          'Шлюзы обмена данными с государственными системами: маркировка, очереди запросов, ретраи и аудит операций.',
        stack: ['Go', 'Python', 'REST', 'Docker'],
        category: 'fullstack',
        mock: 'terminal',
        demoUrl: '#',
        codeUrl: 'https://github.com/karpovai9696-spec',
      },
    ] as Project[],

    /* ---------- Опыт (таймлайн) ---------- */
    experience: [
      {
        id: 1,
        role: 'Full Stack Developer',
        place: 'Фриланс / собственные проекты',
        period: '2023 — настоящее время',
        location: 'Казань / Remote',
        points: [
          'Разработка SPA на Vue 3 и React с нуля',
          'Проектирование REST API на Node.js/Express',
          'Адаптивная вёрстка по макетам Figma',
          'Интеграция сторонних API: оплата, CRM, карты',
          'Оптимизация производительности: lazy loading, code splitting',
        ],
      },
      {
        id: 2,
        role: 'Техник-программист',
        place: 'Обучение и практика',
        period: '2019 — 2023',
        location: 'Калачёвский техникум-интернат',
        points: [
          'Изучение основ программирования и баз данных',
          'Учебные проекты на JavaScript',
          'Дипломный проект — веб-приложение',
        ],
      },
    ] as ExperienceItem[],

    /* ---------- Образование ---------- */
    education: [
      {
        id: 1,
        title: 'Техник-программист',
        organization: 'Калачёвский техникум-интернат',
        period: '2019 — 2023',
      },
      {
        id: 2,
        title: 'JavaScript/TypeScript',
        organization: 'Stepik',
        period: '2022',
      },
      {
        id: 3,
        title: 'Vue.js 3 — полный курс',
        organization: 'Udemy',
        period: '2023',
      },
      {
        id: 4,
        title: 'React — полное руководство',
        organization: 'Udemy',
        period: '2024',
      },
    ] as EducationItem[],
  }),

  getters: {
    /** Проекты, отфильтрованные по категории ('all' — все) */
    filteredProjects: (state) => {
      return (filter: string): Project[] => {
        if (filter === 'all') return state.projects
        return state.projects.filter((p) => p.category === filter)
      }
    },
  },
})
