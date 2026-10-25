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
