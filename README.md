# KBDLIM

Static map viewer for Escape From Tarkov document locations.

## GitHub Pages deployment

This repository is compatible with GitHub Pages as a static website.

### Important caveat

GitHub Pages cannot run `server.py` or the `/save-map` endpoint, so deployed Pages runs in read-only mode and **Save Map** is disabled.

### Enable Pages

1. Push your branch to GitHub.
2. Open **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select your branch (usually `main`) and folder **`/ (root)`**.
5. Save and wait for deployment.

### Verify

1. Open the published GitHub Pages URL.
2. Confirm map images and JSON hotspot data load correctly.
3. Confirm the save button is disabled in GitHub Pages (expected behavior).