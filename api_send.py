from flask import Flask, request, jsonify
import os
import tempfile
import groq_api
import shutil
import ocr
app = Flask(_name_)

@app.route('/', methods=['POST'])
def upload_pdf():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    # Check if the file has a valid name
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Check file type (ensure it’s a PDF)
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file_path = temp_file.name
        file.save(temp_file_path)
    
    pdf_name = "test.pdf"  # PDF file name in the script's directory
    docx_name = "output_text.docx"  # The document created by the OCR pipeline
    ollama_model = "llama-3.3-70b-versatile"  # Ollama model to use
    indic_nlp_resources_folder = "indic_nlp_resources"  # Folder name in the script's directory
    result = ocr.ocr_doc(pdf_name, indic_nlp_resources_folder)
    print(result)
    shutil.rmtree('output_images')
    jsonout=groq_api.groq_res(docx_name, ollama_model)

    return jsonify({
        'message': jsonout,
        'temp_file_path': temp_file_path
    }), 200

if __name__ == '__main__':
    app.run(debug=True)