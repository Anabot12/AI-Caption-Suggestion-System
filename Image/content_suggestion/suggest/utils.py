import pytesseract
from PIL import Image
import spacy

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

nlp=spacy.load("en_core_web_sm")

def Extract_text(image):
    text=pytesseract.image_to_string(Image.open(image))
    return text

def Extract_keyword(text):
    doc=nlp(text)
    keywords=[chunk.text for chunk in doc.noun_chunks if len(chunk.text)>1]
    return keywords
