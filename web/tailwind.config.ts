import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: ["./ui/**/*.{tsx,ts,css}"],
  theme: {
    extend: {}
  },
  plugins: []
};

export default config;
