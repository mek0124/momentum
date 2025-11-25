/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: "#0C2B4E",
        secondary: "#1A3D64",
        accent: "#1D546C",
        accentHover: "#F4F4F4",
        foreground: "#a9a9a9",
      },
    },
  },
  plugins: [],
}

