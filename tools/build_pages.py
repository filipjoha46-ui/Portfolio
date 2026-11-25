"""Generates the four case-study pages (large-image layout)."""
import os, glob

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "projects")
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(OUT + "/*.html"):
    os.remove(f)

ICON = '<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 32 32%22%3E%3Crect width=%2232%22 height=%2232%22 rx=%226%22 fill=%22%23141414%22/%3E%3Ctext x=%2216%22 y=%2222%22 font-family=%22Arial%22 font-size=%2215%22 font-weight=%22600%22 fill=%22%23F2F1ED%22 text-anchor=%22middle%22%3EFJ%3C/text%3E%3C/svg%3E">'


def head(title, desc, og):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Filip Johansson</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title} — Filip Johansson">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="../assets/img/{og}">
{ICON}
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="logo" href="../index.html">Filip Johansson</a>
    <nav class="nav">
      <a href="../index.html" aria-current="page">Work</a>
      <a href="../about.html">About</a>
    </nav>
  </div>
</header>
<main>
"""


def foot(next_href, next_name):
    return f"""
  <div class="wrap">
    <div class="next">
      <p class="label">Next project</p>
      <a class="display" href="{next_href}">{next_name} →</a>
    </div>
  </div>
</main>
<footer class="contact" id="contact">
  <div class="wrap">
    <p class="eyebrow">Contact</p>
    <div class="contact-links">
      <a href="mailto:filip.joha46@gmail.com">filip.joha46@gmail.com</a>
      <a href="https://www.linkedin.com/in/filip-johansson-716963175/" target="_blank" rel="noopener">LinkedIn ↗</a>
      <a href="../index.html">All projects</a>
    </div>
    <div class="foot"><span>© <span id="year">2026</span> Filip Johansson</span><span>Linköping · Taipei</span></div>
  </div>
</footer>
<script src="../assets/main.js"></script>
</body>
</html>
"""


def cover(src, alt, pos="50% 50%"):
    return f'  <div class="case-cover"><img src="../assets/img/{src}" alt="{alt}" style="object-position:{pos}"></div>\n'


def cover_video(src, poster, alt):
    return f'  <div class="case-cover"><video autoplay muted loop playsinline preload="metadata" poster="../assets/video/{poster}" aria-label="{alt}"><source src="../assets/video/{src}" type="video/mp4"></video></div>\n'


def video_band(src, poster, alt, cap=None):
    c = f'<p class="cap wrap">{cap}</p>' if cap else ""
    return f'  <div class="vband reveal"><video autoplay muted loop playsinline preload="metadata" poster="../assets/video/{poster}" aria-label="{alt}"><source src="../assets/video/{src}" type="video/mp4"></video></div>{c}\n'


def scrolly(src, poster, alt):
    return f"""  <section class="scrolly" data-scrolly aria-label="{alt}">
    <div class="scrolly-sticky">
      <video muted playsinline preload="auto" poster="../assets/video/{poster}"><source src="../assets/video/{src}" type="video/mp4"></video>
      <div class="scrolly-fade"></div>
      <p class="scrolly-hint">Scroll</p>
    </div>
  </section>
"""


def split_intro(img, alt, eyebrow, title, lead, meta):
    m = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
    return f"""  <section class="case-split wrap">
    <div class="split-text reveal"><p class="eyebrow">{eyebrow}</p><h1 class="display">{title}</h1><p class="lead">{lead}</p><dl class="meta">{m}</dl></div>
    <figure class="split-img"><img src="../assets/img/{img}" alt="{alt}"></figure>
  </section>
"""


def intro(eyebrow, title, lead, meta):
    m = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in meta)
    return f"""  <section class="case-intro wrap">
    <div class="case-head">
      <div class="reveal"><p class="eyebrow">{eyebrow}</p><h1 class="display">{title}</h1><p class="lead">{lead}</p></div>
      <dl class="meta reveal">{m}</dl>
    </div>
  </section>
