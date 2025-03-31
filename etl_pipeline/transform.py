import re
from pathlib import Path

def clean_text(text):
    """
    Cleans the provided text using regex by removing:
    - Lines with markdown image tags of the format ![](_page_<number>_Picture_<number>.jpeg)
    - Lines containing the artifact "Scanned with S CamScanner"
    """
    # Pattern for markdown image tags, e.g., ![](_page_0_Picture_17.jpeg)
    pattern_images = r"^\s*!\[\]\(_page_\d+_Picture_\d+\.jpeg\)\s*$"
    text = re.sub(pattern_images, '', text, flags=re.MULTILINE)

    # Pattern for lines containing "Scanned with S CamScanner"
    pattern_artifact = r"^\s*.*Scanned with S CamScanner.*\s*$"
    text = re.sub(pattern_artifact, '', text, flags=re.MULTILINE)

    # Remove extra blank lines that might be left after removals
    cleaned_text = re.sub(r'\n+', '\n', text)
    return cleaned_text


def transform_text(text, input_filename: str):
    """Transform the extracted text and save to a corresponding output file."""
    text = clean_text(text)

    # Create output filename based on input filename
    output_file = Path("output_files") / f"{Path(input_filename).stem}_transformed.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Transformed text has been saved to {output_file}")
    return text, output_file
