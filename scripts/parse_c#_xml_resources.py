import os
import sys
import argparse
import base64
import xml.etree.ElementTree as ET

def extract(xml_path, out_dir):
    # Parse the XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Ensure output directory exists
    os.makedirs(out_dir, exist_ok=True)

    # Iterate through all elements
    for elem in root.iter():
        name = elem.attrib.get('name')
        data = elem.text
        if not name or not data:
            continue

        # Clean up whitespace
        b64 = data.strip()

        try:
            blob = base64.b64decode(b64)
        except Exception as e:
            print(f"Skipping '{name}': not valid base64 ({e})", file=sys.stderr)
            continue

        # Determine full output path
        out_path = os.path.join(out_dir, name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        # Write binary data
        with open(out_path, 'wb') as f:
            f.write(blob)
        print(f"Wrote {out_path}")

def main():
    p = argparse.ArgumentParser(
        description="Extract base64-encoded files from an XML resource file."
    )
    p.add_argument("xml_file", help="Path to the XML file to parse")
    p.add_argument(
        "-o", "--output-dir",
        default="output",
        help="Directory where files will be written (default: ./output)"
    )
    args = p.parse_args()

    if not os.path.isfile(args.xml_file):
        print(f"Error: '{args.xml_file}' does not exist or is not a file.", file=sys.stderr)
        sys.exit(1)

    extract(args.xml_file, args.output_dir)

if __name__ == "__main__":
    main()