"""


def chapter(label, title, body, media=""):
    return f"""  <section class="chapter wrap">
    <div class="chapter-text reveal">
      <p class="label">{label}</p>
      <div><h2>{title}</h2>{body}</div>
    </div>
{media}  </section>
"""


def fig(src, alt, cls="r45", cap=None):
    f = f'<figure class="{cls}"><img src="../assets/img/{src}" alt="{alt}" loading="lazy"></figure>'
    return f'<div class="figwrap">{f}<p class="cap">{cap}</p></div>' if cap else f


def ph(title, text, cls="r45"):
    return f'<div class="ph {cls}"><b>Placeholder · {title}</b>{text}</div>'


def svgfig(name, cls="r11 fit"):
    svg = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "diagrams", name), encoding="utf-8").read().strip()
    return f'<figure class="{cls}">{svg}</figure>'


def statement(label, text, body="", media=""):
    """A chapter that opens with one large sentence instead of a heading and paragraphs.
    Wrap the second half of the sentence in <span class="mute"> to set it in grey."""
    return f"""  <section class="chapter wrap">
    <div class="chapter-text reveal">
      <p class="label">{label}</p>
      <div><h2 class="statement">{text}</h2>{body}</div>
    </div>
{media}  </section>
"""


def cols(items, numbered=False, on=None):
    """A full-width row of short text columns: process steps, principles or products.
    items: (title, text) pairs. numbered adds 01, 02... on: index of the item to highlight (others are dimmed)."""
    out = []
    for i, (t, x) in enumerate(items):
        cls = "" if on is None else (" on" if i == on else " dim")
        n = f'<span class="n">{i + 1:02d}</span>' if numbered else ""
        out.append(f'<div class="col{cls}">{n}<h3>{t}</h3><p>{x}</p></div>')
    return f'    <div class="cols reveal" style="--n:{len(items)}">{"".join(out)}</div>\n'


def specs(rows):
    """A two-column list of facts (label, value) instead of a paragraph."""
    r = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in rows)
    return f'<dl class="specs">{r}</dl>'


def media(cols, *items, cap=None):
    c = f'<p class="cap">{cap}</p>' if cap else ""
    return f'    <div class="media {cols} reveal">{"".join(items)}</div>{c}\n'


def bleed(src, alt, crop=False, pos="50% 50%", cap=None):
    c = f'<p class="cap wrap">{cap}</p>' if cap else ""
    cl = "bleed crop" if crop else "bleed"
    return f'  <div class="{cl} reveal"><img src="../assets/img/{src}" alt="{alt}" loading="lazy" style="object-position:{pos}"></div>{c}\n'


def quote(text):
    return f'  <div class="wrap"><p class="quote reveal">{text}</p></div>\n'


def write(name, html):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)
    print("wrote", name)


# ======================================================== CELINA
h = head("Celina", "Celina, a floating ceiling lamp for Reijmyre Glasbruk. Bachelor's thesis, Linköping University 2026.", "card-celina.jpg")
h += cover("cel-header-wide.jpg", "Celina pendant with blue inner glass above a set dining table in a bright room", "50% 30%")
h += intro("Reijmyre Glasbruk · Bachelor's thesis · 2026", "Celina",
           "A ceiling lamp where glass meets metal to create a floating design, built to celebrate the colours Reijmyre Glasbruk is known for.",
           [("Year", "2026"), ("Client", "Reijmyre Glasbruk"),
            ("Capabilities", "Industrial design, mechanical design, prototyping, lighting")])
h += video_band("celina-exploded.mp4", "celina-exploded.jpg", "Animated exploded view of Celina and its components")

h += statement("Introduction", 'Existing glass, new light. <span class="mute">Two pieces from Reijmyre\'s <i>Lina</i> collection, one inside the other, turned into a ceiling lamp.</span>', """
      <p class="st-body">A bachelor's thesis for Reijmyre Glasbruk, which has blown glass by hand since 1810: reproducible lighting from glass already in production, built on standard components.</p>""",
    media("c2", fig("cel-family.jpg", "Three Celina lamps with blue, green and amber inner glass", "r45"), fig("cel-detail.jpg", "Close-up of Celina with blue inner glass by a window over the sea", "r45")))
