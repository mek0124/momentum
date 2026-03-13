/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0B0F14',
        surface: '#121821',
        surface_elevated: '#1A2230',
        surface_light: '#18202B',
        surface_glass: 'rgba(18, 24, 33, 0.85)',
        surface_glass_hover: 'rgba(26, 34, 48, 0.95)',
        primary: '#7F8FA6',
        primary_dim: '#6C7C94',
        primary_gradient_start: '#7F8FA6',
        primary_gradient_end: '#A5B4C8',
        secondary: '#1F2937',
        accent: '#A5B4C8',
        accent_hover: '#C0CEDF',
        text_primary: '#E6ECF3',
        text_secondary: '#B8C4D6',
        text_muted: '#8896AA',
        texton_accent: '#0B0F14',
        success: '#2ECC71',
        warning: '#F1C40F',
        error: '#E74C3C',
        border_radius_small: '6px',
        border_radius_medium: '10px',
        border_radius_large: '14px',
      },
    },
  },
  plugins: [],
}