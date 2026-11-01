# Prompt Template: Build a Single-File Diagram or Slide

Use this template to make any one-page visual: a diagram, a cadence or process map, a swimlane, a dashboard panel, or a slide. Fill in the bracketed fields. Delete any section that does not apply.

---

## 0. Inputs (fill these in first)

- **Title:** [title]
- **Subtitle or purpose:** [one or two sentences that explain what the viewer should understand]
- **Canvas:** [width × height in px, e.g. 1280 × 720 for a 16:9 slide]
- **Output file:** [path, e.g. media/[name].html]
- **Rendered image:** [path, e.g. media/[name].png], size [width × height]
- **Audience:** [who reads it, and in what setting: slide, print, large screen, web]
- **Palette:** [e.g. black and light grey; or brand colors with hex codes]
- **Tone:** [e.g. corporate and clean; or bold and energetic]

## 1. Structure

Describe the grid or layout in plain terms:

- **Horizontal axis:** [what the columns represent, e.g. time cadence: Live, Daily, Weekly, Monthly]
- **Vertical axis:** [what the rows represent, e.g. screens or surfaces]
- **Column widths:** [equal, or a ratio such as 0.7fr for the first column and 1fr for the rest]
- **Row heights:** [fit to content, or fixed px values]
- **Gap between cells:** [px]

Then list each item in the layout:

| Item | Position (row, column or span) | Content | Style |
|---|---|---|---|
| [item name] | [e.g. row 2, columns 2–4] | [text and subtext] | [fill color, text color, radius] |

Use one row per item. Add notes about spanning cells and empty cells.

## 2. Visual style

- **Page background:** [color or gradient]
- **Cards and boxes:** [radius, border, shadow, gloss, padding]
- **Text:** [font family, sizes for title, subtitle, labels, body, footnote; weights; colors]
- **Empty cells:** [e.g. dashed border, faint fill, or none]
- **Accent or arrows:** [color, stroke width, arrowhead style]
- **Icons:** [which items get an icon, its size, its color, and its position]

If the palette needs graded colors, specify the steps. For example: "from lightest at the top to darkest at the bottom, in six steps, all with white or dark text chosen for at least 4.5:1 contrast."

## 3. Interaction

Choose what applies:

- **Hover:** [e.g. card lifts 2px and gains a shadow; no change for static items]
- **Popup or detail:** [what appears, where, how it is triggered, width, style]
- **Clickable cues:** [e.g. an info button, a pointer cursor, an underline]
- **Keyboard:** [focusable items, visible focus outline]
- **Static items:** [items that must not look interactive]

## 4. Overlays and connectors

If arrows, lines, or labels connect items:

- **From:** [item] **To:** [item] **Route:** [straight, or elbow with rounded corner of N px]
- **Style:** [color, stroke width, arrowhead size]
- **Recalculate:** on load and on window resize, from the bounding boxes of the items.

## 5. Text content

Write the exact text for every label and subtext. Do not paraphrase. Use the same spelling, casing, and punctuation as the source.

## 6. Footer and sources

- **Footer lines:** [exact text]
- **Source attribution:** [exact text]

## 7. Output rules

1. Produce one self-contained HTML file. No external images, fonts, or scripts unless specified.
2. Set the body to the canvas size. Use `box-sizing: border-box` and no default margins.
3. Keep all colors in one `:root` block as CSS variables so they can be changed in one place.
4. Render the file to PNG with headless Chrome at [width × height]. The PNG shows the static state only. Hover states and overlays may not appear in it.
5. Commit locally with [the identity you specify]. Do not push unless asked.
6. Before finishing, check:
   - Every label and subtext matches section 5 exactly.
   - No text overflows its box at the target size.
   - Items that should look interactive have a visible cue. Static items do not.
   - Empty cells are styled the same way.
   - Spanning cells line up with the columns they span.

## 8. Revision workflow

When the user asks for a change:

1. Make the smallest edit that satisfies the request.
2. Re-render the PNG.
3. Commit locally with a message that names the change.
4. Report the change in one or two sentences. Do not push until asked.

## Example filled-in fragment

- **Title:** Release Pipeline
- **Canvas:** 1280 × 720
- **Horizontal axis:** Commit, Build, Test, Release
- **Vertical axis:** Owner, Tool
- **Palette:** #111111, #3A3A3A, #F2F2F2, accent #2F6FB0
- **Row item:** Build (row 2, column 2): "Automated build" on fill #2F6FB0, white text, radius 8px, shadow 0 3px 8px rgba(20,33,61,.22).
