# rosaschimneyservices.com

> **Site designer's working copy and demo.** This GitHub repository and the preview at
> https://finnoybu.github.io/rosaschimneyservices-com/ exist only so the site designer
> (Ken Tannenbaum) can build and show the site. They are not the live website and are
> for the site designer's use only. The live site is hosted by Rosas Chimney Services
> at https://rosaschimneyservices.com.

Static website for **Rosas Chimney Services LLC**, a family-owned, CSIA Certified chimney sweep based in Front Royal, Virginia.

**Demo preview (site designer only):** https://finnoybu.github.io/rosaschimneyservices-com/

## What's here

- Plain HTML, CSS and JavaScript. No framework, no build step needed to host it.
- Home, services, about and contact pages, a service-area hub, 9 county pages and 32 town pages.
- `README.txt` is the owners' guide that ships with the site.
- `_build/`, `brand/` and `_build/publish-to-github.bat` are site designer tools and are not part of the site handed to the owners.

## Editing

Pages are generated from `_build/build.py` (layout, header, footer) and `_build/areas.py` (county and town content) so shared parts stay in sync:

```
cd _build
python3 build.py
```

Styles live in `assets/css/styles.css`; site behavior in `assets/js/main.js`.

## Credits

Handshake photo by MART PRODUCTION on Pexels (Pexels License).
