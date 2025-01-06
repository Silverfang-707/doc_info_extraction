import os
import shutil
from modules import pdf2img, transcribe
import ocr
def ocr_doc(pdf_name, indic_nlp_resources_folder):
    """
    Main function to convert a PDF into images, transcribe the text from the images, 
    and save the transcribed text into a Word document.

    Args:
        pdf_name (str): Name of the input PDF file (located in the script's directory).
        indic_nlp_resources_folder (str): Name of the Indic NLP Resources folder (located in the script's directory).

    Returns:
        str: Success message or error message.
    """
    # Get the root directory where the script is located
    root_dir = os.path.dirname(os.path.abspath(__file__))

    # Define paths relative to the script's directory
    pdf_path = os.path.join(root_dir, pdf_name)
    output_folder = os.path.join(root_dir, "output_images")
    doc_path = os.path.join(root_dir, "output_text.docx")
    indic_nlp_resources_path = os.path.join(root_dir, indic_nlp_resources_folder)

    print("Converting PDF to images...")
    image_conversion_result = pdf2img.convert_pdf_to_images(pdf_path, output_folder)

    if isinstance(image_conversion_result, str):  # Check if an error occurred
        return image_conversion_result

    print("Extracting text from images and saving to Word document...")
    transcription_result = transcribe.extract_text_from_folder_to_docx(output_folder, doc_path, indic_nlp_resources_path)

    return transcription_result