h += chapter("Three principles of light", "Built on ambient luminescence.", """
      <p>Lighting designer Richard Kelly describes three kinds of light. Celina is built on the first.</p>""",
    cols([("Ambient luminescence", "Soft, shadowless light that fills the room. The principle behind Celina."),
          ("Focal glow", "Directed light that draws the eye to one place."),
          ("Play of brilliants", "Sparkle and reflections that bring a space to life.")], on=0) +
    media("", fig("cel-principles.jpg", "Diagram of Richard Kelly's three principles of light in a living room", "r32 fit")))
h += chapter("Process", "From light lab to floating glass.", "",
    cols([("Light lab", "Testing light sources, colour temperature and how light travels through Reijmyre's glass."),
          ("Insight", "Coloured glass tints everything and can't stop glare, so the source is hidden and the light lifts the colour."),
          ("Moodboard and sketches", "Elegant, ambient, classic, Scandinavian and inviting. Of the early concepts, No. 3 became Celina."),
          ("Test versions", "Physical tests to judge proportions, hanging height and the glow of the inner glass.")], numbered=True) +
    media("", fig("cel-moodboard.jpg", "Moodboard with five images labelled elegant, ambient, classic, Scandinavian and inviting", "r169"), cap="Moodboard defining the expression of the lamp.") +
    media("c2", fig("cel-lab-grid.jpg", "Twelve light-lab tests with different light sources and Reijmyre glass", "r11 fit"), fig("cel-sketches.jpg", "Early concept sketches No. 1 to No. 6", "r11 fit"), cap="Light-lab tests and early concept sketches. Celina grew out of No. 3.") +
    media("c2", fig("cel-pink-glass.jpg", "Pink Lina glass with a water-jet cut opening for the cable and socket", "r34"), fig("cel-pink-test.jpg", "An early test version in pink glass hanging from its cable", "r34"), cap="An early test in pink glass, with a water-jet cut opening.") +
    media("c2", fig("cel-proto.jpg", "Early test version of Celina with a blue inner glass", "r34"), fig("cel-proto-hang.jpg", "Test version hanging in the workshop to judge height and proportions", "r34"), cap="Test versions on the bench and hanging in the workshop."))

h += chapter("Production &amp; assembly", "Optimised for production, easy to assemble.", """
      <p>Everything except the glass is standard or simple to make, and the construction tolerates the natural variation of hand-blown glass.</p>""" + specs([
        ("Glass", "Existing <i>Lina</i> vases from Reijmyre, no new moulds"),
        ("Metal parts", "Three CNC-turned aluminium parts, modelled in Fusion 360"),
        ("Light source", "GX53 LED puck, fully hidden"),
        ("Suspension", "Inner vase on three 1 mm wires, tensioned in the lock ring"),
        ("Hanging", "300 mm gravity pipe keeps the lamp straight"),
        ("Ceiling", "Bent bracket with strain relief keeps the canopy small")]),
    media("", fig("cel-exploded.jpg", "Exploded view of Celina with every part named: metal wires, Lina vase, lock ring, outer Lina vase, diffuser, GX53, mounting bracket, top cap and gravity pipe", "fit")) +
    media("c2", fig("cel-pipe.jpg", "The gravity pipe mounted in the CNC-turned aluminium top cap", "r34"), fig("cel-bracket.jpg", "Bent sheet-metal bracket with strain relief mounted on the GX53 holder", "r34"), cap="The turned top cap with its gravity pipe, and the bent sheet-metal bracket with built-in strain relief.") +
    media("c2", fig("cel-wiring.jpg", "Fitting the bracket and GX53 holder into the top cap", "r34"), fig("cel-lit.jpg", "The assembled lamp lit, with the blue inner glass glowing inside the ribbed outer glass", "r34"), cap="Fitting the light source into the top cap, and the assembled lamp lit."))

