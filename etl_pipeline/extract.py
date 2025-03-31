from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from pathlib import Path


def split_pdf_pages():
    pass


def extract_text(pdf_path: str):
    """Extract text from a PDF file and save it to a corresponding output file."""
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )
    rendered = converter(pdf_path)
    text = text_from_rendered(rendered)[0]

    # Create output filename based on input filename
    input_path = Path(pdf_path)
    output_file = Path("output_files") / f"{input_path.stem}_extracted.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # for debugging purpose
    # with open(output_file, "w", encoding="utf-8") as f:
    #     f.write(text)

    print(f"Extracted text has been saved to {output_file}")
    return text, output_file
