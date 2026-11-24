# Filip Johansson — portfolio site

Job-search portfolio for Filip Johansson (M.Sc. Design & Product Development, Linköping University). Static site on GitHub Pages, deployed from `main` / root. No build step on GitHub: commit the generated HTML.

## Structure
- `index.html`: Work page. Hero, "Selected works" with four 4:5 project tiles (Celina, Modulix, ORIS, Åbacka), "What I bring", "Areas I can help with", contact footer.
- `about.html`: About page. Dark theme (`body.dark`), third-person professional text, greyscale portrait cropped to the upper body.
- `projects/*.html`: case pages. **Generated. Do not hand-edit.** Edit `tools/build_pages.py`, then run `python3 tools/build_pages.py`.
- `assets/style.css`: all styles. `assets/main.js`: reveal animations, reduced motion, year.
- `assets/img/`: images (JPEG, max about 1600 px on the long side for photos). `assets/video/`: Celina exploded-view video and poster.
- `assets/models/modulix-*.glb`: Modulix configurations for `<model-viewer>` (`assets/js/model-viewer.min.js`). Rebuild them with `python3 tools/modulix/build_models.py` (needs trimesh, pygltflib, numpy).
- `.nojekyll` must stay.

## Design rules (agreed with Filip)
- English, light and clean, inspired by above.se: full-bleed covers, large images, chapters with a small label on the left and the text on the right.
- Font: Inter Tight (self-hosted). Section labels are subtle and small, with no dots or numbering.
- Header: fixed, transparent, `mix-blend-mode: difference`. Nav shows only "Work" and "About". Logo text is just "Filip Johansson".
- Images line up evenly: **two images per row, same aspect ratio**, or one full-width image. No three-image rows that don't line up.
- Project texts describe **what the project was about**. No "My role", "Team" or "I did / we did" framing, and don't name other team members or the other lamps (Nikolina, Paulina) on the Celina page.
- Privacy: no phone number, birthdate or references anywhere. CV "on request".
- Placeholders (`ph(...)`) mark where Filip will add his own sketches or CAD views.

## Projects
- **Celina** (focus project): bachelor's thesis for Reijmyre Glasbruk, 2026. A ceiling lamp where a coloured glass floats inside a clear *Lina* vase. Sections: Introduction → Three principles of light (Celina = ambient luminescence) → Process (light lab, sketches No. 1–6, test versions) → Production & assembly → Light (GX53, 2700 K, 500 lm) → Vernissage → big poster at the end.
- **Modulix**: outdoor modular furniture, Materials for Design, 2025. The Introduction includes the interactive 3D viewer with tabs, in this order: **Sofa (default)**, Side table, Sun lounger, Winter storage.
  - Sofa: 2 seat modules plus upright armrests (open frame facing outward) plus 2 backrest modules, with cushions.
  - Lounger: 2 lying modules plus 1 upright backrest, with cushions.
  - Storage: one stack of 4 modules with the cushions inside.
- **ORIS**: year 1, 2024. Audio family S1/S2/S3 with an Epishine solar cell in the headphone headband. Keep the name ORIS.
- **Åbacka**: year 1, 2024. Outdoor furniture by Stångån, Linköping.

## 3D models and the Claude preview
The Claude artifact preview can't serve `.glb` files and blocks `data:` URIs. Each config button therefore has `data-alt="/_blob/<id>"`, which points to a copy uploaded as an artifact asset. The page falls back to it only when the relative `.glb` fails to load. On GitHub Pages the relative `.glb` is used. If a model changes, re-upload it as an asset and update the `/_blob/` id in `tools/build_pages.py`.

## Workflow
Make changes, regenerate the pages, check the result visually, then commit and push to `main`. GitHub Pages redeploys automatically.
