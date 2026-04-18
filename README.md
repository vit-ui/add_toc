# PDF Hierarchical Indexer

This tool automates the creation of a functional, clickable, and nested Table of
Contents (TOC) for PDF files. It is used to add a navigation sidebar (outline)
to documents that lack internal indexing.

## Quick Start

### 1. Install Dependencies

This tool requires the PyMuPDF library.

```bash
pip install pymupdf
```

### 2. Run the Script

Basic usage with the default `toc.json` data file:

```bash
python3 add_toc.py -i "your_document.pdf"
```

## How It Works

The script uses the `fitz` library to inject hierarchical metadata into the PDF
structure.

To prevent file corruption, the script ensures the input file is never
overwritten while it is being read. If the user does not specify an output path,
or if the specified output matches the input, the script automatically generates
a filename following the pattern `[input_filename]_indexed.pdf`.

## Command Line Arguments

| Argument | Long Flag | Description                                                                  |
| :------- | :-------- | :--------------------------------------------------------------------------- |
| -i       | --input   | Required. Path to the source PDF file.                                       |
| -d       | --data    | Optional. Path to the JSON file containing TOC data. Defaults to `toc.json`. |
| -o       | --output  | Optional. Custom output path. Defaults to `[input_filename]_indexed.pdf`.    |

## Data Format (JSON)

The TOC data must be a JSON array of arrays. Each inner array represents a
bookmark in the format: `[Level, "Title", PageNumber]`.

Example `toc.json`:

```json
[
    [1, "Chapter 1: The Basics", 10],
    [2, "1.1 Starting Hands", 12],
    [3, "High Pair Strategy", 15],
    [1, "Chapter 2: Advanced Play", 45]
]
```

> Note: The `PageNumber` refers to the absolute physical index of the page within
the PDF file (where the first page is 1). This index may differ from the page
numbers printed on the corners of the book if the document contains front matter
or unnumbered pages.

## Generating toc.json with AI

If the book does not already have a `toc.json`, you can generate one using an AI
assistant (e.g. Claude) with computer use / code execution access. Paste the
prompt below at the start of a new chat, then attach the PDF.

<details>
<summary>Expand prompt</summary>

```markdown
I need you to build a complete toc.json for the attached PDF book. This file
will be used to inject a clickable navigation sidebar into the PDF using
PyMuPDF's set_toc().

---

Output format

A JSON array of arrays. Each inner array is [level, "Title", pdf_page]:
- level: hierarchy depth — 1 for top-level chapters, 2 for subchapters, 3 for sub-subchapters
- "Title": exact title as it appears in the book
- pdf_page: the absolute physical PDF page number (first page of the file = 1),
  NOT the printed page number on the corner of the page

One entry per line. Example:
[
    [1, "Chapter 1: The Basics", 12],
    [2, "Starting Hands", 14],
    [3, "High Pairs", 17],
    [1, "Chapter 2: Advanced Play", 45]
]

---

How to build it

Step 1 — Find the book's own Table of Contents

Rasterize the first ~20 pages at 150 DPI with pdftoppm and visually read them.
Most books have a printed TOC listing all chapters and subchapters with their
printed page numbers. If the book has per-section TOCs (each chapter starts with
its own contents list), read those too — they are the most complete source of
subchapter titles.

If no TOC exists anywhere in the book, fall back to scanning for headings page
by page.

Step 2 — Establish the offset

The printed page number on the corner of a page is NOT the PDF page number.
There is usually an offset (front matter: cover, dedication, foreword, etc. are
often unnumbered or roman-numbered).

To find the offset, rasterize a known page (e.g. the first page that shows a
printed "1") and note its PDF page number. Then:

    pdf_page = printed_page + offset

Step 3 — Watch for offset drift

The offset is NOT always constant throughout the book. Full-page photos,
illustrations, or other unnumbered inserts shift it. Every time you enter a new
major section, verify the offset by rasterizing the first numbered page of that
section and reading its header. Do not assume the offset from one section applies
to the next.

In practice: rasterize the page you expect a chapter to start on, read the
printed number in the corner, and correct if wrong before moving on.

Step 4 — Verify, do not estimate

For every entry in the TOC, verify the PDF page number by actually rasterizing
that page and confirming the printed page number matches. Do not guess or
extrapolate. If a section TOC says a subchapter starts on printed page 82,
rasterize the expected PDF page and confirm the header reads 82 before writing
the entry.

Step 5 — Cover all levels

Include every level the book's TOC lists: parts, chapters, subchapters,
sub-subchapters. Do not flatten the hierarchy. Do not skip entries.

---

Tools to use

    # Get page count and metadata
    pdfinfo book.pdf

    # Rasterize a specific page range to check content
    pdftoppm -jpeg -r 150 -f 5 -l 10 book.pdf /tmp/page

    # Then view /tmp/page-005.jpg, /tmp/page-006.jpg, etc.

Install PyMuPDF if needed: pip install pymupdf --break-system-packages

---

Important rules

- Never use printed page numbers directly as PDF page numbers — always convert
  through the verified offset
- Always re-verify the offset when entering a new section
- If a page is a full-page illustration with no number, it still counts as a PDF
  page and shifts the offset for everything after it
- All entries must be on one line each in the final JSON
- Do not stop at top-level chapters — every subchapter and sub-subchapter listed
  anywhere in the book's TOC must be included
- When done, validate the JSON (parse it) and confirm no entry has a page number
  out of bounds (> total PDF pages)
```

</details>
