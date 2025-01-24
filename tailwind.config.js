/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    './*/templates/*/**/*.html',  // All app templates
    './*/static/*/**/*.css',     // All app CSS files
    './*/static/*/**/*.js',      // All app JS files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

