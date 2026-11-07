# Vacation-rental host page and chimney self-check. Spanish text sits beside the English
# via t(en, es); build.py merges EXTRA_ES into the translator before making /es/.
import html as _h
EXTRA_ES = {}
def t(en, es):
    EXTRA_ES[en] = es
    return _h.escape(en, quote=False)

def faq_block(faqs):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)

def faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _h.unescape(q), "acceptedAnswer": {"@type": "Answer", "text": _h.unescape(a)}} for q, a in faqs]}

def rentals(B):
    I, PHONE, PHONE_DISPLAY, BOOK, TOWN_BY = B["I"], B["PHONE"], B["PHONE_DISPLAY"], B["BOOK"], B["TOWN_BY"]
    towns = "".join(f'<li><a href="service-areas/{TOWN_BY[s]["county"]}/{s}.html">{I["pin"]}{TOWN_BY[s]["name"]}</a></li>'
                    for s in ["luray", "stanley", "shenandoah", "front-royal", "bentonville", "linden", "sperryville", "washington"])
    def li(b, s): return f'<li>{I["check"]}<span><b>{b}</b> {s}</span></li>'
    tips = [
     t("Open the damper before lighting a fire, and leave it open until the fire is completely out.", "Abra el regulador de tiro antes de encender el fuego y déjelo abierto hasta que el fuego esté completamente apagado."),
     t("Burn only the dry firewood we provide. No trash, cardboard, wrapping paper or painted wood.", "Queme solo la leña seca que le proporcionamos. Nada de basura, cartón, papel de regalo ni madera pintada."),
     t("Keep fires small to medium, and never use lighter fluid or gasoline.", "Mantenga fuegos pequeños o medianos, y nunca use líquido para encendedor ni gasolina."),
     t("Keep the screen or glass doors closed, and keep rugs, blankets and furniture at least 3 feet away.", "Mantenga cerrada la pantalla o las puertas de vidrio, y mantenga alfombras, mantas y muebles a por lo menos 3 pies (1 metro) de distancia."),
     t("Never leave a fire unattended or go to bed while it is still burning.", "Nunca deje el fuego sin vigilancia ni se vaya a dormir mientras siga encendido."),
     t("Put ashes only in the lidded metal container provided, and set it outside, away from the house.", "Ponga las cenizas solo en el recipiente metálico con tapa que le proporcionamos, y déjelo afuera, lejos de la casa."),
     t("If smoke comes into the room or you smell something unusual, let the fire burn down and contact us.", "Si entra humo a la habitación o nota un olor extraño, deje que el fuego se apague y comuníquese con nosotros."),
    ]
    faqs = [
     (t("Do I need to be at the property?", "¿Tengo que estar en la propiedad?"),
      t("No. Many hosts send us the access details, and we text photos and a summary when we are done.", "No. Muchos anfitriones nos envían los datos de acceso, y le mandamos fotos y un resumen por mensaje cuando terminamos.")),
     (t("How often should a rental chimney be swept?", "¿Con qué frecuencia se debe deshollinar la chimenea de un alquiler?"),
      t("At least once a year, before the burning season. Rentals with heavy winter bookings often need a second sweep partway through the season, and we can check the buildup and tell you.", "Al menos una vez al año, antes de la temporada de uso. Los alquileres con muchas reservas en invierno suelen necesitar un segundo deshollinado a mitad de temporada, y podemos revisar la acumulación y decírselo.")),
     (t("Can you work around my bookings?", "¿Pueden trabajar según mis reservas?"),
      t("Yes. Tell us your checkout and check-in times and we will schedule the visit between guests, Monday through Saturday.", "Sí. Díganos sus horarios de salida y llegada y programaremos la visita entre huéspedes, de lunes a sábado.")),
     (t("Do you provide a record of the work?", "¿Me dan un registro del trabajo?"),
      t("Yes. You get dated photos and a plain-language summary of what we cleaned, inspected and found, to keep with your property records.", "Sí. Recibe fotos con fecha y un resumen claro de lo que limpiamos, inspeccionamos y encontramos, para guardar con los documentos de su propiedad.")),
    ]
    body = B["page_hero"](t("Vacation Rentals", "Alquileres vacacionales"), t("For Rental Hosts", "Para anfitriones"),
        t("Chimney care for cabins and vacation rentals", "Cuidado de chimeneas para cabañas y alquileres vacacionales"),
        t("Guests love a fire. You need it to be safe. We keep fireplaces and stoves in Shenandoah Valley and Blue Ridge rentals clean, inspected and documented, on a schedule that works around your bookings.",
          "A los huéspedes les encanta encender el fuego. Usted necesita que sea seguro. Mantenemos limpios, inspeccionados y documentados los hogares y estufas de los alquileres del valle de Shenandoah y el Blue Ridge, con un horario que se adapta a sus reservas."))
    body += f"""<section class="section"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">{t("Why Rentals Are Different", "Por qué los alquileres son diferentes")}</span>
    <h2>{t("A rental fireplace works harder than a home fireplace", "El hogar de un alquiler trabaja más que el de una casa")}</h2>
    <p>{t("Every week brings new guests who do not know your fireplace or stove. That changes how fast it wears and what can go wrong between visits.", "Cada semana llegan huéspedes nuevos que no conocen su hogar o su estufa. Eso cambia qué tan rápido se desgasta y lo que puede salir mal entre visitas.")}</p>
    <ul class="check-list">
      {li(t("Guests burn differently.", "Los huéspedes queman distinto."), t("Bigger fires, damp wood and doors left open build creosote faster than everyday use.", "Fuegos más grandes, leña húmeda y puertas abiertas acumulan creosota más rápido que el uso diario."))}
      {li(t("Empty weeks invite trouble.", "Las semanas vacías traen problemas."), t("Birds, squirrels and rain find their way into uncapped flues while the cabin sits empty.", "Pájaros, ardillas y lluvia entran por los conductos sin sombrerete mientras la cabaña está vacía."))}
      {li(t("Nobody is there to notice.", "No hay nadie para notarlo."), t("A smoky room or a strange smell may go unreported until it shows up in a review.", "Una habitación con humo o un olor extraño pueden pasar sin aviso hasta que aparecen en una reseña."))}
      {li(t("Records matter.", "Los registros importan."), t("A dated inspection shows you are keeping up with the fireplace, which insurers and property managers may ask about.", "Una inspección con fecha demuestra que usted mantiene el hogar al día, algo que las aseguradoras y los administradores de propiedades pueden pedir."))}
    </ul>
  </div>
  <div class="art-card photo reveal">{B["work_fig"](*B["WORK"][1])}</div>
</div></section>

<section class="section bg-cream"><div class="wrap">
  <div class="section-head center reveal"><span class="eyebrow">{t("What Hosts Get", "Lo que reciben los anfitriones")}</span><h2>{t("Built around your calendar", "Pensado según su calendario")}</h2></div>
  <div class="values">
    <div class="value reveal">{I['calendar']}<h3>{t("Scheduled between guests", "Programado entre huéspedes")}</h3><p>{t("Tell us your turnover times and we will work in the gap, Monday through Saturday.", "Díganos sus horarios de cambio de huéspedes y trabajaremos en ese intervalo, de lunes a sábado.")}</p></div>
    <div class="value reveal">{I['inspect']}<h3>{t("Photos for your records", "Fotos para sus registros")}</h3><p>{t("Dated photos and a plain-language summary of what we cleaned, inspected and found.", "Fotos con fecha y un resumen claro de lo que limpiamos, inspeccionamos y encontramos.")}</p></div>
    <div class="value reveal">{I['home']}<h3>{t("No need to be there", "No tiene que estar presente")}</h3><p>{t("Send the access details and we will text you when the job is done.", "Envíenos los datos de acceso y le avisaremos por mensaje cuando terminemos.")}</p></div>
    <div class="value reveal">{I['cap']}<h3>{t("Caps that keep critters out", "Sombreretes que impiden la entrada de animales")}</h3><p>{t("A sturdy cap and screen stop animals, nests and rain while the property sits empty.", "Un sombrerete resistente con malla detiene animales, nidos y lluvia mientras la propiedad está vacía.")}</p></div>
    <div class="value reveal">{I['users']}<h3>{t("More than one property?", "¿Tiene más de una propiedad?")}</h3><p>{t("We can group visits so every cabin is ready before the season starts.", "Podemos agrupar las visitas para que todas sus cabañas estén listas antes de que empiece la temporada.")}</p></div>
    <div class="value reveal">{I['flame']}<h3>{t("Stoves and inserts too", "También estufas e insertos")}</h3><p>{t("Wood stoves, pellet stoves and inserts get the same careful cleaning and inspection.", "Las estufas de leña, de pellets y los insertos reciben la misma limpieza e inspección cuidadosa.")}</p></div>
  </div>
</div></section>

<section class="section bg-soot"><div class="wrap">
  <div class="section-head reveal"><span class="eyebrow">{t("A Simple Plan", "Un plan sencillo")}</span><h2>{t("Getting a rental ready for the season", "Cómo preparar un alquiler para la temporada")}</h2></div>
  <div class="steps">
    <div class="step reveal"><h3>{t("Inspect and sweep", "Inspección y deshollinado")}</h3><p>{t("Book before your fall and winter reservations fill up.", "Reserve antes de que se llenen sus reservas de otoño e invierno.")}</p></div>
    <div class="step reveal"><h3>{t("Fix and protect", "Reparar y proteger")}</h3><p>{t("Take care of caps, crowns and leaks before the cold sets in.", "Atienda sombreretes, coronas y filtraciones antes de que llegue el frío.")}</p></div>
    <div class="step reveal"><h3>{t("Check mid-season", "Revisión a mitad de temporada")}</h3><p>{t("Busy cabins may need a second sweep. We will tell you if yours does.", "Las cabañas con mucho uso pueden necesitar un segundo deshollinado. Le diremos si la suya lo necesita.")}</p></div>
    <div class="step reveal"><h3>{t("Brief your guests", "Informe a sus huéspedes")}</h3><p>{t("Add the fireplace tips below to your house manual.", "Agregue los consejos de abajo a su manual de la casa.")}</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap split">
  <div class="reveal">
    <span class="eyebrow">{t("For Your House Manual", "Para su manual de la casa")}</span>
    <h2>{t("Fireplace tips for your guests", "Consejos del hogar para sus huéspedes")}</h2>
    <p>{t("Feel free to copy these into your welcome book or listing. Clear rules up front prevent most of the problems we see in rentals.", "Puede copiarlos en su libro de bienvenida o en su anuncio. Unas reglas claras desde el principio evitan la mayoría de los problemas que vemos en los alquileres.")}</p>
    <p class="note-sm">{t("Hosts: test the smoke and carbon monoxide alarms at every turnover.", "Anfitriones: prueben las alarmas de humo y de monóxido de carbono en cada cambio de huéspedes.")}</p>
  </div>
  <div class="tips-box reveal"><h3>{t("Using the fireplace", "Uso del hogar")}</h3><ol>{"".join(f"<li>{x}</li>" for x in tips)}</ol></div>
</div></section>

<section class="section bg-cream"><div class="wrap area-wrap">
  <div class="reveal">
    <span class="eyebrow">{t("Rental Country", "Zona de alquileres")}</span>
    <h2 style="font-size:clamp(30px,4vw,42px);margin-bottom:16px">{t("Cabins and rentals we serve", "Cabañas y alquileres que atendemos")}</h2>
    <p class="lead">{t("From riverfront cabins on the South Fork to mountain homes near Shenandoah National Park, we serve rentals across all nine counties in our area.", "Desde cabañas junto al South Fork hasta casas de montaña cerca del Parque Nacional Shenandoah, atendemos alquileres en los nueve condados de nuestra área.")}</p>
    <ul class="towns">{towns}</ul>
  </div>
  <div class="reveal"><div class="faq faq-tight">{faq_block(faqs)}</div></div>
</div></section>
""" + B["cta_band"](t("Get your rental ready for the season", "Prepare su alquiler para la temporada"),
                    t("Call or text with your property address and your next open dates.", "Llame o envíe un mensaje con la dirección de su propiedad y sus próximas fechas libres."))
    extra = '<script type="application/ld+json">' + B["json"].dumps(faq_ld(faqs)) + '</script>\n'
    return B["head"](t("Chimney Service for Vacation Rentals and Cabins | Rosas Chimney Services", "Servicio de chimeneas para alquileres vacacionales y cabañas | Rosas Chimney Services"),
                     t("Chimney sweeping and inspections for cabins and vacation rentals in the Shenandoah Valley, scheduled between guests, with dated photos for your records. Call or text (540) 431-9629.",
                       "Deshollinado e inspecciones para cabañas y alquileres vacacionales en el valle de Shenandoah, programados entre huéspedes, con fotos fechadas para sus registros. Llame o envíe un texto al (540) 431-9629."),
                     "vacation-rentals.html", extra) + B["header"]("vacation-rentals.html") + body + B["footer"]()

