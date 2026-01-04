/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        primary: '#2d1a3d',
        secondary: '#4a2d5d',
        accent: '#6b4a81',
        accentHover: '#8d6ba5',
        foreground: '#f0e8fa',
      },
    },
  },
  plugins: [],
}