h += statement("Light", 'Soft ambience around the lamp, <span class="mute">useful light on the table below it.</span>', """
      <p class="st-body">The top of the inner vase is cut off to send an even beam downwards and a fabric diffuser prevents glare, while the ribbed outer glass glows softly around it.</p>
      <div class="facts-row"><div>GX53<small>LED puck</small></div><div>2700 K<small>Colour temperature</small></div><div>500 lm<small>Luminous flux</small></div><div>300 mm<small>Gravity pipe</small></div></div>""",
    media("c2", svgfig("celina-light.svg", "r11 fit"), fig("cel-diffuser.jpg", "How the fabric diffuser scatters light", "r11 fit")))

h += chapter("Vernissage", "Shown at the final vernissage.", """
      <p>Presented at Linköping University in a staged dining scene, together with Reijmyre's glass.</p>""",
    media("c2", fig("cel-vernissage-1.jpg", "Celina at the vernissage", "r34"), fig("cel-vernissage-2.jpg", "Celina lit above the dinner table at the vernissage", "r34")))
h += quote('Glass Reijmyre already makes, <span class="mute">turned into a premium light.</span>')
h += bleed("cel-hero.jpg", "Celina hanging by a large window over the sea in a timber room", crop=True, pos="50% 45%")
write("celina.html", h + foot("modulix.html", "Modulix"))

# ======================================================== MODULIX
h = head("Modulix", "Modulix, modular outdoor furniture in perforated metal. Materials for Design, Linköping University 2025.", "card-modulix.jpg")
h += cover("mod-hero-wide.jpg", "Modulix sofa module on a wooden deck in a garden", "40% 60%")
h += intro("Materials for Design · 2025", "Modulix",
           "Modular outdoor furniture in perforated aluminium, designed to get people out into their gardens.",
           [("Year", "2025"), ("Context", "Materials for Design, Linköping University"),
            ("Theme", "Inconcrete brutalism"), ("Direction", "UT&amp;NJUT, get out and enjoy")])
