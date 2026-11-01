# Prompt: Build the "Private Cloud Management" Cadence Map

Create one self-contained HTML file (`media/cadence-map.html`) that renders a 1280×720 slide showing who does what, when, and how in a VMware Private Cloud (VCF Operations) operating model. Then render it to PNG (`media/cadence-map.png`) with headless Chrome at 1280×760.

Do not push to the remote unless asked. Commit locally only.

---

## 1. Page frame

- Body: 1280×720 px, padding 40px top/bottom and 56px left/right, flex column.
- Font: "Segoe UI", Arial, Helvetica, sans-serif.
- Background: soft gradient, `linear-gradient(160deg, #FFFFFF 0%, #F3F6FB 100%)`.
- Text color: #111111. Muted text: #666666. Grid line color: #D0D0D0.
- Palette is black and grey, with blue and teal for team bars. Do not use black in the AI Dashboard area.

## 2. Header

- H1: "Private Cloud Management" (30px, weight 600, #111111, letter-spacing -0.01em).
- Subtitle (15px, muted), two sentences with a line break after the first:
  - Line 1: "Who does what when, and how. Transforming from reactive to proactive operations management."
  - Line 2: "Beyond role-based, each person has a personalized AI dashboard that is tailored. Daily, Weekly, and Monthly follow different SOPs, as different questions are answered."

## 3. Timeline (above the grid)

- Label: "Cadence with Standard Operating Procedure" (13px, uppercase, letter-spacing .06em, muted). Left edge aligned to the grid's cadence columns (margin-left 178px).
- Track: a 6px-high bar with a gradient from #6B6B6B to #111111 and rounded ends. Add a 16px-wide solid black arrowhead at the right end.
- Four hollow markers (16px circles, 3px black border, white fill) centered over the Live, Daily, Weekly, and Monthly columns. Positions: 91.5px, 321.5px, 590.5px, 859.5px from the track's left edge. Use the Live column width of 0.7fr, as set below.

## 4. Grid layout

Main grid:
- Columns: `170px 0.7fr 1fr 1fr 1fr`. The Live column is narrower than the other three.
- Gap: 8px.
- Rows: header row (auto), then Live Screen, AI Alerts, AI Dashboard, Reports.

### 4a. Cadence header cards (row 1)

Four cards, one per column: Live, Daily, Weekly, Monthly.

Each card:
- Rounded corners 10px. Padding 10px 12px. Min-height 96px. Padding-bottom 46px to leave room for the info button.
- Position: relative. Cursor: pointer. Focusable (`tabindex="0"`).
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
- Title (h2, 17px, weight 600, white): Live, Daily, Weekly, Monthly.
- Review time badge, bottom-right (absolute, bottom 10px, right 10px):
  - Background: rgba(255,255,255,.2), padding 8px 14px, radius 10px.
  - Shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 2px 6px rgba(0,0,0,.15).
  - Small label "REVIEW TIME" (10px, weight 700, uppercase, letter-spacing .08em, opacity .9).
  - Value row (22px, weight 700, white): clock icon then text. Clock icon is an 18px SVG (circle r=9 and hand `M12 7v5l3 2`), stroke 2.2, round caps, nudged up 1px (`position: relative; top: 1px`).
  - Values: Live "5 sec", Daily "5 min", Weekly "1 hour", Monthly "0.5 day".
- Info button, bottom-left (absolute, left 12px, bottom 10px):
  - 28px round button, border none, background #1F6FD1, white glyph, shadow 0 2px 6px rgba(0,0,0,.25), cursor pointer.
  - Glyph: 18px SVG with no outer circle. A vertical bar `M12 10.5v7.5` and a dot `circle cx=12 cy=6.6 r=1.5`, both white, stroke 2.6.
  - Hover and focus: background #174E96, 2px white outline with 2px offset.
  - `aria-label="Show details"`.
- Hover popup (appears on card hover, card focus, or focus within):
  - Absolute, top calc(100% + 10px), left 0, width 290px, z-index 20.
  - White background, #111111 text, 1px #D0D0D0 border, radius 8px, shadow 0 10px 24px rgba(0,0,0,.18), padding 12px 14px, 13px font, line-height 1.45.
  - Text:
    - Live: "Streaming, auto-updating on the big TV screen with auto-rotation"
    - Daily: "Quick, 5 min review at start of day. Focus on the day ahead only. Time consuming check is not operationally practical."
    - Weekly: "1 hour deeper dive at start of week. Plan ahead for the week. Insight analysis."
    - Monthly: "Big team review. Half a day at start of month. Review past month, plan ahead."

### 4b. Row labels (left column)

Four labels: Live Screen, AI Alerts, AI Dashboard, Reports.
- Fill: `linear-gradient(180deg, #FFFFFF 0%, #E9EEF5 100%)`. Radius 10px. Padding 10px 12px. Shadow 0 2px 6px rgba(20,33,61,.08). Text 15px, weight 600, #111111.
- Each has a 20px icon, 10px to the left of the text:
  - Live Screen: blue monitor (#2F6FB0), a rectangle with a small stand.
  - AI Alerts: amber warning triangle (#E0A526) with a white "!".
  - AI Dashboard: teal bar chart (#2A9D8F), three bars.
  - Reports: purple document (#7A4E9C) with a folded corner.
- AI Dashboard label: the title sits on top, with a subtext underneath (11px, weight 400, muted): "Personalized to each person, not just role. Covers both Alert + Insight."

### 4c. Live Screen and AI Alerts rows

- Live cell (column 2): one tag "NOC + Help Desk" inside the cell.
- AI Alerts cell (column 2): one tag "NOC + Help Desk".
- Tag style: light blue #9CC8EE, dark text #0B2545, 12.5px, padding 5px 9px, radius 8px, shadow 0 3px 8px rgba(20,33,61,.22), white-space nowrap. Add a person icon on the left (13px, currentColor).
- Columns Daily, Weekly, Monthly in these two rows: empty dashed cells (`#FAFAFA` background, 1px dashed #D0D0D0 border, min-height 44px, radius 10px).

### 4d. AI Dashboard panel

One bordered panel spanning columns 2 to 5 (`grid-column: 2 / 6`). Radius 10px. Background gradient `linear-gradient(180deg, #FFFFFF 0%, #F5F8FC 100%)`. Shadow `0 8px 20px rgba(20,33,61,.10), inset 0 0 0 1px #D0D0D0`. Padding 8px 0.

Inside, a 4-column grid where column 1 is 0.7fr and columns 2–4 are 1fr. Row heights fit the content. Each bar has 8px left and right margin, radius 8px, a person icon on the left, and text centered.

Bars in order (top to bottom), with grid positions:

1. **NOC + Help Desk** (row 1, column 2 only). Subtext: "Shift Handover dashboard". Fill #9CC8EE, dark text.
2. **L2 Team (Platform, Storage, Network, Kubernetes, AI, QA)** (row 2, columns 2–4). Subtext: "Proactive performance analysis using both insight + alert. Reclamation and rightsizing." Fill #2F6FB0, white text.
3. **Security + Compliance Team** (row 3, columns 2–4). Fill #2D6BAA, white text. No subtext.
4. **Capacity + FinOps Team** (row 4, columns 3–4). Subtext: "Capacity Planning and cost optimization". Fill #2960A0.
5. **L3 Team (Engineering)** (row 5, columns 3–4). Subtext: "System architecture, vendor escalation, deep troubleshooting". Fill #22518A.
6. **Backup + DR Team** (row 6, columns 3–4). Fill #1C4478, white text.
7. **IT Leaders** (row 7, column 4). Fill #13325E, white text.

Each bar: subtext in 11px at opacity .9. Shadow `0 3px 8px rgba(20,33,61,.22)`. Gloss overlay `linear-gradient(180deg, rgba(255,255,255,.28) 0%, rgba(255,255,255,0) 70%)`.

Team bars do not have hover popups. Keep them static.

### 4e. Reports row

- Live cell (column 2): empty dashed cell.
- Daily cell (column 3): empty dashed cell.
- Weekly and Monthly (columns 4–5 of the outer grid, one cell spanning both): a bordered cell with one bar "IT Leaders" in #13325E, white text, with the person icon.

Cell style: 1px #D0D0D0 border, radius 10px, shadow 0 2px 6px rgba(20,33,61,.06).

## 5. Escalation arrows

Draw these as an overlay SVG (position absolute, pointer-events none, full page size). Compute the positions at render time from the bounding boxes of the elements, and redraw on window resize.

Two thin red arrows, both starting from the AI Alerts "NOC + Help Desk" tag:
- Arrow A: goes down from the tag's bottom center, bends with a 14px rounded corner, then runs right into the L2 Team bar's left edge.
- Arrow B: same route, but ends at the Security + Compliance Team bar's left edge.
- Stroke #E8382B, 1.5px, round joins and caps. Arrowhead: a 9×10 px filled triangle at the end point.

Only these two arrows. Do not draw arrows from L2 to L3.

## 6. Footer

Font 11px, muted, top margin 10px. Two lines:
- "Source: Private Cloud Management, 5th edition. Empty cells mean no defined use case at that cadence."
- "Note: Ad hoc tasks are not shown. Longer cadences, such as quarterly, are not shown."

## 7. Accessibility and interaction

- Cadence cards are focusable and open the popup on focus. Info buttons are real `<button>` elements with aria-labels.
- Use `:hover`, `:focus-within`, and `:focus-visible` for the popup and lift effect.
- Keep the outline visible on keyboard focus.

## 8. Output checklist

1. One file: `media/cadence-map.html`, no external assets.
2. Render `media/cadence-map.png` (1280×760) with headless Chrome. The PNG shows the static layout. Hover popups and arrows may not appear in the static image.
3. Commit locally with an identity you are told to use. Do not push unless asked.
4. Before finishing, confirm: no leftover "Details" text, "Half a day" appears only in the subtitle or footer, not as a badge, and every card's badge reads 5 sec, 5 min, 1 hour, 0.5 day.
