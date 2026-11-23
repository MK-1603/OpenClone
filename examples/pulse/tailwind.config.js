/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        charcoal: {
          950: "#070707",
          900: "#0A0A0A", // primary background
          850: "#0F0F0F",
          800: "#111111", // secondary surface
          750: "#141414",
          700: "#181818", // elevated surface
          600: "#222222",
          500: "#2A2A2A",
        },
        gold: {
          300: "#EBD8AC",
          400: "#E0C58A",
          500: "#D6B36A", // restrained gold accent
          600: "#BA984E",
          700: "#9E7E36",
          900: "#3D2F11",
        },
        foreground: {
          primary: "#F5F5F5",
          secondary: "#A1A1AA",
          muted: "#71717A",
        },
        border: {
          subtle: "rgba(255, 255, 255, 0.07)",
          standard: "#27272A",
          gold: "rgba(214, 179, 106, 0.3)",
        },
      },
      fontFamily: {
        sans: [
          "-apple-system",
          "BlinkMacSystemFont",
          '"Segoe UI"',
          "Roboto",
          '"Helvetica Neue"',
          "Arial",
          "sans-serif",
        ],
      },
    },
  },
  plugins: [],
};
