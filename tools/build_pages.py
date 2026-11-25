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

h += chapter("Introduction", "Existing glass, new light.", """
      <p>A bachelor's thesis for Reijmyre Glasbruk, which has blown glass by hand since 1810. The brief was to turn their existing <i>Lina</i> glass collection into reproducible lighting built on standard components. Celina pairs two pieces from the collection, using light to bring out the colour of the glass rather than depend on it.</p>""",
    media("c2", fig("cel-family.jpg", "Three Celina lamps with blue, green and amber inner glass", "r45"), fig("cel-detail.jpg", "Close-up of Celina with blue inner glass by a window over the sea", "r45")))

h += chapter("Three principles of light", "Built on ambient luminescence.", """
      <p>The project is based on lighting designer Richard Kelly's three principles of light: ambient luminescence, focal glow and play of brilliants. Celina is built on the first, a soft, shadowless light that fills the room.</p>""",
    media("", fig("cel-principles.jpg", "Diagram of Richard Kelly's three principles of light in a living room", "r32 fit")))

h += chapter("Process", "From light lab to floating glass.", """
      <p>The work started in a light lab, testing light sources, colour temperature and how light travels through Reijmyre's glass. Coloured glass tints everything and can't stop glare, so the source had to be hidden and the light had to lift the colour rather than depend on it.</p>
      <p>A moodboard then set the expression the lamp should carry: elegant, ambient, classic, Scandinavian and inviting. The insights and the moodboard fed straight into sketching. Of the early concepts, No. 3 became Celina: a small coloured vase suspended inside a large clear <i>Lina</i> vase. Physical test versions were used to judge proportions, hanging height and the glow of the inner glass before committing to the final construction.</p>""",
    media("", fig("cel-moodboard.jpg", "Moodboard with five images labelled elegant, ambient, classic, Scandinavian and inviting", "r169"), cap="Moodboard defining the expression of the lamp.") +
    media("c2", fig("cel-lab-grid.jpg", "Twelve light-lab tests with different light sources and Reijmyre glass", "r11 fit"), fig("cel-sketches.jpg", "Early concept sketches No. 1 to No. 6", "r11 fit"), cap="Light-lab tests and early concept sketches. Celina grew out of No. 3.") +
    media("c2", fig("cel-proto.jpg", "Early test version of Celina with a blue inner glass", "r34"), fig("cel-proto-hang.jpg", "Test version hanging in the workshop to judge height and proportions", "r34"), cap="Test versions on the bench and hanging in the workshop.") +
    media("c2", fig("cel-pink-glass.jpg", "Pink Lina glass with a water-jet cut opening for the cable and socket", "r34"), fig("cel-pink-test.jpg", "An early test version in pink glass hanging from its cable", "r34"), cap="An early test in pink glass, with a water-jet cut opening."))

h += chapter("Production &amp; assembly", "Optimised for production, easy to assemble.", """
      <p>Celina uses glass Reijmyre already blows, so no new moulds are needed. Everything else is standard or simple to make: a GX53 LED puck, three CNC-turned aluminium parts modelled in Fusion 360, and one bent sheet-metal bracket. The construction tolerates the natural variation of hand-blown glass.</p>
      <p>Assembly is just as simple. The glass is clamped mechanically between the top cap and the lower lock ring, and the inner vase hangs from three 1 mm wires tensioned in the lock ring, which adds to the floating effect. A 300 mm gravity pipe keeps the lamp hanging straight, the power cable runs hidden through the pendant tube, and the bracket with integrated strain relief lets the ceiling canopy stay small.</p>""" + ph("CAD / section view", "Add a Fusion 360 section view showing the parts.", "txt"),
    media("", fig("cel-exploded.jpg", "Exploded view of Celina with every part named: metal wires, Lina vase, lock ring, outer Lina vase, diffuser, GX53, mounting bracket, top cap and gravity pipe", "fit")) +
    media("c2", fig("cel-pipe.jpg", "The gravity pipe mounted in the CNC-turned aluminium top cap", "r34"), fig("cel-bracket.jpg", "Bent sheet-metal bracket with strain relief mounted on the GX53 holder", "r34"), cap="The turned top cap with its gravity pipe, and the bent sheet-metal bracket with built-in strain relief.") +
    media("c2", fig("cel-wiring.jpg", "Fitting the bracket and GX53 holder into the top cap", "r34"), fig("cel-lit.jpg", "The assembled lamp lit, with the blue inner glass glowing inside the ribbed outer glass", "r34"), cap="Fitting the light source into the top cap, and the assembled lamp lit."))

