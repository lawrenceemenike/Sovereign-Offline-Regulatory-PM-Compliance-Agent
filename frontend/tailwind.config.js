/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bnh: {
          bg: '#FFFFFF',
          surface: '#F8FAFC',
          card: '#FFFFFF',
          border: '#E2E8F0',
          accent: '#1E40AF',
          gold: '#D97706',
          goldLight: '#B45309',
          emerald: '#059669',
          crimson: '#DC2626',
          textMuted: '#64748B',
          textBright: '#0F172A',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
};