def self_check(B):
    I, PHONE, PHONE_DISPLAY, BOOK = B["I"], B["PHONE"], B["PHONE_DISPLAY"], B["BOOK"]
    def box(kind, en, es, note=""):
        n = f' data-note="{note}"' if note else ""
        return f'<label class="chk"><input type="checkbox" name="sign" value="{kind}"{n}><span>{t(en, es)}</span></label>'
    groups = [
     (t("Warning signs", "Señales de alerta"), [
       box("urgent", "Smoke comes into the room when the fireplace or stove is in use", "Entra humo a la habitación cuando usa el hogar o la estufa"),
       box("urgent", "A carbon monoxide alarm has gone off in the home", "Ha sonado una alarma de monóxido de carbono en la casa"),
       box("urgent", "There may have been a chimney fire: a loud roar, sparks or flames from the top, or puffy, flaky creosote afterward", "Puede haber ocurrido un incendio de chimenea: un rugido fuerte, chispas o llamas por arriba, o creosota hinchada y escamosa después"),
       box("urgent", "I can see cracks, gaps or missing pieces in the firebox or flue liner", "Veo grietas, aberturas o piezas faltantes en la cámara de combustión o en el revestimiento del conducto"),
     ]),
     (t("Things you may have noticed", "Cosas que quizás ha notado"), [
       box("soon", "It has been more than a year since the last inspection, or I do not know when it was", "Ha pasado más de un año desde la última inspección, o no sé cuándo fue"),
       box("soon", "There is black, flaky buildup or a shiny glaze inside the firebox or near the damper", "Hay residuos negros y escamosos o una capa brillante dentro de la cámara de combustión o cerca del regulador de tiro"),
       box("soon", "A strong smoky or musty smell comes from the fireplace, especially in warm or wet weather", "Sale un olor fuerte a humo o a humedad del hogar, sobre todo con calor o lluvia"),
       box("soon", "Fires are hard to start or keep going, or smoke rolls out when the door is opened", "Cuesta encender o mantener el fuego, o sale humo al abrir la puerta"),
       box("soon", "I hear animals or see nesting material, or there is no cap on top", "Escucho animales o veo restos de nidos, o no hay sombrerete arriba"),
       box("soon", "There are water stains, rust or white staining on or near the chimney, or water in the firebox", "Hay manchas de agua, óxido o manchas blancas en la chimenea o cerca de ella, o agua en la cámara de combustión"),
       box("soon", "The crown, bricks or mortar on the outside look cracked, crumbling or loose", "La corona, los ladrillos o el mortero por fuera se ven agrietados, desmoronados o sueltos"),
       box("soon", "The damper is stuck, rusted or hard to open and close", "El regulador de tiro está atascado, oxidado o cuesta abrirlo y cerrarlo"),
     ]),
     (t("Your situation", "Su situación"), [
       box("plan", "I am buying or selling this home", "Estoy comprando o vendiendo esta casa", "sale"),
       box("plan", "I am adding or replacing a stove, insert or fuel type", "Voy a agregar o cambiar una estufa, un inserto o el tipo de combustible", "change"),
       box("plan", "We burn wood several times a week through the winter", "Quemamos leña varias veces por semana durante el invierno", "heavy"),
       box("plan", "The home is a vacation rental or sits empty for weeks at a time", "La casa es un alquiler vacacional o pasa semanas vacía", "rental"),
     ]),
    ]
    fs = "".join(f'<fieldset class="chk-group"><legend>{lg}</legend>{"".join(bx)}</fieldset>' for lg, bx in groups)
    est = f'<a class="btn btn-ghost" data-estimate href="contact.html?service=Chimney%20inspection">{t("Request an inspection", "Solicitar una inspección")}</a>'
    book = f'<a class="btn btn-primary" href="{BOOK}" target="_blank" rel="noopener">{I["calendar"]}{t("Book Online", "Reserve en línea")}</a>'
    call = f'<a class="btn btn-primary" href="tel:{PHONE}">{I["phone"]}{t("Call", "Llamar")} {PHONE_DISPLAY}</a>'
    body = B["page_hero"](t("Chimney Self-Check", "Autoevaluación de chimenea"), t("One-Minute Self-Check", "Autoevaluación de un minuto"),
        t("Is your chimney due for service?", "¿Su chimenea necesita servicio?"),
        t("Check anything that applies to your fireplace, stove or chimney. You will see right away whether to call now, schedule a visit or simply keep up your yearly inspection.",
          "Marque todo lo que se aplique a su hogar, estufa o chimenea. Verá de inmediato si debe llamar ahora, programar una visita o simplemente mantener su inspección anual."))
    body += f"""<section class="section"><div class="wrap check-layout">
  <div>
    <p class="alert">{I['flame']}<span><b>{t("Fire in the chimney right now?", "¿Hay fuego en la chimenea ahora mismo?")}</b> {t("Get everyone out of the house and call 911.", "Saque a todos de la casa y llame al 911.")}</span></p>
    <form id="self-check" class="check-card" novalidate>
      {fs}
      <div class="chk-actions"><button class="btn btn-primary" type="submit">{t("See my result", "Ver mi resultado")} {I['arrow']}</button><button class="btn btn-ghost" type="reset">{t("Start over", "Empezar de nuevo")}</button></div>
    </form>
  </div>
  <aside>
    <div id="check-result" class="check-result" tabindex="-1" aria-live="polite">
      <div class="res res-idle" data-result="idle"><h3>{t("Your result will show here", "Su resultado aparecerá aquí")}</h3><p>{t("Check the boxes that apply, then press See my result.", "Marque las casillas que correspondan y luego presione Ver mi resultado.")}</p></div>
      <div class="res res-urgent" data-result="urgent" hidden><span class="res-tag">{t("Call us before your next fire", "Llámenos antes de su próximo fuego")}</span><h3>{t("Stop using it until it is inspected", "No lo use hasta que se inspeccione")}</h3><p>{t("Something you checked can be a sign of a safety problem. Do not use the fireplace or stove until it has been inspected. If a carbon monoxide alarm is sounding, get everyone outside and call 911.", "Algo que marcó puede ser señal de un problema de seguridad. No use el hogar ni la estufa hasta que se inspeccione. Si está sonando una alarma de monóxido de carbono, saque a todos afuera y llame al 911.")}</p><div class="hero-actions">{call}{est}</div></div>
      <div class="res res-soon" data-result="soon" hidden><span class="res-tag">{t("Schedule a visit", "Programe una visita")}</span><h3>{t("Time for a sweep and inspection", "Es hora de un deshollinado y una inspección")}</h3><p>{t("What you checked usually means buildup, wear or water getting in. Schedule a sweep and inspection before your next fire, and we will find the cause and tell you what, if anything, needs repair.", "Lo que marcó suele indicar acumulación, desgaste o entrada de agua. Programe un deshollinado y una inspección antes de su próximo fuego, y encontraremos la causa y le diremos qué necesita reparación, si es que algo lo necesita.")}</p><div class="hero-actions">{book}{est}</div></div>
      <div class="res res-plan" data-result="plan" hidden><span class="res-tag">{t("Plan ahead", "Planifique")}</span><h3>{t("Plan a visit at the right time", "Programe una visita en el momento adecuado")}</h3><p>{t("Nothing you checked points to a problem today, but your situation calls for a closer look.", "Nada de lo que marcó indica un problema hoy, pero su situación requiere una revisión más detallada.")}</p><div class="hero-actions">{book}{est}</div></div>
      <div class="res res-ok" data-result="ok" hidden><span class="res-tag">{t("Looking good", "Todo bien")}</span><h3>{t("You are in good shape", "Su chimenea está en buen estado")}</h3><p>{t("Nothing you checked points to a problem. Keep up a yearly inspection, as the CSIA and NFPA 211 recommend, and call us if anything changes.", "Nada de lo que marcó indica un problema. Mantenga una inspección anual, como recomiendan la CSIA y la norma NFPA 211, y llámenos si algo cambia.")}</p><div class="hero-actions">{book}</div></div>
      <ul class="res-notes">
        <li data-note-for="sale" hidden>{t("Buying or selling: a Level 2 inspection with a camera is recommended whenever a home changes hands.", "Compra o venta: se recomienda una inspección de Nivel 2 con cámara cada vez que una casa cambia de dueño.")}</li>
        <li data-note-for="change" hidden>{t("New stove, insert or fuel: this calls for a Level 2 inspection, and often a liner sized to the new appliance.", "Estufa, inserto o combustible nuevo: requiere una inspección de Nivel 2 y, a menudo, un revestimiento del tamaño del nuevo aparato.")}</li>
        <li data-note-for="heavy" hidden>{t("Heavy use: burning several times a week can call for more than one sweep each season.", "Uso intenso: quemar leña varias veces por semana puede requerir más de un deshollinado por temporada.")}</li>
        <li data-note-for="rental" hidden>{t("Rental or seasonal home: empty weeks invite nests and water. See our page for vacation rental hosts.", "Alquiler o casa de temporada: las semanas vacías atraen nidos y agua. Vea nuestra página para anfitriones de alquileres vacacionales.")} <a href="vacation-rentals.html">{t("Rental hosts", "Para anfitriones")} {I['arrow']}</a></li>
      </ul>
    </div>
    <p class="note-sm">{t("This self-check is a guide, not an inspection. Only a certified inspection can confirm the condition of your chimney.", "Esta autoevaluación es una guía, no una inspección. Solo una inspección certificada puede confirmar el estado de su chimenea.")}</p>
  </aside>
</div></section>
""" + B["cta_band"]()
    return B["head"](t("Chimney Self-Check | Is Your Chimney Due for Service? | Rosas Chimney Services", "Autoevaluación de chimenea | ¿Su chimenea necesita servicio? | Rosas Chimney Services"),
                     t("Take a one-minute chimney self-check to see whether your fireplace or stove needs a sweep, an inspection or a call today. From Rosas Chimney Services, CSIA Certified Sweep #11978.",
                       "Haga una autoevaluación de un minuto para saber si su hogar o estufa necesita un deshollinado, una inspección o una llamada hoy. De Rosas Chimney Services, deshollinador certificado CSIA n.º 11978."),
                     "chimney-check.html") + B["header"]("chimney-check.html") + body + B["footer"]()

PROMO = (t("Not sure your chimney needs service?", "¿No sabe si su chimenea necesita servicio?"), t("Take our one-minute self-check", "Haga nuestra autoevaluación de un minuto"),
         t("Own a cabin or vacation rental?", "¿Tiene una cabaña o un alquiler vacacional?"), t("Chimney care built around your bookings", "Cuidado de chimeneas según sus reservas"),
         t("Self-Check", "Autoevaluación"), t("Rental Hosts", "Para anfitriones"))
