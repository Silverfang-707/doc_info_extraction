import os
import torch
from docx import Document
from groq import Groq
import ocr
import shutil
import config

# Function to extract text from a Word document
def extract_text_from_docx(docx_path):
    """
    Reads a Word document and extracts all the text.

    Args:
        docx_path (str): Path to the .docx file.

    Returns:
        str: The extracted text from the document.
    """
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])

# Function to generate embeddings for text using Groq API
def generate_embeddings(text, model="mxbai-embed-large"):
    client = Groq(api_key="your_api_key_here")
    response = client.embeddings.create(model=model, input=text)
    return response["data"][0]["embedding"]

# Function to find relevant context from a vault
def get_relevant_context(prompt, vault_embeddings, vault_content, top_k=3):
    if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
        return []
    input_embedding = torch.tensor(generate_embeddings(prompt)).unsqueeze(0)
    cos_scores = torch.cosine_similarity(input_embedding, vault_embeddings)
    top_k = min(top_k, len(cos_scores))
    top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
    return [vault_content[idx].strip() for idx in top_indices]

# Function to interact with the Groq API for structured information extraction
def extract_parties_and_roles(doc_text, model):
    client = Groq(api_key=config.GROQ_API_KEY)
    prompt = f"""
    You're given the contents of a legal document written in Tamil. 
    Translate the given text from Tamil to English and extract information 
    about the names of people mentioned in the text and the roles they 
    played in the legal exchange in detail without leaving any information 
    since everything's sensitive:\n\n{doc_text}
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert at extracting structured information and translation."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Handle streaming response
    extracted_info = ""
    for chunk in completion:
        extracted_info += chunk.choices[0].delta.content or ""
    return extracted_info

# Main function to process the Word document and extract information
def main(docx_name, groq_model):
    # Get the root directory where the script is located
    root_dir = os.path.dirname(os.path.abspath(__file__))
    docx_path = os.path.join(root_dir, docx_name)

    # Extract text from the Word document
    print("Extracting text from the document...")
    doc_text = extract_text_from_docx(docx_path)

    # Extract parties and roles using the Groq model
    print("Extracting parties and roles...")
    extracted_info = extract_parties_and_roles(doc_text, groq_model)

    # Print the extracted information
    print("\nExtracted Information:")
    print(extracted_info)

if __name__ == "__main__":
    # Example usage
    pdf_name = "test.pdf"  # PDF file name in the script's directory
    docx_name = "output_text.docx"  # The document created by the OCR pipeline
    ollama_model = "llama3.2-vision"  # Ollama model to use
    indic_nlp_resources_folder = "indic_nlp_resources"  # Folder name in the script's directory
    result = ocr.ocr_doc(pdf_name, indic_nlp_resources_folder)
    print(result)
    shutil.rmtree('output_images')
    main(docx_name, ollama_model)