h += chapter("Light", "Soft ambience and useful light from one lamp.", """
      <p>The top of the inner vase is cut off so it directs an even beam downwards, and a fabric diffuser in the lock ring spreads the light and prevents glare. Most of the light falls through the inner vase onto the table, while the ribbed outer glass glows softly around it.</p>
      <div class="facts-row"><div>GX53<small>LED puck</small></div><div>2700 K<small>Colour temperature</small></div><div>500 lm<small>Luminous flux</small></div><div>300 mm<small>Gravity pipe</small></div></div>""",
    media("c2", svgfig("celina-light.svg", "r11 fit"), fig("cel-diffuser.jpg", "How the fabric diffuser scatters light", "r11 fit")))

h += chapter("Vernissage", "Shown at the final vernissage.", """
      <p>The finished prototype was presented at Linköping University in a staged dining scene, together with Reijmyre's glass. Celina gives Reijmyre a way to sell pieces they already make as a premium light.</p>""",
    media("c2", fig("cel-vernissage-1.jpg", "Celina at the vernissage", "r34"), fig("cel-vernissage-2.jpg", "Celina lit above the dinner table at the vernissage", "r34")))
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
h += chapter("Process", "From sketch to sheet metal.", """
      <p>The process started wide with brutalist, mesh-like forms, moved on to repeating forms, and finally landed on a module system where one part can become many: a single rounded module that combines into every piece of furniture.</p>""",
    media("", fig("mod-sketches.jpg", "Sketches moving from brutalist mesh forms through repeating forms to a system of modules", "r169 fit"), cap="From brutalist forms to repeating forms to a module system.") +
    media("c2", fig("mod-foam-1.jpg", "Blue foam model of modules combined into a chair", "r11"), fig("mod-foam-2.jpg", "Blue foam blocks testing how modules combine", "r11"), cap="Foam models testing how the modules combine.") +
    media("c2", fig("mod-process-1.jpg", "Cutting perforated sheet for the scale model", "r34"), fig("mod-model.jpg", "The finished Modulix scale model as a sofa", "r34"), cap="Building the scale model."))
h += chapter("Technical details", "Light, dry and simple to assemble.", """
      <ul class="points">
        <li><b>Aluminium module</b>Perforated aluminium sheet, about 8.5 kg per module, light enough to carry and stack.</li>
        <li><b>Clamp and feet</b>Powder-coated steel with EPDM rubber, protecting both the module and the deck.</li>
        <li><b>Quick-dry cushions</b>Polyester mesh with quick-dry foam and a cover in solution-dyed polyester.</li>
        <li><b>Simple mounting</b>Modules are bolted together through the side walls with one clamp.</li>
        <li><b>Production</b>Each module is cut from flat aluminium sheet, perforated and bent twice into its rounded shape. An inner frame of bent tube in a two-part profile stiffens it.</li>
      </ul>""",
    media("", fig("mod-production.jpg", "Production steps: flat sheet, perforated, bent twice, with bent tube frames in a two-part profile; and the clamp joining two modules", "fit"), cap="Production from flat sheet to module, and the clamp that joins modules.") +
    media("c2", fig("mod-clamp.jpg", "Clamp joining two modules", "r45"), fig("mod-cad.jpg", "CAD model of a single Modulix module with its perforated sheet and tube frame", "r45 fit")))
h += bleed("mod-exhibit.jpg", "The Modulix scale model in front of the project poster at the exhibition", crop=True, pos="50% 70%")
write("modulix.html", h + foot("oris.html", "ORIS"))

# ======================================================== ORIS
h = head("ORIS", "ORIS, a family of audio products with a shared design language and headphones powered by Epishine's flexible solar cells. Linköping University 2024.", "card-oris.jpg")
h += cover("oris-hero.jpg", "ORIS headphones on aluminium stands", "60% 50%")
h += intro("Course project · Year 1 · 2024", "ORIS",
           "A family of three audio products with one design language, where the headphones harvest light through a flexible solar cell in the headband.",
           [("Year", "2024"), ("Context", "Year 1, Linköping University"),
            ("Products", "S1 compact speaker, S2 home speaker, S3 headphones"), ("Capabilities", "Industrial design, CMF, CAD, rendering")])

h += chapter("Introduction", "One family, one language.", """
      <p>The brief was to develop a technical product with clear requirements on production, users and design, then extend it into a product family that proves a coherent design language.</p>
      <p>ORIS is a simple, Scandinavian family: the compact <b>S1</b> speaker, the larger <b>S2</b> home speaker and the <b>S3</b> headphones. Calm, soft volumes are broken by precise horizontal grooves, which tie the two speakers together, while S1 and S3 share the same organic, pebble-like forms.</p>""",
    media("c3", fig("oris-s1.jpg", "S1 compact speaker with horizontal grooves", "r45"), fig("oris-s3.jpg", "S3 headphones on their aluminium stand", "r45"), fig("oris-s2.jpg", "S2 home speaker with horizontal grooves", "r45")))