h += statement("Introduction", 'One aluminium module, clamped together, <span class="mute">becomes a side table, a sofa or a sun lounger, and stacks away when summer ends.</span>', """
      <p class="st-body">Outdoor furniture for a customer group in Vadstena that handles rain and changing weather, dries fast and never needs carrying in.</p>
      <div class="facts-row"><div>1<small>Module</small></div><div>4<small>Configurations</small></div><div>8.5 kg<small>Per module</small></div></div>""",
    """
    <div class="viewer reveal">
      <script type="module" src="../assets/js/model-viewer.min.js"></script>
      <div class="cfg-tabs" role="tablist" aria-label="Modulix configurations">
        <button role="tab" aria-selected="true" data-src="modulix-sofa.glb" data-alt="/_blob/3c91870297e62bc04a1f9375acbfe499" data-cap="Two seat modules with upright modules as armrests and backrest, plus cushions.">Sofa</button>
        <button role="tab" aria-selected="false" data-src="modulix-single.glb" data-alt="/_blob/92ab692d7303f423be727a82c0cbbb20" data-cap="One module as a side table or stool.">Side table</button>
        <button role="tab" aria-selected="false" data-src="modulix-lounger.glb" data-alt="/_blob/804200318404638ceea0e552f4bab41f" data-cap="Two modules end to end with an upright backrest and a full-length cushion.">Sun lounger</button>
        <button role="tab" aria-selected="false" data-src="modulix-stack.glb" data-alt="/_blob/233151c03e19b26ea81ecd89e0fcc364" data-cap="One stack for winter, with the cushions stored inside each module.">Winter storage</button>
      </div>
      <model-viewer id="mod-viewer" src="../assets/models/modulix-sofa.glb" alt="Interactive 3D model of Modulix configurations" camera-controls disable-zoom loading="lazy" interaction-prompt="auto" interaction-prompt-style="basic" interaction-prompt-threshold="600" shadow-intensity="0.8" exposure="1.05" environment-image="neutral" camera-orbit="35deg 70deg auto" ar ar-modes="webxr scene-viewer quick-look" touch-action="pan-y">
        <div slot="interaction-prompt" class="drag-hint"><svg viewBox="0 0 64 32" aria-hidden="true"><path class="arr" d="M8 16l5-5M8 16l5 5"/><path class="arr" d="M56 16l-5-5M56 16l-5 5"/><g class="mouse"><rect x="24" y="5" width="16" height="23" rx="8"/><path d="M32 9v5"/></g></svg><span class="hint-mouse">Drag to rotate</span><span class="hint-touch">Swipe to rotate</span></div>
      </model-viewer>
      <p class="cap"><span id="mod-cap">Two seat modules with upright modules as armrests and backrest, plus cushions.</span> Drag to rotate.</p>
      <script>
        (function(){var mv=document.getElementById('mod-viewer'),cap=document.getElementById('mod-cap'),bs=document.querySelectorAll('.cfg-tabs button'),cur=bs[0];
        mv.addEventListener('error',function(){var a=cur.dataset.alt;if(a&&mv.getAttribute('src')!==a)mv.setAttribute('src',a);});
        bs.forEach(function(b){b.addEventListener('click',function(){cur=b;bs.forEach(function(x){x.setAttribute('aria-selected',x===b)});mv.setAttribute('src','../assets/models/'+b.dataset.src);cap.textContent=b.dataset.cap;});});})();
      </script>
    </div>
""")
h += chapter("Process", "From sketch to sheet metal.", "",
    cols([("Brutalist forms", "A wide start with heavy, mesh-like shapes from the theme."),
          ("Repeating forms", "One shape used again and again to build different pieces."),
          ("Module system", "A single rounded module that becomes every piece of furniture."),
          ("Models", "Foam blocks, then a sheet-metal scale model, to test proportions and joints.")], numbered=True) +
    media("", fig("mod-sketches.jpg", "Sketches moving from brutalist mesh forms through repeating forms to a system of modules", "r169 fit"), cap="From brutalist forms to repeating forms to a module system.") +
    media("c2", fig("mod-foam-1.jpg", "Blue foam model of modules combined into a chair", "r11"), fig("mod-foam-2.jpg", "Blue foam blocks testing how modules combine", "r11"), cap="Foam models testing how the modules combine.") +
    media("c2", fig("mod-process-1.jpg", "Cutting perforated sheet for the scale model", "r34"), fig("mod-model.jpg", "The finished Modulix scale model as a sofa", "r34"), cap="Building the scale model."))
h += chapter("Technical details", "Light, dry and simple to assemble.", specs([
        ("Module", "Perforated aluminium sheet, about 8.5 kg, light enough to carry and stack"),
        ("Production", "Cut from flat sheet, perforated and bent twice, with an inner frame of bent tube in a two-part profile"),
        ("Clamp and feet", "Powder-coated steel with EPDM rubber, protecting both the module and the deck"),
        ("Mounting", "Modules bolt together through the side walls with one clamp"),
        ("Cushions", "Polyester mesh with quick-dry foam and a cover in solution-dyed polyester")]),
    media("", fig("mod-production.jpg", "Production steps: flat sheet, perforated, bent twice, with bent tube frames in a two-part profile; and the clamp joining two modules", "fit"), cap="Production from flat sheet to module, and the clamp that joins modules.") +
    media("c2", fig("mod-clamp.jpg", "Clamp joining two modules", "r45"), fig("mod-cad.jpg", "CAD model of a single Modulix module with its perforated sheet and tube frame", "r45 fit")))
h += quote('Create, rebuild and adapt. <span class="mute">Modulix makes it possible.</span>')
h += bleed("mod-exhibit.jpg", "The Modulix scale model in front of the project poster at the exhibition", crop=True, pos="50% 55%")
write("modulix.html", h + foot("oris.html", "ORIS"))

