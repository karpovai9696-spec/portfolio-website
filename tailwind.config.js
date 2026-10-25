/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // High-tech yellow — основной акцент (тёмная тема)
        primary: {
          DEFAULT: '#FCD116',
          hover: '#E3BC0E',
          soft: '#FCD116',
        },
        // Тёмное золото — акцент для текста на светлой теме и вторичные метки
        accent: '#8E751D',
        gold: '#8E751D',
        golddeep: '#6B5A17',
        // Cyber-палитра (тёмная тема)
        cyber: {
          bg: '#09090A',
          card: '#17171A',
          text: '#FFF5B8',
          muted: '#3F3820',
        },
        // Светлая тема — производная: тёплый кремовый фон, тёмные чернила
        paper: {
          DEFAULT: '#FFFDF0',
          soft: '#FFF8D6',
          raised: '#FFFEF6',
        },
        ink: {
          50: '#6B6552',
          100: '#6B6552',
          300: '#B9B28F', // приглушённый текст на тёмном (~7.5:1 на #09090A)
          400: '#8F8A6E',
          500: '#6B6552',
          700: '#2E2C1E', // основной текст на светлом (~12:1 на #FFFDF0)
          800: '#1F1F23',
          900: '#17171A',
          950: '#09090A',
        },
        hairline: '#E6E0C2',
      },
      fontFamily: {
        display: ['Montserrat', 'Inter', 'system-ui', 'sans-serif'],
        sans: [
          'Inter',
          'system-ui',
          '-apple-system',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'sans-serif',
        ],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'Menlo', 'monospace'],
      },
      keyframes: {
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-12px)' },
        },
        marquee: {
          '0%': { transform: 'translateX(0)' },
          '100%': { transform: 'translateX(-50%)' },
        },
        blink: {
          '0%, 45%': { opacity: '1' },
          '50%, 95%': { opacity: '0' },
        },
        'scroll-dot': {
          '0%': { transform: 'translateY(0)', opacity: '1' },
          '70%': { transform: 'translateY(14px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '0' },
        },
        'pulse-ring': {
          '0%': { transform: 'scale(1)', opacity: '0.6' },
          '80%, 100%': { transform: 'scale(2.2)', opacity: '0' },
        },
        'spin-slow': {
          to: { transform: 'rotate(360deg)' },
        },
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.7s ease-out both',
        float: 'float 6s ease-in-out infinite',
        marquee: 'marquee 32s linear infinite',
        blink: 'blink 1.1s step-end infinite',
        'scroll-dot': 'scroll-dot 1.8s ease-in-out infinite',
        'pulse-ring': 'pulse-ring 2.4s cubic-bezier(0.22, 1, 0.36, 1) infinite',
        'spin-slow': 'spin-slow 14s linear infinite',
      },
    },
  },
  plugins: [],
}
