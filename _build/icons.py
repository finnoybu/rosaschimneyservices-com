def _i(body, fill=False):
    if fill:
        return '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' + body + '</svg>'
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + body + '</svg>'

I = {
 "phone": _i('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
 "sms": _i('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M8 10h.01M12 10h.01M16 10h.01"/>'),
 "mail": _i('<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>'),
 "clock": _i('<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>'),
 "shield": _i('<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>'),
 "award": _i('<circle cx="12" cy="8" r="6"/><path d="M15.5 13.2 17 22l-5-3-5 3 1.5-8.8"/>'),
 "home": _i('<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>'),
 "heart": _i('<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1.1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>'),
 "pin": _i('<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>'),
 "sweep": _i('<path d="M14 3 9.5 13"/><path d="M8 12.5 15 15l-1.5 6.5H4.5L6 14z"/><path d="M8 21.5l1.2-4M11 21.5l.8-4"/>'),
 "inspect": _i('<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/><path d="M8.5 11h5M11 8.5v5"/>'),
 "repair": _i('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>'),
 "liner": _i('<rect x="8" y="2" width="8" height="20" rx="1.5"/><path d="M8 6h8M8 10h8M8 14h8M8 18h8"/><path d="M4 22V8M20 22V8"/>'),
 "cap": _i('<path d="M3 9h18l-3-5H6z"/><path d="M7 9v4M17 9v4M12 9v4"/><path d="M6 13h12v9H6z"/>'),
 "stove": _i('<rect x="5" y="8" width="14" height="12" rx="2"/><path d="M10 8V3h4v5"/><path d="M12 17c-1.7 0-2.5-1.2-2.5-2.3 0-1.4 1.5-2 2.5-3.7 1 1.7 2.5 2.3 2.5 3.7 0 1.1-.8 2.3-2.5 2.3z"/><path d="M7 20v2M17 20v2"/>'),
 "flame": _i('<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.4-.5-2-1-3-1.1-2.1-.2-4 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.2.4-2.3 1-3.3.3 1.4 1.3 2.8 2.5 2.8z"/>'),
 "check": _i('<circle cx="12" cy="12" r="10"/><path d="m8 12 3 3 5-6"/>'),
 "star": _i('<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>', True),
 "arrow": _i('<path d="M5 12h14M13 6l6 6-6 6"/>'),
 "menu": _i('<path d="M4 6h16M4 12h16M4 18h16"/>'),
 "close": _i('<path d="M6 6l12 12M6 18 18 6"/>'),
 "leaf": _i('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6 2.4-.5 4.9-2 5.9-3"/>'),
 "facebook": _i('<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v2H7v4h3v8h4v-8h3l1-4h-4V8a0 0 0 0 1 0 0z"/>'),
 "instagram": _i('<rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/>'),
 "review": _i('<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="m12 6.5 1.2 2.4 2.6.4-1.9 1.8.5 2.6-2.4-1.3-2.4 1.3.5-2.6-1.9-1.8 2.6-.4z"/>'),
 "users": _i('<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>'),
 "calendar": _i('<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>'),
 "broom": _i('<path d="M14 3 9.5 13"/><path d="M8 12.5 15 15l-1.5 6.5H4.5L6 14z"/>'),
}
