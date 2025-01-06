import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path, output_folder, dpi=300):
    """
    Convert a PDF file into images, saving each page as an image in the specified folder.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_folder (str): Path to the folder where images will be saved.
        dpi (int, optional): Resolution of the output images. Defaults to 300.

    Returns:
        list: List of file paths to the saved images.
    """
    try:
        # Convert PDF to images
        images = convert_from_path(pdf_path, dpi=dpi)

        # Ensure the output folder exists
        os.makedirs(output_folder, exist_ok=True)

        image_paths = []
        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{i + 1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)

        return image_paths

    except Exception as e:
        return f"An error occurred while converting PDF to images: {e}"