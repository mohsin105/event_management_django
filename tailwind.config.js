/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html", //templates at root level
	    "./**/templates/**/*.html" //templates at app level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
