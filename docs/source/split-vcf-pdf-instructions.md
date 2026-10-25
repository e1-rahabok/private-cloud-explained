# Instructions: split the VCF 9.1 PDF into section PDFs

These instructions are for Claude Code running on a laptop where this repository is cloned. The goal is to split `docs/source/vmware-cloud-foundation-9-1.pdf` into one PDF per top-level heading (bookmark), starting at Release Notes (page 76), and save the results in `docs/source/vmware-cloud-foundation-9-1-sections/`. The output is input for an AI LLM, not for people to read.

The sections are numbered from 01 and run in document order: Release Notes, Overview, Design, Planning and Preparation, and so on. The cover, Contents (pages 1-75), Documentation Legal Notice and Index are not included. The Index bookmark has no destination page, so the script skips it.

## Why the script prunes resources

The source PDF has one shared resource list that names all 2,845 images (plus about 9,000 patterns and shadings) for every page. A plain page copy carries all of them into every output file, so each file comes out at 100 MB or more even for a one-page section. The script gives each page its own resource list, keeping only the images, patterns and shadings that the page's content stream uses. The result is about 158 MB across 25 files, with the largest at about 37 MB.

## Steps

1. **Check the environment.** Confirm `docs/source/vmware-cloud-foundation-9-1.pdf` exists and that `python` is available.

2. **Install the PDF libraries.** Run `python -m pip install pypdf pikepdf`. If that fails, stop and report the exact error. Do not work around network or package-policy blocks.

3. **Create the script.** Save the script below as `docs/source/split_vcf_pdf.py`.

4. **Run the split.** From the repository root, run:

   ```
   python docs/source/split_vcf_pdf.py docs/source/vmware-cloud-foundation-9-1.pdf docs/source/vmware-cloud-foundation-9-1-sections
   ```

   The script prints one line per output file with its page range.

5. **Verify the result.**
   - The first file is `01 - Release Notes.pdf`, covering pages 76-713.
   - Page ranges are contiguous, with no gaps or overlaps, and end at page 9089 (Advanced Services), just before the Legal Notice.
   - If the script reports "No top-level bookmarks found" or "Bookmark 'Release Notes' not found", stop and report it. Do not split by guessing page numbers.
   - Spot check one large section (for example Design): text extracts correctly and it still contains images.

6. **Check file sizes before committing.** GitHub rejects any single file over 100 MB. List the sizes of the files in `docs/source/vmware-cloud-foundation-9-1-sections/`, for example with `Get-ChildItem` in PowerShell or `ls -lh` in Git Bash. If any section file is over 95 MB, stop and report it. Do not commit the source PDF, which is in `.gitignore`.

7. **Commit the output.** Commit the new section folder and `split_vcf_pdf.py` together, with the message `Split VCF 9.1 PDF into section PDFs`. Do not push unless the user asks.

Report the number of files, their names, and the page counts. Report anything that failed.

## Script: `docs/source/split_vcf_pdf.py`

```python
"""Split the VCF 9.1 PDF into one PDF per top-level bookmark (heading).

Front matter before the first section (cover, contents) and the legal notice
are skipped. Each output is written with pikepdf, which keeps only the objects
(images, fonts) that the section's own pages use, so files stay small.

Requires: pip install pypdf pikepdf
Usage:    python split_vcf_pdf.py <input.pdf> <output_dir>
"""

import re
import sys
from pathlib import Path

import pikepdf
from pypdf import PdfReader

FIRST_SECTION = "Release Notes"
SKIP_TITLES = {"Documentation Legal Notice", "Index"}


def safe_name(title: str) -> str:
    # Replace characters Windows forbids in file names, and collapse whitespace.
    name = re.sub(r'[<>:"/\\|?*]', "-", title)
    name = re.sub(r"\s+", " ", name).strip().rstrip(".")
    return name or "untitled"


# Resource category -> content stream operators that name an entry in it.
PRUNED_RESOURCES = {
    "/XObject": {"Do"},
    "/Pattern": {"scn", "SCN"},
    "/Shading": {"sh"},
}


def prune_resources(page: pikepdf.Page) -> None:
    # Every page shares one resource dictionary listing every image, pattern and
    # shading in the book. Give the page its own dictionary holding only the
    # entries its content stream uses.
    resources = page.obj.get("/Resources")
    if resources is None:
        return
    used = {category: set() for category in PRUNED_RESOURCES}
    for operands, operator in pikepdf.parse_content_stream(page.obj):
        for category, operators in PRUNED_RESOURCES.items():
            if str(operator) in operators and operands:
                name = operands[-1]
                if isinstance(name, pikepdf.Name):
                    used[category].add(str(name))
    pruned = pikepdf.Dictionary({k: v for k, v in resources.items()})
    for category, names in used.items():
        if category in resources:
            pruned[category] = pikepdf.Dictionary(
                {k: v for k, v in resources[category].items() if k in names}
            )
    page.obj["/Resources"] = pruned


def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)

    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    reader = PdfReader(str(src))
    total = len(reader.pages)

    # Top-level bookmarks only (depth 0), in document order.
    top = []
    for item in reader.outline:
        if isinstance(item, list):
            continue
        page = reader.get_destination_page_number(item)
        if page is None:
            print(f"Skipping '{item.title}': bookmark has no destination page")
            continue
        top.append((page, item.title))
    top.sort(key=lambda entry: entry[0])

    if not top:
        sys.exit("No top-level bookmarks found in the PDF.")

    titles = [title for _, title in top]
    if FIRST_SECTION not in titles:
        sys.exit(f"Bookmark '{FIRST_SECTION}' not found.")
    top = top[titles.index(FIRST_SECTION):]

    number = 0
    with pikepdf.open(src) as pdf:
        for index, (start, title) in enumerate(top):
            end = top[index + 1][0] if index + 1 < len(top) else total
            if title in SKIP_TITLES or end <= start:
                print(f"Skipping '{title}'")
                continue

            number += 1
            section = pikepdf.new()
            for page in pdf.pages[start:end]:
                prune_resources(page)
            section.pages.extend(pdf.pages[start:end])
            target = out_dir / f"{number:02d} - {safe_name(title)}.pdf"
            section.save(target)
            print(f"{target.name}: pages {start + 1}-{end}")


if __name__ == "__main__":
    main()
```
