import os
import docx
import pdfplumber
from werkzeug.utils import secure_filename

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'docx'}


def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def parse_docx(file_stream):
    """
    Parses the content of a .docx file.
    Args:
        file_stream: The file stream object from the uploaded file.
    Returns:
        A string containing the text from the .docx file.
    """
    try:
        doc = docx.Document(file_stream)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return '\n'.join(full_text)
    except Exception as e:
        # In a real app, you'd want to log this error.
        print(f"Error parsing DOCX file: {e}")
        return ""


def parse_pdf(file_stream):
    """
    Parses the content of a .pdf file.
    Args:
        file_stream: The file stream object from the uploaded file.
    Returns:
        A string containing the text from the .pdf file.
    """
    text = ""
    try:
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Error parsing PDF file: {e}")
        return ""


def get_text_from_file(file):
    """
    Master function to extract text from an uploaded file.
    It checks the file extension and calls the appropriate parser.
    Args:
        file: The file object from the Flask request.
    Returns:
        A string of the extracted text or None if the file type is not allowed.
    """
    filename = secure_filename(file.filename)

    if not allowed_file(filename):
        return None

    # Get the file extension
    ext = filename.rsplit('.', 1)[1].lower()

    # file.stream gives us a file-like object that our parsers can read
    file_stream = file.stream

    if ext == 'docx':
        return parse_docx(file_stream)
    elif ext == 'pdf':
        return parse_pdf(file_stream)

    return None

