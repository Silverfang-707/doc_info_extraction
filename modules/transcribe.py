import os
from ocr_tamil.ocr import OCR
from docx import Document
from indicnlp.tokenize import sentence_tokenize
from indicnlp import common

def extract_text_from_folder_to_docx(folder_path, doc_path, indic_nlp_resources_path):
    """
    Extract text from all images in a folder using OCR, tokenize it into sentences, 
    and save it to a Word document.

    Args:
        folder_path (str): Path to the folder containing image files.
        doc_path (str): Path to save the Word document.
        indic_nlp_resources_path (str): Path to the Indic NLP Resources folder.

    Returns:
        str: Success message or error message.
    """
    # Set the path to the Indic NLP Resources folder
    common.set_resources_path(indic_nlp_resources_path)

    # Initialize OCR with text detection enabled
    ocr = OCR(detect=True)

    try:
        # Create a new Word document
        doc = Document()

        # Iterate through all files in the folder
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # Check if the file is an image
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                # Perform OCR on the image
                text_list = ocr.predict(file_path)

                # Flatten the text list if it contains sublists
                flattened_text_list = [word for sublist in text_list for word in sublist]

                # Combine the list items into a single string
                full_text = ' '.join(flattened_text_list)

                # Tokenize the text into sentences using indic-nlp-library
                sentences = sentence_tokenize.sentence_split(full_text, lang='tam')

                # Add the processed text to the document
                for sentence in sentences:
                    doc.add_paragraph(sentence)

        # Save the document
        doc.save(doc_path)

        return f"Extracted text from all images in {folder_path} has been written to {doc_path}"

    except PermissionError:
        return f"Permission denied: Unable to save the document to {doc_path}. Please ensure the file is closed and you have write permissions."

    except Exception as e:
        return f"An error occurred: {e}"