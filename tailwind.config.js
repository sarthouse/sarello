/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './staticfiles/js/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        accounting: {
          debe: 'var(--accounting-debe)',
          haber: 'var(--accounting-haber)',
          saldo: 'var(--accounting-saldo)',
          activo: 'var(--accounting-activo)',
          pasivo: 'var(--accounting-pasivo)',
          patrimonio: 'var(--accounting-patrimonio)',
          ingreso: 'var(--accounting-ingreso)',
          egreso: 'var(--accounting-egreso)',
        },
      },
      fontFamily: {
        sans: ['IBM Plex Sans', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
        mono: ['IBM Plex Mono', 'monospace'],
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        dark: {
          'primary': '#4f9eff',
          'primary-content': '#ffffff',
          'secondary': '#00d4aa',
          'secondary-content': '#ffffff',
          'accent': '#f5a623',
          'neutral': '#252b42',
          'neutral-content': '#e8edf7',
          'base-100': '#0f1117',
          'base-200': '#161b27',
          'base-300': '#1e2535',
          'base-content': '#ffffff',
          'info': '#4f9eff',
          'success': '#4caf82',
          'warning': '#f5a623',
          'error': '#e05252',
          '--rounded-box': '0.5rem',
          '--rounded-btn': '0.375rem',
          '--rounded-badge': '0.375rem',
          '--tab-radius': '0.375rem',
        },
      },
      {
        light: {
          'primary': '#4f9eff',
          'primary-content': '#ffffff',
          'secondary': '#00d4aa',
          'secondary-content': '#ffffff',
          'accent': '#f5a623',
          'neutral': '#e5e7eb',
          'neutral-content': '#1f2937',
          'base-100': '#ffffff',
          'base-200': '#f5f5f5',
          'base-300': '#e5e5e5',
          'base-content': '#234472',
          'info': '#4f9eff',
          'success': '#4caf82',
          'warning': '#f5a623',
          'error': '#e05252',
          '--rounded-box': '0.5rem',
          '--rounded-btn': '0.375rem',
          '--rounded-badge': '0.375rem',
          '--tab-radius': '0.375rem',
        },
      },
    ],
    defaultTheme: 'dark',
  },
}
