/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,vue}"],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: "#f15264",
          dark: "#d93f50",
        },
        dark: "#1a1a1a",
        text: {
          DEFAULT: "#333333",
          light: "#666666",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        heading: ["Exo 2", "Inter", "sans-serif"],
      },
      spacing: {
        18: "4.5rem",
        22: "5.5rem",
      },
      borderRadius: {
        "3xl": "24px",
      },
      boxShadow: {
        card: "0 4px 12px rgba(0, 0, 0, 0.1)",
        "card-hover": "0 8px 24px rgba(0, 0, 0, 0.15)",
      },
      keyframes: {
        scroll: {
          "0%": { transform: "translateX(0)" },
          "100%": { transform: "translateX(-50%)" },
        },
        shimmer: {
          "0%": { backgroundPosition: "0 0" },
          "100%": { backgroundPosition: "20px 20px" },
        },
      },
      animation: {
        scroll: "scroll 30s linear infinite",
        shimmer: "shimmer 1.5s infinite linear",
      },
    },
  },
  plugins: [],
};
