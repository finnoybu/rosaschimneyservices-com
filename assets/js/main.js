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
    var label = T("Mon to Sat, 7 AM to 7 PM", "Lun. a sáb., 7 AM a 7 PM");
    try {
      var parts = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", weekday: "short", hour: "numeric", hour12: false }).formatToParts(new Date());
      var wd = "", hr = 0;
      parts.forEach(function (p) { if (p.type === "weekday") wd = p.value; if (p.type === "hour") hr = parseInt(p.value, 10) % 24; });
      var open = wd !== "Sun" && hr >= 7 && hr < 19;
      label = open ? T("Open now until 7 PM", "Abierto ahora hasta las 7 PM") : T("Emergency calls accepted 24/7", "Atendemos emergencias 24/7");
      // after hours the top bar switches to the emergency line (phone icon, alert color)
      Array.prototype.forEach.call(document.querySelectorAll(".u-status"), function (el) { el.classList.toggle("is-emergency", !open); });
    } catch (err) { /* keep default label */ }
    var shortLabel = open ? label : T("Emergencies 24/7", "Emergencias 24/7");
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
    // Email becomes required when the customer asks to be contacted by email
    var emailInput = form.querySelector("#email");
    var emailReq = document.getElementById("email-req");
    var syncEmailRequired = function () {
      var picked = form.querySelector('input[name="contact"]:checked');
      var needEmail = !!picked && picked.value === "Email";
      emailInput.required = needEmail;
      if (emailReq) emailReq.hidden = !needEmail;
      if (!needEmail) emailInput.setCustomValidity("");
    };
    Array.prototype.forEach.call(form.querySelectorAll('input[name="contact"]'), function (r) {
      r.addEventListener("change", syncEmailRequired);
    });
    syncEmailRequired();

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var d = new FormData(form);
      var v = function (k) { return (d.get(k) || "").toString().trim(); };
      var lines = [
        "Name: " + v("name"),
        "Phone: " + v("phone"),
        v("email") ? "Email: " + v("email") : "",
        "Service address:",
        "  " + v("address1"),
        v("address2") ? "  " + v("address2") : "",
        "  " + v("city") + ", " + v("state").toUpperCase() + " " + v("zip"),
        "Service: " + v("service"),
        "Best way to reach me: " + v("contact"),
        "",
        v("message"),
        ES ? "" : null,
        ES ? "Preferred language: Spanish (sent from the Spanish site)" : null
      ].filter(function (l) { return l !== null; });
      var keep = [];
      lines.forEach(function (l, i) { if (l !== "" || (i > 0 && lines[i - 1] !== "" && i < lines.length - 1)) keep.push(l); });
      lines = keep;
      var body = lines.join("\n");
      var subject = "Estimate request: " + v("service") + " (" + v("city") + ", " + v("state").toUpperCase() + ")";
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