h += chapter("Materials", "Metal and textile in balance.", """
      <p>The material choices are meant to echo the calm of nature. Metal gives the products a precise, elegant feel and frames the sound, while a soft mesh textile on the headband and ear cushions adds warmth. Together they create a clear contrast: cool and exact against soft and tactile.</p>
      <ul class="points">
        <li><b>Metal</b>Polished shells and grooved bodies for an exact, premium expression.</li>
        <li><b>Mesh textile</b>Soft, breathable surfaces where the products meet the body.</li>
        <li><b>Horizontal grooves</b>One shared detail that reads across the whole family.</li>
        <li><b>Soft volumes</b>Rounded, organic forms that feel calm on a desk or a shelf.</li>
      </ul>""")

h += chapter("Energy", "Headphones that charge from the light around you.", """
      <p>The headband of S3 integrates a solar cell from Epishine, a Linköping company that prints thin, flexible organic solar cells made to harvest energy from everyday indoor light. Because the cell is flexible and only fractions of a millimetre thick, it can follow the curve of the headband instead of sitting on top as a separate panel.</p>
      <p>The concept: the headphones top up their battery whenever they are worn or left on the stand in a lit room, so they need charging less often. The cell also becomes part of the look, a fine pattern of cells in the headband that shows the technology instead of hiding it.</p>""",
    media("c2", fig("oris-solar.jpg", "Close-up of the S3 headband with the integrated solar cell", "r45"), fig("oris-epishine.jpg", "A flexible Epishine solar cell bent between two fingers", "r45"), cap="Right: Epishine's flexible solar cell. Photo: Epishine."))

h += chapter("Process", "Sketch, model, refine.", ph("Sketches & CAD", "Add early form sketches and CAD views of the headphones and speakers.", "txt"))
h += bleed("oris-family.jpg", "The ORIS family: S1, S3 and S2 side by side")
write("oris.html", h + foot("abacka.html", "Åbacka"))

# ======================================================== ÅBACKA
h = head("Åbacka", "Åbacka, site-specific outdoor furniture by Stångån in Linköping. Linköping University 2024.", "card-abacka.jpg")
h += cover("aba-hero-wide.jpg", "Åbacka deck, slatted loungers and pergola by the river", "50% 60%")
h += intro("Course project · Year 1 · 2024", "Åbacka",
           "Outdoor furniture for one specific place: the riverbank along Stångån in Linköping. Form, function and material taken from the site itself.",
           [("Year", "2024"), ("Context", "Year 1, Linköping University"),
            ("Location", "Stångån, Linköping")])
h += chapter("Introduction", "Reading the riverbank.", """
      <p>The brief was to create custom outdoor furniture for a place along Stångån, letting the site drive form, function and materials. The work started on site, studying how people move along the path, where they stop and how the slope meets the water.</p>""",
    media("c2", fig("aba-site-1.jpg", "The path along Stångån", "r45"), fig("aba-site-2.jpg", "People walking along the riverbank", "r45")))
h += quote("From generation to generation.")
h += chapter("Concept", "Shaped by the body, built to last.", """
      <p>Åbacka has a rational origin in production technology and, above all, in the shape of the human body. Slats in quartz composite on robust steel blades mean no part repeats another, creating a unique and durable place to sit, lie and gather by the water.</p>""",
    media("c2", ph("Sketches", "Add your concept sketches of the loungers and pergola.", "r45"), fig("aba-proc-3.jpg", "Cutting sections for the model", "r45")))
h += chapter("Model", "Built slice by slice.", """
      <p>The form was developed through physical models, building the loungers from stacked, individually cut sections, the same logic as the full-scale slats.</p>""",
    media("c3", fig("aba-proc-1.jpg", "Model parts on the workshop table", "r34"), fig("aba-proc-4.jpg", "Assembling the model base", "r34"), fig("aba-model-1.jpg", "Finished model", "r34")))
h += chapter("Result", "A place where people meet.", """
      <p>Åbacka was created to bring people together. The seating faces both the water and the path, so different groups can meet on the same piece of furniture.</p>
      <p>The tree-like pergola connects the path with the meeting place, while giving shade and a sheltered feeling.</p>""",
             media("", fig("aba-sheet.jpg", "Åbacka presentation sheet", "fit paper")))
write("abacka.html", h + foot("celina.html", "Celina"))
