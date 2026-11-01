# Prompt: Build the "Private Cloud Management" Cadence Map

Create one self-contained HTML file (`media/cadence-map.html`) that renders a 1280×720 slide showing who does what, when, and how in a VMware Private Cloud (VCF Operations) operating model. Below the slide, the same file holds supporting panels and a Technical details section. Then render the slide to PNG (`media/cadence-map.png`) with headless Chrome at 1280×760.

---

## 1. Page frame

- Body: 1280 px wide, flex column. Padding 40px top and bottom, 56px left and right.
- Font: "Segoe UI", Arial, Helvetica, sans-serif.
- Background: soft gradient, `linear-gradient(160deg, #FFFFFF 0%, #F3F6FB 100%)`.
- Text: #111111. Muted text: #5B6575 or #666666. Grid line color: #D0D0D0.
- Palette: navy, blue, and teal for team bars, with the four cadence colors below. Do not use black in the AI Dashboard area.
- Everything on the slide is static except the hover, focus, and click behavior in section 7.

## 2. Header

- H1: "Private Cloud Management" (30px, weight 600, #111111, letter-spacing -0.01em).
- Subtitle (15px, muted), two sentences with a line break after the first:
  - Line 1: "Who does what when, and how. Transforming from reactive to proactive operations management."
  - Line 2: "Beyond role-based, each person has a personalized AI dashboard that is tailored. Daily, Weekly, and Monthly follow different SOPs, as different questions are answered."

## 3. Timeline (above the grid)

- Label: "Cadence with Standard Operating Procedure" (13px, uppercase, letter-spacing .06em, muted). Left edge aligned to the cadence columns (margin-left 178px). Top margin of the timeline block: 27px.
- Track: a 6px-high bar with a gradient from teal (#2A9D8F) to navy (#14213D), rounded ends, and a solid arrowhead at the right end.
- Four hollow markers (16px circles, 3px border, white fill) centered over the Live, Daily, Weekly, and Monthly columns. Place each marker at the center of its column. Recalculate on load and on window resize.

## 4. Grid layout

Main grid:
- Columns: `170px 0.85fr 1fr 1fr 1fr`. The Live column is slightly narrower than the other three.
- Gap: 8px.
- Rows: a header row for the cadence cards (auto), then Live Screen, Alerts, Dashboard, and Reports.

### 4a. Cadence header cards (row 1)

Four cards, one per column: Live, Daily, Weekly, Monthly.

Each card:
- Radius 10px. Padding 10px 12px. Minimum height 100px. Padding-bottom 46px to leave room for the info button.
- Position relative. Cursor pointer. Focusable (`tabindex="0"`).
- Fills:
  - Live: coral #D9725F
  - Daily: charcoal #3A3A3A
  - Weekly: dark grey #2E2E2E
  - Monthly: near-black #111111
- Gloss overlay: `linear-gradient(180deg, rgba(255,255,255,.22) 0%, rgba(255,255,255,0) 60%)`.
- Shadow: `0 6px 14px rgba(20,33,61,.18)`.
- Hover and keyboard focus: lift 2px, shadow `0 6px 16px rgba(0,0,0,.25)`, outline 2px #111111 with 2px offset. Transition 0.15s.
- Stacking: `z-index: 1`. On hover or focus-within: `z-index: 30`.

Card contents:
- Title (h2, 17px, weight 600, white, top -1px): Live, Daily, Weekly, Monthly. No subtext.
- Review time badge, bottom-right (absolute, bottom 10px, right 10px):
  - Background: rgba(255,255,255,.2), padding 8px 14px, radius 10px.
  - Shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 2px 6px rgba(0,0,0,.15).
  - Small label "REVIEW TIME" (10px, weight 700, uppercase, letter-spacing .08em, opacity .9).
  - Value row (22px, weight 700, white): clock icon, then text. The clock icon is an 18px SVG (circle r=9 and hand `M12 7v5l3 2`), stroke 2.2, round caps, nudged up 1px.
  - Values: Live "5 sec", Daily "5 min", Weekly "1 hour", Monthly "0.5 day".
- Info button, bottom-left (absolute, left 12px, bottom 10px):
  - 18px round button, no border, background #9DBBE0, white glyph, shadow `0 1px 3px rgba(0,0,0,.12)`, cursor pointer.
  - Glyph: 14px SVG with no outer circle. A vertical bar `M12 10.5v7.5` and a dot `circle cx=12 cy=6.6 r=1.5`, both white, stroke 2.6.
  - Hover and focus: background #174E96, 2px white outline with 2px offset.
  - `aria-label="Show details"`.
- Hover popup (appears on card hover, card focus, or focus within):
  - Absolute, top calc(100% + 10px), left 0, width 290px, z-index 20.
  - White background, #111111 text, 1px #D0D0D0 border, radius 8px, shadow `0 10px 24px rgba(0,0,0,.18)`, padding 12px 14px, 13px font, line-height 1.45.
  - Text comes from `POPUP_TEXT` (see section 9).

### 4b. Row labels (left column)

Four labels: Live Screen, Alerts, Dashboard, Reports. Use these exact names. Do not add "AI" to the names.
- Fill: `linear-gradient(180deg, #FFFFFF 0%, #E9EEF5 100%)`. Radius 10px. Padding 10px 12px. Shadow `0 2px 6px rgba(20,33,61,.08)`. Text 15px, weight 600, #111111.
- Each label has a 30×30 icon, 10px to the left of the text:
  - Live Screen: blue monitor (#2F6FB0) with a coral pulse line.
  - Alerts: amber bell (#E0A526) with a red badge.
  - Dashboard: teal gauge (#2A9D8F) with a navy needle and a purple sparkle (#7A4E9C).
  - Reports: purple document (#7A4E9C) with a folded corner and white bars.
- Each label has an info button at the right edge, on the same row as the name: 19px round, soft blue #9DBBE0, white "i" glyph 14px. The Dashboard label has no subtext. Its info button sits at the top right, clear of the title.
- Each info button opens its panel (section 6). Live Screen, Alerts, Dashboard, and Reports each have one.

### 4c. Live Screen and Alerts rows

- Live cell (column 2): one tag "NOC + Help Desk" inside the cell.
- Alerts cell (column 2): one tag "NOC + Help Desk".
- Tag style: light blue #9CC8EE, dark text #0B2545, 12.5px, padding 5px 9px, radius 8px, shadow `0 3px 8px rgba(20,33,61,.22)`, white-space nowrap. A person icon on the left (13px, currentColor). Each tag has an info button (section 4f).
- Columns Daily, Weekly, Monthly in these two rows: empty dashed cells (`#FAFAFA` background, 1px dashed #D0D0D0 border, min-height 44px, radius 10px).

### 4d. Dashboard panel

One bordered panel spanning columns 2 to 5 (`grid-column: 2 / 6`). Radius 10px. Background gradient `linear-gradient(180deg, #FFFFFF 0%, #F5F8FC 100%)`. Shadow `0 8px 20px rgba(20,33,61,.10), inset 0 0 0 1px #D0D0D0`. Padding 8px.

Inside, a 4-column grid: column 1 is 0.85fr, columns 2–4 are 1fr. Rows are 44px tall, gap 10px 8px. Each bar has a person icon on the left (except where noted), radius 8px, and centered text.

Bars, top to bottom, with grid positions:

1. **NOC + Help Desk** (row 1, columns 2 only). Fill #9CC8EE, dark text. Carries the Dashboard icon link (4e) and an info button. Its info popup text comes from `noc.dashboard`.
2. **L2 Team (Platform, Storage, Network, Kubernetes, AI, QA)** (row 2, columns 2–4). Fill #2F6FB0, white text.
3. **Security + Compliance Team** (row 3, columns 2–4). Fill #2D6BAA, white text.
4. **Capacity + FinOps Team** (row 4, columns 3–4). Fill #2960A0, white text.
5. **L3 Team (Engineering)** (row 5, columns 3–4). Fill #22518A, white text.
6. **Backup + DR Team** (row 6, columns 3–4). Fill #1C4478, white text.
7. **IT Leaders** (row 7, column 4). Fill #13325E with gloss, white text. The IT Leaders style is identical in every place it appears.

Each bar: shadow `0 3px 8px rgba(20,33,61,.22)`. Gloss overlay `linear-gradient(180deg, rgba(255,255,255,.28) 0%, rgba(255,255,255,0) 70%)`.

Each team bar has an info button at the right edge (18px, soft blue, section 4f). Its popup text comes from `POPUP_TEXT`. Team bars have hover popups that show only when the mouse is over the info button. Hovering the bar itself does not open the popup.

### 4e. Dashboard link icon (NOC + Help Desk bar in the Dashboard panel)

- A 24px circle at the left of the NOC + Help Desk bar, left 28px, vertically centered.
- Fill: multicolor gradient `linear-gradient(135deg, #FFB347 0%, #F26B8A 35%, #7C5CFF 65%, #3FD0C9 100%)`, with a white 1px border and a glow: `0 0 6px 1px rgba(255,179,71,.85), 0 0 14px 3px rgba(63,208,201,.6), 0 0 22px 6px rgba(124,92,255,.35)`.
- Glyph: a white gauge (arc and needle, 14px, stroke 2.2).
- It links to https://e1-rahabok.github.io/VMW-Executive-Dashboard/design/export/ and opens in a new tab (`target="_blank" rel="noopener"`), with `aria-label="Open executive dashboard"`.
- Hover or focus shows a small popup: "Try a sample dashboard" (from `dash.sample`). This popup is separate from the info popup. The two popups never show together.
- The bar's info button shows only the info popup. Hovering the icon does not show it.

### 4f. Info buttons and tag popups

- Every tag with an info button has its popup show only while the info button is hovered or focused. Hovering the tag body does not show it.
- Popup: white, #111111 text, 1px #D0D0D0 border, radius 8px, 13px, line-height 1.45, width 300px, shadow `0 10px 24px rgba(0,0,0,.18)`.
- Escalation note info button (in the empty dashboard column): 20px, soft blue, popup to its right.

### 4g. Reports row

- Live cell (column 2): empty dashed cell.
- Daily cell (column 3): empty dashed cell.
- Weekly and Monthly (columns 4–5 of the outer grid, one cell spanning both): a bordered cell with one bar "IT Leaders" in #13325E with gloss, white text, and an info button.

Cell style: 1px #D0D0D0 border, radius 10px, shadow `0 2px 6px rgba(20,33,61,.06)`.

## 5. Escalation arrows

Draw these as an overlay SVG (position absolute, pointer-events none, full page size). Compute positions at render time from the bounding boxes of the elements. Redraw on window resize.

Two dashed red arrows, both starting from the Alerts "NOC + Help Desk" tag:
- Arrow A: goes down from the tag's bottom center, bends with a rounded corner, then runs right into the L2 Team bar's left edge.
- Arrow B: same route, but ends at the Security + Compliance Team bar's left edge.
- Stroke #E8786B, 3px, dash `9 8`, round joins and caps, opacity 0.9. The dashes flow from source to target: an animation of 1.6s linear infinite. Turn the animation off under `prefers-reduced-motion`.
- Arrowhead: a filled triangle at the end point.

Only these two arrows. Do not draw arrows from L2 to L3.

## 6. Supporting panels (below the slide)

Each row info button opens a full-width panel below the slide, in normal page flow. Panels are hidden until their button is clicked. A click on a row button toggles its own panel. Escape closes all panels. Each button has `aria-expanded` and `aria-controls`.

Panel style: white background, 1px #D0D0D0 border, radius 8px, shadow `0 10px 24px rgba(0,0,0,.12)`, padding 14px 18px, 13px text, line-height 1.45. Each panel has a title (16px, weight 600), an optional intro (#444444), and rows. A row is a two-column grid: the label (170px, weight 600) and the paragraphs (1fr).

Panels:
- **Alerts, titled "Why 3 colors?"**: a decision flow image, a color legend image, and a table. The flow and legend are supplied as images and are embedded as data URIs. Do not redraw them. The table rows are Yellow, Orange, and Red, each with a color swatch and text from `POPUP_TEXT` (`alert.guide`).
- **Live Screen, titled "Best practice for a NOC screen"**: rows for 0 interaction, Large number, Now, Color, and 5 second (text from `live.bestpractice`).
- **Dashboard, titled "Design Best Practices"**: rows for Who, What, How, When, and Why (text from `dash.design`).
- **Reports, titled "Where a report beats a dashboard"**: an intro line and rows for Offline, No access, Casual user, Export, Legal requirement, Printed document, Historical copies, and Attachment (text from `reports.edge`).

The panel text comes from `POPUP_TEXT`. Panel content is plain text (no HTML). Build the rows in script with `textContent`.

## 7. Footer

- Font 11px, muted, top margin 10px. Two lines:
  - "Source: Private Cloud Management, 5th edition. Empty cells mean no defined use case at that cadence." The words "Private Cloud Management, 5th edition" link to https://isvara.io and open in a new tab.
  - "Note: Ad hoc tasks are not shown. Longer cadences, such as quarterly, are not shown."

## 8. Technical details section (below the footer)

- A section with a top border (2px #D0D0D0), margin-top 28px, padding-top 16px.
- Heading: "Technical details" (18px, weight 600, #14213D). Subtitle (13px, muted): "Further technical diagrams and infographics. Click a diagram to view it full size."
- Grid: 3 columns, gap 10px. Items are in reading order.
- Diagram cards (first three items). Each card:
  - A button, white background, 1px #D0D0D0 border, radius 8px, padding 8px, left-aligned text.
  - Title above the image (14px, weight 600, #14213D). No subtext below.
  - A thumbnail area 150px tall, light grey background, the image with `object-fit: contain`.
  - Hover: border #1F6FD1 and a stronger shadow. Focus: 2px outline.
  - Click opens a native `<dialog>` with the full-size image, a Close button, and close on backdrop click or Escape.
  - Images are embedded as data URIs so the file stays self-contained.
- Placeholder items: dashed border, #FAFAFA background, 110px minimum height, grey centered label "Placeholder N". Replace them as the diagrams are supplied.
- The current diagrams are: (1) Private Cloud: Consumer and Provider, (2) Business, Operations and Architecture, (3) Daily and Weekly Cadence. About 10 diagrams are planned.

## 9. Popup and panel text: one editable block

All popup and panel text lives in one `<script>` block at the top of the `<body>`, in an object named `POPUP_TEXT`. Each entry has a key. Every element with `data-pop="<key>"` reads its text from that key on load.

- A string value fills a popup with plain text.
- An object value `{ title, intro, rows }` builds a panel. Each row is `{ label, color?, text: [paragraphs] }`, or an array `[label, paragraph, ...]`.
- Keys in use: `cadence.live`, `cadence.daily`, `cadence.weekly`, `cadence.monthly`, `noc.live`, `noc.dashboard`, `escalation.note`, `team.l2`, `team.capacity`, `team.l3`, `team.security`, `team.dr`, `team.it.dashboard`, `team.it.reports`, `dash.sample`, `alert.guide`, `live.bestpractice`, `dash.design`, `reports.edge`.
- The block has a comment that says: edit the text after the key, keep the key names, plain text only, no HTML tags.
- Text is written in plain, functional language. Avoid marketing words.

## 10. Accessibility and interaction

- Cadence cards are focusable. Info buttons are real `<button>` elements with `aria-label`.
- Popups use `:hover`, `:focus-within`, and `:focus-visible`. Panels use a click toggle with `aria-expanded`.
- Keep a visible focus outline on all interactive elements.
- Respect `prefers-reduced-motion`.

## 11. Output checklist

1. One file: `media/cadence-map.html`, with images embedded as data URIs and no external assets.
2. Render `media/cadence-map.png` (1280×760) with headless Chrome. The PNG shows the static layout. Hover popups, panels, and arrows may not appear in the static image.
3. Check that no "AI" prefix appears on the row labels, and that the Dashboard label has no subtext.
4. Check that every info button is 18px to 20px and uses the soft blue fill.
5. Check that the team bars have no hover popups on the bar body.
6. Check that every popup and panel text comes from `POPUP_TEXT`.
7. Check that the Technical details cards show the title above the image and no subtext.