# ======================================================== ORIS
h = head("ORIS", "ORIS, a family of audio products with a shared design language and headphones powered by Epishine's flexible solar cells. Linköping University 2024.", "card-oris.jpg")
h += cover("oris-hero.jpg", "ORIS headphones on aluminium stands", "60% 50%")
h += intro("Course project · Year 1 · 2024", "ORIS",
           "A family of three audio products with one design language, where the headphones harvest light through a flexible solar cell in the headband.",
           [("Year", "2024"), ("Context", "Year 1, Linköping University"),
            ("Products", "S1 compact speaker, S2 home speaker, S3 headphones"), ("Capabilities", "Industrial design, CMF, CAD, rendering")])

h += statement("Introduction", 'Three products, one design language: <span class="mute">calm, soft volumes broken by precise horizontal grooves.</span>', """
      <p class="st-body">The brief was to develop a technical product with clear requirements on production, users and design, then extend it into a product family.</p>""",
    media("c3", fig("oris-s1.jpg", "S1 compact speaker with horizontal grooves", "r45"), fig("oris-s3.jpg", "S3 headphones on their aluminium stand", "r45"), fig("oris-s2.jpg", "S2 home speaker with horizontal grooves", "r45")) +
    cols([("S1", "Compact speaker. Shares its organic, pebble-like form with the headphones."),
          ("S3", "Headphones with a solar cell in the headband."),
          ("S2", "Home speaker. Shares the horizontal grooves with S1.")]))
h += statement("Materials", 'Cool, exact metal <span class="mute">against soft, tactile textile.</span>', """
      <p class="st-body">Materials chosen to echo the calm of nature: metal frames the sound and gives a precise feel, while mesh textile adds warmth where the products meet the body.</p>""")
h += statement("Energy", 'Headphones that charge <span class="mute">from the light around them.</span>', """
      <p class="st-body">A thin, flexible printed solar cell from Epishine, a Linköping company, follows the curve of the S3 headband and tops up the battery whenever the headphones are worn or left in a lit room. The cell becomes part of the look instead of being hidden.</p>
      <p class="credit-logo"><span>Solar cell technology</span><img src="../assets/img/epishine-logo.png" alt="Epishine" width="134" height="29"></p>""",
    media("c2", fig("oris-solar.jpg", "Close-up of the S3 headband with the integrated solar cell", "r45"), fig("oris-epishine.jpg", "A flexible Epishine solar cell bent between two fingers", "r45"), cap="Right: Epishine's flexible solar cell. Photo: Epishine."))

