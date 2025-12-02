Exercise Tracker (IndexedDB) - Full Frontend PWA-ready Project

Files:

- package.json (frontend only)
- vite.config.js
- index.html
- manifest.webmanifest
- /icons (placeholders)
- /src (Svelte app)
  - main.js
  - App.svelte
  - /components (Login, Dashboard, Admin, FiveChart)
  - /lib (idb.js, utils.js)

How to run locally:

1) Install dependencies
   npm install

2) Run dev server
   npm run dev

Open http://localhost:5173

Notes:
- All data is stored in browser IndexedDB. No backend needed.
- To create an admin: register a user, then open browser DevTools -> Application -> IndexedDB -> exercise-db -> users -> edit role to 'admin'.
- Replace /icons/icon-192.png and icon-512.png with real icons for PWA install icon.
