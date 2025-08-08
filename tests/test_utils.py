import os
from app.utils import allowed_file, parse_docx, parse_pdf

# Define the path to our test files directory
TEST_FILES_DIR = os.path.join(os.path.dirname(__file__), 'test_files')


def test_allowed_file():
    """
    Tests the allowed_file function to ensure it correctly
    identifies valid and invalid file extensions.
    """
    # Assert that these should be True
    assert allowed_file('resume.pdf') is True
    assert allowed_file('document.docx') is True

    # Assert that these should be False
    assert allowed_file('image.jpg') is False
    assert allowed_file('data.txt') is False
    assert allowed_file('archive.zip') is False
    assert allowed_file('nodot') is False


def test_parse_docx():
    """
    Tests if the parse_docx function can correctly extract
    text from our sample .docx file.
    """
    # Construct the full path to the sample docx file
    file_path = os.path.join(TEST_FILES_DIR, 'sample.docx')

    # 'rb' means read in binary mode, which is what the parser expects
    with open(file_path, 'rb') as file_stream:
        # Call the function with the file's stream
        result_text = parse_docx(file_stream)

    # Assert that the text we expect is in the result
    assert "Hello World DOCX" in result_text


def test_parse_pdf():
    """
    Tests if the parse_pdf function can correctly extract
    text from our sample .pdf file.
    """
    # Construct the full path to the sample pdf file
    file_path = os.path.join(TEST_FILES_DIR, 'sample.pdf')

    with open(file_path, 'rb') as file_stream:
        # Call the function with the file's stream
        result_text = parse_pdf(file_stream)

    # Assert that the text we expect is in the result
    assert "Hello World PDF" in result_text

