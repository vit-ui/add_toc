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
