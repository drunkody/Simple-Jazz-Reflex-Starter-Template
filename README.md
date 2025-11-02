# 🎺 Jazz Notes - Frontend-Only App

**No backend state required!** All interactivity runs in the browser.

## Architecture

- ✅ **Stateless Reflex** - Static HTML generator only
- ✅ **Frontend JavaScript** - All logic in `assets/app.js`
- ✅ **localStorage** - Data persistence (ready for Jazz CRDTs)
- ✅ **No WebSocket** - No backend server needed in production

## Quick Start

```bash
# Development
reflex run

# Production (static export)
reflex export
```

## Deployment

This app exports to 100% static files. Deploy anywhere:
- GitHub Pages
- Netlify
- Vercel
- Any static host

```bash
reflex export
# Upload .web/_static/ to your host
```
