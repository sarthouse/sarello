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
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
          800: '#075985',
          900: '#0c3d66',
        },
      },
      spacing: {
        'safe-top': 'var(--safe-area-inset-top)',
        'safe-bottom': 'var(--safe-area-inset-bottom)',
      },
    },
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: [
      {
        light: {
          'primary': '#1e40af',
          'primary-focus': '#1e3a8a',
          'primary-content': '#ffffff',
          'secondary': '#10b981',
          'secondary-focus': '#059669',
          'secondary-content': '#ffffff',
          'accent': '#f97316',
          'neutral': '#2b3544',
          'neutral-focus': '#16a34a',
          'neutral-content': '#f9fafb',
          'base-100': '#ffffff',
          'base-200': '#f3f4f6',
          'base-300': '#d1d5db',
          'base-content': '#1f2937',
          'info': '#0ea5e9',
          'success': '#10b981',
          'warning': '#f59e0b',
          'error': '#ef4444',
          '--rounded-box': '0.5rem',
          '--rounded-btn': '0.375rem',
          '--rounded-badge': '0.375rem',
          '--tab-radius': '0.375rem',
        },
      },
      'dark',
    ],
  },
}
