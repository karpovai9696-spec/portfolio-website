/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,ts}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Терракотовый акцент — единственный цветовой акцент системы
        primary: {
          DEFAULT: '#B4491A',
          hover: '#97380F',
          soft: '#B4491A',
        },
        // Приглушённая охра — вторичный акцент (только для мелких меток)
        accent: '#8C6D1F',
        // Тёплая бумага и чернила (editorial-палитра)
        paper: {
          DEFAULT: '#F5F1E8',
          soft: '#EFEBDF',
          raised: '#FFFCF5',
        },
        ink: {
          50: '#6E6656',
          100: '#6E6656',
          400: '#8F8677',
          500: '#6E6656',
          700: '#4A443B',
          800: '#241E15',
          900: '#1B1610',
          950: '#14100C',
        },
        hairline: '#E2DCCB',
      },
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
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
