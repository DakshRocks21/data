import os
import sys
import argparse
import base64
import binascii
import xml.etree.ElementTree as ET

try:
    import filetype
except ImportError:
    filetype = None

def extract(xml_path, out_dir):
    # Parse the XML
    tree = ET.parse(xml_path)
    root = tree.getroot()

    os.makedirs(out_dir, exist_ok=True)

    for data_elem in root.findall('.//data'):
        name = data_elem.get('name')
        value_elem = data_elem.find('value')
        if not name or value_elem is None or not value_elem.text:
            continue

        b64 = value_elem.text.strip()
        try:
            blob = base64.b64decode(b64)
        except Exception as e:
            blob = b64
            continue

        ext = ''
        if filetype:
            kind = filetype.guess(blob)
            if kind and kind.extension:
                ext = '.' + kind.extension
        if not ext:
            ext = '.bin'

        base = os.path.splitext(name)[0]
        final_name = base + ext
        out_path = os.path.join(out_dir, final_name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, 'wb') as f:
            f.write(blob)
        print(f"Wrote {out_path}")
def main():
    p = argparse.ArgumentParser(
        description="Extract files from an XML resource file"
    )
    p.add_argument("xml_file", help="Path to the XML or .resx file")
    p.add_argument(
        "-o", "--output-dir",
        default="output",
        help="Where to write decoded files (default: ./output)"
    )
    args = p.parse_args()

    if not os.path.isfile(args.xml_file):
        print(f"Error: '{args.xml_file}' not found.", file=sys.stderr)
        sys.exit(1)

    extract(args.xml_file, args.output_dir)

if __name__ == "__main__":
    main()
