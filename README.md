# rosaschimneyservices.com

Static website for **Rosas Chimney Services LLC**, a family-owned, CSIA Certified chimney sweep based in Front Royal, Virginia.

**Preview:** https://finnoybu.github.io/rosaschimneyservices-com/

## What's here

- Plain HTML, CSS and JavaScript. No framework, no build step needed to host it.
- Home, services, about and contact pages, a service-area hub, 9 county pages and 32 town pages.
- `README.txt` has plain-English hosting instructions for the site owners.

## Editing

Pages are generated from `_build/build.py` (layout, header, footer) and `_build/areas.py` (county and town content) so shared parts stay in sync:

```
cd _build
python3 build.py
```

Styles live in `assets/css/styles.css`; site behavior in `assets/js/main.js`.

## Credits

Handshake photo by MART PRODUCTION on Pexels (Pexels License).
