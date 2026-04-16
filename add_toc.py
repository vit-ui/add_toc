import argparse
import json
import fitz
import os

# fitz: The module name for PyMuPDF, a library used to access and modify PDF structures.

def get_args():
    parser = argparse.ArgumentParser(description="Add a hierarchical Table of Contents to a PDF.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input PDF")
    parser.add_argument("-o", "--output", default=None, help="Path to the output PDF")
    parser.add_argument("-d", "--data", default="toc.json", help="Path to JSON file containing TOC data")
    args = parser.parse_args()

    # Verify that the input PDF exists
    if not os.path.exists(args.input):
        parser.error(f"The input file '{args.input}' was not found.")

    # Verify that the JSON data file exists
    if not os.path.exists(args.data):
        parser.error(f"The data file '{args.data}' was not found.")
    # Resolve absolute paths first for reliable comparison
    input_abs = os.path.abspath(args.input)
    output_abs = os.path.abspath(args.output) if args.output else None

    # Check if output is missing OR if it points to the same file as input
    if output_abs is None or input_abs == output_abs:
        base_path, ext = os.path.splitext(args.input)
        # Remove the dot before {ext} because splitext includes it
        args.output = f"{base_path}_indexed{ext}"

    return args

def main():
    args = get_args()

    # Load the TOC data from the JSON file
    try:
        with open(args.data, "r") as f:
            toc_list = json.load(f)
    except Exception as e:
        print(f"Error loading data file: {e}")
        return

    doc = fitz.open(args.input)

    # set_toc: A method that takes a list of lists [level, title, page]
    # to create the hierarchical navigation sidebar.
    doc.set_toc(toc_list)

    doc.save(args.output)
    doc.close()

if __name__ == "__main__":
    main()
