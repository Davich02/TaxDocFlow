import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def extract_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == '.pdf':
        page = convert_from_path(file_path)
        text = []
        for page in page:
            text.append(page.text)
        return '\n'.join(text)

    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang='eng+deu')
    return text


