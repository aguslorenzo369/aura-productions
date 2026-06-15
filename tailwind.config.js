/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        gold: {
          DEFAULT: '#C9A84C',
          light: '#E8C97A',
          dark: '#A07830',
        },
        aura: {
          black: '#000000',
          deep: '#08080F',
          card: '#0D0D14',
        }
      },
      fontFamily: {
        sans: ['var(--font-space-grotesk)', 'sans-serif'],
        serif: ['var(--font-playfair)', 'serif'],
      },
      letterSpacing: {
        widest: '0.25em',
        ultra: '0.35em',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-gold': 'pulseGold 2s ease-in-out infinite',
        'rotate-slow': 'rotate 50s linear infinite',
        'rotate-medium': 'rotate 35s linear reverse infinite',
        'rotate-fast': 'rotate 22s linear infinite',
        'ticker': 'ticker 30s linear infinite',
        'breathe': 'breathe 4s ease-in-out infinite',
        'scroll-line': 'scrollLine 2s ease-in-out infinite',
        'fade-up': 'fadeUp 0.8s ease forwards',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-14px)' },
        },
        pulseGold: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.3' },
        },
        rotate: {
          from: { transform: 'translate(-50%, -50%) rotate(0deg)' },
          to: { transform: 'translate(-50%, -50%) rotate(360deg)' },
        },
        ticker: {
          from: { transform: 'translateX(0)' },
          to: { transform: 'translateX(-50%)' },
        },
        breathe: {
          '0%, 100%': { transform: 'scale(1)', opacity: '0.5' },
          '50%': { transform: 'scale(1.4)', opacity: '1' },
        },
        scrollLine: {
          '0%': { opacity: '0', transform: 'scaleY(0)', transformOrigin: 'top' },
          '60%': { opacity: '1' },
          '100%': { opacity: '0', transform: 'scaleY(1)', transformOrigin: 'top' },
        },
        fadeUp: {
          from: { opacity: '0', transform: 'translateY(30px)' },
          to: { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
