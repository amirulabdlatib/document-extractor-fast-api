from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from pathlib import Path
import fitz

def split_pdf_pages(pdf_path: str):
    """
    Splits the input PDF into individual pages.
    Each page is saved as a separate PDF file in the 'split_files' directory.

    Returns:
        A list of Path objects for each split PDF file.
    """
    doc = fitz.open(pdf_path)
    split_files = []
    split_dir = Path("split_files")
    split_dir.mkdir(parents=True, exist_ok=True)
    
    for page_number in range(doc.page_count):
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_number, to_page=page_number)
        
        split_file = split_dir / f"{Path(pdf_path).stem}_page_{page_number + 1}.pdf"
        new_doc.save(str(split_file))
        new_doc.close()
        split_files.append(split_file)
    
    doc.close()
    return split_files

def extract_text(pdf_path: str):
    """
    Extracts text from each page of a PDF file by first splitting it into individual pages.
    Each split page is processed separately to generate its own output text file.
    
    Returns:
        A list of paths to the individual extracted text files.
    """

    splitted_pages = split_pdf_pages(pdf_path)
    
    converter = PdfConverter(
        artifact_dict=create_model_dict(),
    )
    
    output_files = []
    
    for splitted_file in splitted_pages:
        rendered = converter(str(splitted_file))
        page_text = text_from_rendered(rendered)[0]
        
        output_file = Path("output_files") / f"{splitted_file.stem}_extracted.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(page_text)
        
        print(f"Extracted text for {splitted_file} has been saved to {output_file}")
        output_files.append(output_file)
    
    return output_files
