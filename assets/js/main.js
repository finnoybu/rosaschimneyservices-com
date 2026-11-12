/* Rosas Chimney Services: small, dependency-free site script */
(function () {
  "use strict";
  var PHONE = "+15404319629";
  var EMAIL = "rosaschimneyservices@gmail.com";
  var ES = document.documentElement.lang === "es";
  var T = function (en, es) { return ES ? es : en; };

  // Mobile menu
  var btn = document.querySelector(".menu-btn");
  var panel = document.getElementById("mobile-nav");
  if (btn && panel) {
    var setOpen = function (open) {
      panel.classList.toggle("open", open);
      btn.setAttribute("aria-expanded", open ? "true" : "false");
      btn.setAttribute("aria-label", open ? T("Close menu", "Cerrar menú") : T("Open menu", "Abrir menú"));
      btn.querySelector(".i-open").style.display = open ? "none" : "";
      btn.querySelector(".i-close").style.display = open ? "" : "none";
    };
    btn.addEventListener("click", function () { setOpen(!panel.classList.contains("open")); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1080) setOpen(false); });
  }

  // Device-aware call buttons (same approach as the Sturrock's site):
  // phones dial directly; desktops open a small panel with the number,
  // a copy button and a link to the online estimate form.
  var isPhone = function () {
    return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent) ||
      (window.matchMedia && window.matchMedia("(pointer: coarse)").matches);
  };
  var modal = null;
  var buildModal = function () {
    var contactLink = document.querySelector('.nav a[href$="contact.html"]');
    var contactHref = contactLink ? contactLink.getAttribute("href") : "contact.html";
    var d = document.createElement("dialog");
    d.className = "call-modal";
    d.setAttribute("aria-labelledby", "cm-title");
    d.innerHTML =
      '<div class="cm-top"><small id="cm-title">' + T("Call or text Rosas Chimney Services", "Llame o escriba a Rosas Chimney Services") + '</small>' +
      '<div class="cm-num">(540) 431-9629</div>' +
      '<button class="cm-close" type="button" aria-label="' + T("Close", "Cerrar") + '">&times;</button></div>' +
      '<div class="cm-body"><p class="cm-status" data-open-status>' + T("Mon to Sat, 7 AM to 7 PM", "Lun. a sáb., 7 AM a 7 PM") + '</p>' +
      '<p>' + T("Call or text this number from your phone for estimates and pricing, or send us a request online and we will get back to you.", "Llame o envíe un mensaje a este número desde su teléfono para presupuestos y precios, o envíenos una solicitud en línea y le responderemos.") + '</p>' +
      '<button class="btn btn-primary cm-copy" type="button">' + T("Copy Phone Number", "Copiar número") + '</button>' +
      '<a class="btn btn-ghost" href="' + contactHref + '">' + T("Request an Estimate Online", "Solicitar un presupuesto en línea") + '</a>' +
      '<div class="cm-copied" role="status" aria-live="polite"></div></div>';
    document.body.appendChild(d);
    var close = function () { d.close(); };
    d.querySelector(".cm-close").addEventListener("click", close);
    d.addEventListener("click", function (e) { if (e.target === d) close(); });
    d.querySelector(".cm-copy").addEventListener("click", function () {
      var out = d.querySelector(".cm-copied");
      var done = function () { out.textContent = T("Copied (540) 431-9629", "Copiado: (540) 431-9629"); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText("(540) 431-9629").then(done, function () { out.textContent = T("Our number is (540) 431-9629", "Nuestro número es (540) 431-9629"); });
      } else { out.textContent = T("Our number is (540) 431-9629", "Nuestro número es (540) 431-9629"); }
    });
    return d;
  };
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest('a[href^="tel:"]');
    if (!a || isPhone()) return;
    if (typeof HTMLDialogElement === "undefined") return; // very old browsers: leave the tel: link alone
    e.preventDefault();
    if (!modal) modal = buildModal();
    modal.querySelector(".cm-copied").textContent = "";
    var st = document.querySelector(".utility [data-open-status]");
    if (st) modal.querySelector(".cm-status").textContent = st.textContent;
    modal.showModal();
  });

  // Footer year
  var y = document.getElementById("year");
  if (y) y.textContent = new Date().getFullYear();

  // Open now / closed indicator (Mon to Sat, 7 AM to 7 PM, Eastern)
  var status = document.querySelectorAll("[data-open-status]");
  if (status.length) {
    var label = T("Mon to Sat, 7 AM to 7 PM", "Lun. a sáb., 7 AM a 7 PM"), shortLabel = T("Mon to Sat, 7 to 7", "Lun. a sáb., 7 a 7");
    try {
      var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", hour12: false }).formatToParts(new Date());
      var wd = "", hr = 0;
      parts.forEach(function (p) { if (p.type === "weekday") wd = p.value; if (p.type === "hour") hr = parseInt(p.value, 10) % 24; });
      var open = wd !== "Sun" && hr >= 7 && hr < 19;
      label = open ? T("Open now until 7 PM", "Abierto ahora hasta las 7 PM") : T("Closed now. Text us anytime", "Cerrado ahora. Escríbanos cuando quiera");
      // shorter wording for small phones so the top bar stays on one line
      shortLabel = open ? T("Open until 7 PM", "Abierto hasta las 7 PM") : T("Closed now", "Cerrado ahora");
    } catch (err) { /* keep default label */ }
    status.forEach(function (el) { el.textContent = label; el.setAttribute("data-short", shortLabel); });
  }

  // Scroll reveal
  var els = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && els.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else {
    els.forEach(function (el) { el.classList.add("in"); });
  }

  // Chimney self-check: worst checked item decides the result; situation items add notes.
  var check = document.getElementById("self-check");
  if (check) {
    var box = document.getElementById("check-result");
    var show = function (scroll) {
      var picked = Array.prototype.slice.call(check.querySelectorAll('input[name="sign"]:checked'));
      var kinds = picked.map(function (i) { return i.value; });
      var res = kinds.indexOf("urgent") > -1 ? "urgent" : kinds.indexOf("soon") > -1 ? "soon" : kinds.indexOf("plan") > -1 ? "plan" : "ok";
      Array.prototype.forEach.call(box.querySelectorAll("[data-result]"), function (el) { el.hidden = el.getAttribute("data-result") !== res; });
      var notes = picked.map(function (i) { return i.getAttribute("data-note"); }).filter(Boolean);
      Array.prototype.forEach.call(box.querySelectorAll("[data-note-for]"), function (el) { el.hidden = notes.indexOf(el.getAttribute("data-note-for")) < 0; });
      box.className = "check-result is-" + res;
      var summary = picked.map(function (i) { return i.parentNode.textContent.trim(); }).join("|");
      Array.prototype.forEach.call(box.querySelectorAll("[data-estimate]"), function (a) {
        var base = a.getAttribute("href").split("&notes=")[0];
        a.setAttribute("href", summary ? base + "&notes=" + encodeURIComponent(summary) : base);
      });
      if (scroll) {
        box.focus({ preventScroll: true });
        if (box.getBoundingClientRect().top < 0 || box.getBoundingClientRect().top > window.innerHeight * 0.6) box.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    };
    check.addEventListener("submit", function (e) { e.preventDefault(); show(true); });
    check.addEventListener("reset", function () {
      setTimeout(function () {
        Array.prototype.forEach.call(box.querySelectorAll("[data-result]"), function (el) { el.hidden = el.getAttribute("data-result") !== "idle"; });
        Array.prototype.forEach.call(box.querySelectorAll("[data-note-for]"), function (el) { el.hidden = true; });
        box.className = "check-result";
      }, 0);
    });
  }

  // Estimate request form. No server needed: it opens the visitor's
  // email app (or text messages) with the request filled in.
  var form = document.getElementById("estimate-form");
  if (form) {
    var msg = document.getElementById("form-msg");
    var qs = new URLSearchParams(window.location.search);
    var notesParam = qs.get("notes");
    if (notesParam && !form.querySelector("#message").value) form.querySelector("#message").value = T("From the chimney self-check:", "De la autoevaluación de chimenea:") + "\n- " + notesParam.split("|").join("\n- ");
    var townParam = qs.get("town");
    if (townParam) form.querySelector("#city").value = townParam;
    var preselect = qs.get("service");
    if (preselect && window.SERVICE_ALIAS && window.SERVICE_ALIAS[preselect]) preselect = window.SERVICE_ALIAS[preselect];
    if (preselect) {
      var sel = form.querySelector("#service");
      Array.prototype.forEach.call(sel.options, function (o) { if (o.value === preselect) sel.value = preselect; });
    }
    // ---- Field checks. Errors show under each field when the visitor
    // leaves it, and all of them are checked again on Send.
    var $ = function (id) { return document.getElementById(id); };
    var emailInput = $("email"), emailReq = $("email-req");
    var zipNote = $("zip-note");
    var ZIPS = window.SERVICE_ZIPS || {};
    var NAME_RX = /^[\p{L}\p{M}][\p{L}\p{M}'’. -]*$/u;
    var EMAIL_RX = /^[^\s@]+@[^\s@.]+(\.[^\s@.]+)*\.[A-Za-z]{2,}$/;
    var phoneDigits = function (s) {
      var d = s.replace(/\D/g, "");
      if (d.length === 11 && d.charAt(0) === "1") d = d.slice(1);
      return d;
    };
    // Virginia ZIP codes start with 201 or 220 to 246
    var isVaZip = function (z) { var p = +z.slice(0, 3); return p === 201 || (p >= 220 && p <= 246); };
    var picked = function () {
      return Array.prototype.filter.call(form.querySelectorAll('input[name="contact"]'), function (c) { return c.checked; })
        .map(function (c) { return c.value; });
    };
    var REQ = T("This field is required.", "Este campo es obligatorio.");
    var NAME_MSG = T("Please use letters only. Spaces, hyphens and apostrophes are fine.", "Use solo letras. Se permiten espacios, guiones y apóstrofos.");
    var checks = {
      fname: function (v) { return !v ? REQ : NAME_RX.test(v) ? "" : NAME_MSG; },
      lname: function (v) { return !v ? REQ : NAME_RX.test(v) ? "" : NAME_MSG; },
      email: function (v) {
        if (!v) return picked().indexOf("Email") > -1 ? T("Enter your email, since you asked us to contact you by email.", "Escriba su correo, ya que pidió que le contactemos por correo.") : "";
        return EMAIL_RX.test(v) ? "" : T("Please enter a valid email address, like name@example.com.", "Escriba un correo válido, como nombre@ejemplo.com.");
      },
      phone: function (v) {
        if (!v) return REQ;
        var d = phoneDigits(v);
        return /^[2-9]\d{2}[2-9]\d{6}$/.test(d) && d.slice(1, 3) !== "11" ? "" : T("Please enter a valid 10-digit phone number, like (540) 555-1234.", "Escriba un número de teléfono válido de 10 dígitos, como (540) 555-1234.");
      },
      address1: function (v) { return !v ? REQ : /[A-Za-z]/.test(v) && /\d/.test(v) ? "" : T("Please enter a street address with a house number, like 123 Main St.", "Escriba una dirección con número, como 123 Main St."); },
      city: function (v) { return !v ? REQ : NAME_RX.test(v) ? "" : T("Please check the city or town name.", "Revise el nombre de la ciudad o pueblo."); },
      zip: function (v) {
        if (!v) return REQ;
        if (!/^\d{5}(-\d{4})?$/.test(v)) return T("Enter a 5-digit ZIP code, like 22630.", "Escriba un código postal de 5 dígitos, como 22630.");
        return isVaZip(v) ? "" : T("This ZIP code is not in Virginia.", "Este código postal no es de Virginia.");
      },
      service: function (v) { return v ? "" : T("Please choose a service.", "Elija un servicio."); },
      contact: function () { return picked().length ? "" : T("Choose at least one way for us to contact you.", "Elija al menos una forma de contactarle."); }
    };
    var check = function (id, show) {
      var el = $(id), err = $(id + "-err");
      var val = el && el.value !== undefined ? el.value.trim() : "";
      var m = checks[id](val);
      if (el && el.setCustomValidity) el.setCustomValidity(m);
      if (show || !m) {
        if (err) err.textContent = m;
        if (el && el.classList) el.classList.toggle("bad", !!m);
      }
      return !m;
    };
    // Show the ZIP result: in our area, in Virginia but outside our usual
    // area, or outside Virginia (which blocks sending).
    // A ZIP we know fills in the city and locks it, so the two can't
    // disagree. Any other Virginia ZIP leaves the city open to type.
    var zipLookup = function () {
      var z = $("zip").value.trim().slice(0, 5), city = $("city");
      var town = /^\d{5}$/.test(z) ? ZIPS[z] : "";
      zipNote.hidden = true; zipNote.className = "zip-note";
      if (town) {
        city.value = town; city.readOnly = true; city.tabIndex = -1; check("city");
      } else if (city.readOnly) {
        city.value = ""; city.readOnly = false; city.removeAttribute("tabindex");
      }
      if (!/^\d{5}$/.test(z)) return;
      if (town) {
        zipNote.className = "zip-note ok";
        zipNote.textContent = T("Good news: " + town + ", VA " + z + " is in our service area.", "Buenas noticias: " + town + ", VA " + z + " está en nuestra área de servicio.");
      } else if (isVaZip(z)) {
        zipNote.className = "zip-note warn";
        zipNote.textContent = T("This ZIP code may be outside our usual service area. Please type your city or town, then send your request and we will let you know if we can help.", "Este código postal puede estar fuera de nuestra área habitual. Escriba su ciudad o pueblo y envíe su solicitud; le diremos si podemos ayudarle.");
      } else {
        zipNote.className = "zip-note out";
        zipNote.textContent = T("Sorry, this address is not in our service area. We serve the northern Shenandoah Valley and nearby counties in Virginia.", "Lo sentimos, esta dirección no está en nuestra área de servicio. Atendemos el norte del valle de Shenandoah y condados cercanos en Virginia.");
      }
      zipNote.hidden = false;
    };
    Object.keys(checks).forEach(function (id) {
      if (id === "contact") return;
      var el = $(id);
      el.addEventListener("blur", function () {
        if (id === "phone") { var d = phoneDigits(el.value); if (d.length === 10) el.value = "(" + d.slice(0, 3) + ") " + d.slice(3, 6) + "-" + d.slice(6); }
        if (el.value.trim() || el.classList.contains("bad")) check(id, true);
      });
      el.addEventListener(id === "service" ? "change" : "input", function () {
        if (id === "zip") zipLookup();
        check(id, el.classList.contains("bad"));
      });
    });
    var syncEmailRequired = function () {
      var needEmail = picked().indexOf("Email") > -1;
      emailInput.required = needEmail;
      if (emailReq) emailReq.hidden = !needEmail;
      check("contact", true);
      if (!needEmail || emailInput.classList.contains("bad")) check("email", emailInput.classList.contains("bad"));
    };
    Array.prototype.forEach.call(form.querySelectorAll('input[name="contact"]'), function (r) {
      r.addEventListener("change", syncEmailRequired);
    });
    syncEmailRequired();
    if ($("zip").value) zipLookup();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var first = null;
      Object.keys(checks).forEach(function (id) {
        if (!check(id, true) && !first) first = id === "contact" ? form.querySelector('input[name="contact"]') : $(id);
      });
      if (first) {
        first.focus();
        msg.className = "form-msg err show";
        msg.textContent = T("Please fix the highlighted fields, then send again.", "Corrija los campos marcados y vuelva a enviar.");
        return;
      }
      msg.className = "form-msg";
      var d = new FormData(form);
      var v = function (k) { return (d.get(k) || "").toString().trim(); };
      var lines = [
        "Name: " + v("fname") + " " + v("lname"),
        "Phone: " + v("phone"),
        v("email") ? "Email: " + v("email") : "",
        "Service address:",
        "  " + v("address1"),
        v("address2") ? "  " + v("address2") : "",
        "  " + v("city") + ", VA " + v("zip"),
        "Service: " + v("service"),
        "Preferred contact: " + picked().join(", "),
        "",
        v("message"),
        ES ? "" : null,
        ES ? "Preferred language: Spanish (sent from the Spanish site)" : null
      ].filter(function (l) { return l !== null; });
      var keep = [];
      lines.forEach(function (l, i) { if (l !== "" || (i > 0 && lines[i - 1] !== "" && i < lines.length - 1)) keep.push(l); });
      lines = keep;
      var body = lines.join("\n");
      var subject = "Estimate request: " + v("service") + " (" + v("city") + ", VA)";
      var href;
      if (e.submitter && e.submitter.value === "sms") {
        var sep = /iPhone|iPad|iPod/i.test(navigator.userAgent) ? "&" : "?";
        href = "sms:" + PHONE + sep + "body=" + encodeURIComponent(subject + "\n" + body);
      } else {
        href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
      }
      window.location.href = href;
      msg.className = "form-msg show";
      msg.textContent = T("Your message is ready to send in your email or messaging app. If nothing opened, call or text us at (540) 431-9629.", "Su mensaje está listo para enviar en su aplicación de correo o de mensajes. Si no se abrió nada, llámenos o escríbanos al (540) 431-9629.");
    });
  }
})();
