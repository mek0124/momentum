/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'deep-purple': '#210F37',
        'mid-purple': '#4F1C51',
        'red-clay': '#A55B4B',
        gold: '#DCA06D',
        'deep-blue': '#0C2B4E',
        'mid-blue': '#1A3D64',
        teal: '#1D546C',
        white: '#F4F4F4',
        // Additional utility colors based on your CSS variables
        'glass-panel': 'rgba(12, 43, 78, 0.9)',
        'glass-border': 'rgba(220, 160, 109, 0.15)',
        'text-primary': '#F4F4F4',
        'text-muted': 'rgba(244, 244, 244, 0.5)',
        accent: '#DCA06D',
        'accent-dim': 'rgba(220, 160, 109, 0.2)',
        interactive: '#1D546C',
        danger: '#A55B4B',
        'bg-void': '#210F37',
      },
      // Custom gradients
      backgroundImage: {
        'grad-void': 'radial-gradient(circle at 80% -20%, #4F1C51, #0C2B4E 90%)',
        'grad-lock': 'linear-gradient(to bottom, #210F37, #0C2B4E)',
      },
      // Font families
      fontFamily: {
        'brand': ['Cinzel', 'serif'],
        'ui': ['Inter', 'sans-serif'],
        'body': ['Playfair Display', 'serif'],
        'mono': ['JetBrains Mono', 'monospace'],
      },
      // Custom animation curve
      transitionTimingFunction: {
        'ease-special': 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },
  plugins: [],
}

