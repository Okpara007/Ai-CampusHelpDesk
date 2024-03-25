/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './node_modules/flowbite/**/*.js'
  ], /* Tells tailwind where to look for classes in the project */
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}

