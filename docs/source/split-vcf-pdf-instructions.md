# Instructions: split the VCF 9.1 PDF into section PDFs

These instructions are for Claude Code running on a laptop where this repository is cloned. The goal is to split `docs/source/vmware-cloud-foundation-9-1.pdf` into one PDF per top-level heading (bookmark), and save the results in `docs/source/vmware-cloud-foundation-9-1-sections/`.

The expected top-level sections begin with:

1. Release Notes
2. Overview
3. Design
4. Planning and Preparation

and continue through the rest of the document.

## Steps

1. **Check the environment.** Confirm `docs/source/vmware-cloud-foundation-9-1.pdf` exists and that `python` is available.

2. **Install the PDF library.** Run `python -m pip install pypdf`. If that fails, stop and report the exact error. Do not work around network or package-policy blocks.

3. **Create the script.** Save the script below as `docs/source/split_vcf_pdf.py`.

4. **Run the split.** From the repository root, run:

   ```
   python docs/source/split_vcf_pdf.py docs/source/vmware-cloud-foundation-9-1.pdf docs/source/vmware-cloud-foundation-9-1-sections
   ```

   The script prints one line per output file with its page range.

5. **Verify the result.**
   - The number of files matches the number of top-level bookmarks, and the first file is `01 - Release Notes.pdf`.
   - Page ranges are contiguous, with no gaps or overlaps.
   - The page counts add up to the page count of the source PDF.
   - If the script reports "No top-level bookmarks found", stop and report it. Do not split by guessing page numbers.

6. **Check file sizes before committing.** GitHub rejects any single file over 100 MB. List the sizes of the files in `docs/source/vmware-cloud-foundation-9-1-sections/`, for example with `Get-ChildItem` in PowerShell or `ls -lh` in Git Bash. If any section file is over 95 MB, stop and report it. Do not commit the source PDF, which is in `.gitignore`.

7. **Commit the output.** Commit the new section folder and `split_vcf_pdf.py` together, with the message `Split VCF 9.1 PDF into section PDFs`. Do not push unless the user asks.

Report the number of files, their names, and the page counts. Report anything that failed.

## Script: `docs/source/split_vcf_pdf.py`

```python
"""Split the VCF 9.1 PDF into one PDF per top-level bookmark (heading).

Requires: pip install pypdf
Usage:    python split_vcf_pdf.py <input.pdf> <output_dir>
"""

import re
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter


def safe_name(title: str) -> str:
    # Replace characters Windows forbids in file names, and collapse whitespace.
    name = re.sub(r'[<>:"/\\|?*]', "-", title)
    name = re.sub(r"\s+", " ", name).strip().rstrip(".")
    return name or "untitled"


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
        top.append((reader.get_destination_page_number(item), item.title))
    top.sort(key=lambda entry: entry[0])

    if not top:
        sys.exit("No top-level bookmarks found in the PDF.")

    for index, (start, title) in enumerate(top):
        end = top[index + 1][0] if index + 1 < len(top) else total
        if end <= start:
            print(f"Skipping '{title}': empty page range")
            continue

        writer = PdfWriter()
        for page_number in range(start, end):
            writer.add_page(reader.pages[page_number])

        number = f"{index + 1:02d}"
        target = out_dir / f"{number} - {safe_name(title)}.pdf"
        with target.open("wb") as handle:
            writer.write(handle)
        print(f"{target.name}: pages {start + 1}-{end}")


if __name__ == "__main__":
    main()
```
