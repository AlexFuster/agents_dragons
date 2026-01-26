/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'fantasy-dark': '#1a1a2e',
        'fantasy-medium': '#16213e',
        'fantasy-accent': '#0f3460',
        'fantasy-highlight': '#533483',
        'fantasy-gold': '#e94560',
      }
    },
  },
  plugins: [],
}
