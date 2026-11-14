# Moss & Maple

A quiet coloring book of the seasons, for iPad and phones.

## What's in this folder

- `index.html`: the whole app, including all 12 pages
- `manifest.webmanifest`, `icon-*.png`, `apple-touch-icon.png`: these give the app its name and icon when you add it to the Home Screen
- `sw.js`: lets the app work offline once it's hosted
- `source/`: the scripts that draw the pages and build the app (only needed when making changes)

## Put it online with GitHub Pages (free)

1. On github.com, create a new repository, for example `moss-and-maple`. It can be public or private, but free accounts need it to be public for Pages.
2. Upload these files to it: `index.html`, `manifest.webmanifest`, `sw.js` and the three `.png` icons. Use **Add file → Upload files**.
3. Open the repository's **Settings → Pages**. Under "Build and deployment", choose **Deploy from a branch**, then the **main** branch and the **/ (root)** folder, and click **Save**.
4. After a minute or two, the app is live at `https://YOUR-USERNAME.github.io/moss-and-maple/`.
5. On the iPad, open that address in **Safari**, tap **Share**, then **Add to Home Screen**. It now opens full screen like a real app and works offline.

Your coloring progress is saved on each device itself, in the browser's storage.

## How to use it

- **Pencil, Brush, Water, Fill, Eraser**: pick a tool, then set its size and opacity with the sliders.
- **Stay inside the lines** is the button at the top right next to the ⋯ menu. When it's on, each stroke stays inside the shape where it started.
- **Apple Pencil**: pressing harder makes a thicker line. Once the app has seen the Pencil, fingers only move and zoom the page. You can change this in the ⋯ menu.
- **Gestures**: pinch to zoom, drag with two fingers to move the page, and tap with two fingers to undo.
- **Colors**: each season has its own palette (the four small icons). The **+** circle lets you mix your own color.
- **Save as picture** is in the ⋯ menu.
