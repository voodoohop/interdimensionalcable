# ⚠️ DEPRECATED: html_apps/

**This directory is for local development only and is NOT deployed.**

## For Production

All production HTML files are in `public/`:
- `public/index.html`
- `public/embedding_flow.html`
- `public/landing.html`
- `public/debug.html`

## For Local Testing

To test locally:
```bash
# Option 1: Open directly
open html_apps/tv_embedding_flow.html

# Option 2: Use local server
python3 -m http.server 8000
# Then visit: http://localhost:8000/html_apps/tv_embedding_flow.html
```

**Note**: Local files use `../` paths, production files use `/` paths.

## Migration Status

- ✅ `embedding_flow.html` → `public/embedding_flow.html` (deployed)
- ⏳ Other TV apps not yet migrated to public/

## To Deploy Changes

1. Edit files in `public/` (not `html_apps/`)
2. Test locally
3. Deploy: `npx wrangler pages deploy public --project-name=interdimensional-cable`