h += chapter("Calculation", "What the light is worth.", """
      <p>A theoretical estimate of what the headband cell could add on an ordinary day, using typical values for Epishine's printed organic solar cells. Not measured on a prototype.</p>
      <div class="facts-row"><div>22 %<small>Of daily energy from light</small></div><div>+28 %<small>More days between charges</small></div><div>&minus;22 %<small>Battery size, same charging</small></div><div>55 g<small>CO&#8322;e saved per headphone</small></div></div>""",
    """    <div class="bars reveal" role="img" aria-label="Daily energy: 150 mWh used, 33 mWh harvested from light. Battery: 2.5 Wh without the cell, 1.95 Wh with it.">
      <p class="bars-title">A typical day</p>
      <div class="bar-row"><span class="bar-label">Used</span><div class="bar-track"><i class="use" style="width:100%"></i></div><span class="bar-val">150 mWh</span></div>
      <div class="bar-row"><span class="bar-label">Harvested from light</span><div class="bar-track"><i class="in" style="width:6.1%"></i><i class="out" style="width:15.9%"></i></div><span class="bar-val">33 mWh</span></div>
      <p class="bar-key"><span class="kitem"><span class="k in"></span>Indoors, 11 h at 500 lux: 9 mWh</span><span class="kitem"><span class="k out"></span>Outdoors, 1 h overcast: 24 mWh</span></p>
      <p class="bars-title">Battery for the same charging interval</p>
      <div class="bar-row"><span class="bar-label">Without the cell</span><div class="bar-track"><i class="bat" style="width:100%"></i></div><span class="bar-val">2.5 Wh</span></div>
      <div class="bar-row"><span class="bar-label">With the cell</span><div class="bar-track"><i class="bat" style="width:78%"></i><i class="saved" style="width:22%"></i></div><span class="bar-val">1.95 Wh</span></div>
    </div>
    <div class="chapter-text reveal calc-notes">
      <p class="label">Assumptions</p>
      <div>""" + specs([
        ("Solar cell", "About 50 cm&sup2; of printed organic cell along the S3 headband"),
        ("Indoor light", "500 lux office light, about 10 % conversion: 0.8 mW from the whole cell"),
        ("Outdoor light", "10,000 lux on an overcast day, about 5 % conversion: 24 mW"),
        ("Use", "Bluetooth with noise cancelling at about 50 mW, worn 3 h a day"),
        ("Battery", "2.5 Wh, 50 h of play, at 200 Wh/kg: 12.5 g"),
        ("Footprint", "About 100 kg CO&#8322;e per kWh of lithium-ion battery produced")]) + """
      <p class="calc-note">Result: 33 of 150 mWh a day comes from light. The same battery lasts about 21 days instead of 17 between charges, or a 1.95 Wh battery keeps today's interval. That is 0.55 Wh and about 2.7 g less battery, roughly 2 g net with the cell film, and about 55 g CO&#8322;e per headphone: around 5.5 tonnes per 100,000 units. The cell's own footprint is not included. A sunny day would harvest far more.</p></div>
    </div>
""")
h += chapter("Process", "Sketch, model, refine.", ph("Sketches & CAD", "Add early form sketches and CAD views of the headphones and speakers.", "txt"))
h += bleed("oris-family.jpg", "The ORIS family: S1, S3 and S2 side by side")
write("oris.html", h + foot("abacka.html", "Åbacka"))

# ======================================================== ÅBACKA
h = head("Åbacka", "Åbacka, site-specific outdoor furniture by Stångån in Linköping. Linköping University 2024.", "card-abacka.jpg")
h += cover("aba-hero-wide.jpg", "Åbacka deck, slatted loungers and pergola by the river", "50% 60%")
h += intro("Course project · Year 1 · 2024", "Åbacka",
           "Site-specific outdoor furniture, with form, function and material taken from the place itself.",
           [("Year", "2024"), ("Context", "Year 1, Linköping University"),
            ("Location", "Stångån, Linköping")])
h += statement("Introduction", 'Outdoor furniture for one place: <span class="mute">the riverbank along Stångån in Linköping.</span>', """
      <p class="st-body">The work started on site, studying how people move along the path, where they stop and how the slope meets the water.</p>""",
    media("c2", fig("aba-site-1.jpg", "The path along Stångån", "r45"), fig("aba-site-2.jpg", "People walking along the riverbank", "r45")))
h += quote("From generation to generation.")
h += chapter("Concept", "Shaped by the body, built to last.", """
      <p>A rational origin in production technology and, above all, in the shape of the human body.</p>""" + specs([
        ("Slats", "Quartz composite"),
        ("Structure", "Robust steel blades"),
        ("Form", "Follows the body, so no part repeats another")]),
    media("c2", ph("Sketches", "Add your concept sketches of the loungers and pergola.", "r45"), fig("aba-proc-3.jpg", "Cutting sections for the model", "r45")))
h += chapter("Model", "Built slice by slice.", """
      <p>The form was developed through physical models, building the loungers from stacked, individually cut sections, the same logic as the full-scale slats.</p>""",
    media("c3", fig("aba-proc-1.jpg", "Model parts on the workshop table", "r34"), fig("aba-proc-4.jpg", "Assembling the model base", "r34"), fig("aba-model-1.jpg", "Finished model", "r34")))
h += statement("Result", 'A place where people meet, <span class="mute">facing both the water and the path.</span>', """
      <p class="st-body">The tree-like pergola connects the path with the meeting place and gives shade and a sheltered feeling.</p>""",
             media("", fig("aba-sheet.jpg", "Åbacka presentation sheet", "fit paper")))
write("abacka.html", h + foot("celina.html", "Celina"))
