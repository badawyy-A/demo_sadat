// tailwind.config.js
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        primary: {
          light: "#4ade80", // Light green - energetic
          DEFAULT: "#22c55e", // Sporty green - main
          dark: "#16a34a", // Deep green - for hover
        },
        secondary: {
          light: "#fb923c", // Light orange - energy
          DEFAULT: "#f97316", // Vibrant orange - motivation
          dark: "#ea580c", // Deep orange - for hover
        },
        accent: {
          light: "#38bdf8", // Light blue - active
          DEFAULT: "#0ea5e9", // Sporty blue - hydration
          dark: "#0284c7", // Deep blue - for hover
        },
        background: {
          light: "#f8fafc", // Very light gray - clean
          dark: "#0f172a", // Deep navy - night mode
        },
        card: {
          light: "#ffffff", // White
          dark: "#1e293b", // Dark slate
        },
        text: {
          light: "#334155", // Slate
          dark: "#f1f5f9", // Light gray
        },
      },
    },
  },
  plugins: [],
  safelist: [
    "bg-primary-light",
    "bg-primary",
    "bg-primary-dark",
    "bg-secondary-light",
    "bg-secondary",
    "bg-secondary-dark",
    "bg-accent-light",
    "bg-accent",
    "bg-accent-dark",
  ],
};
