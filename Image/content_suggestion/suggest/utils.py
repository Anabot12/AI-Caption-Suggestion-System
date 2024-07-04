import pytesseract
from PIL import Image
import spacy
from transformers import pipeline
import fitz

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

nlp=spacy.load("en_core_web_sm")

text_gen = pipeline("text-generation", model="openai-community/gpt2")

def Extract_text(image):
    text=pytesseract.image_to_string(Image.open(image))
    return text

def Extract_keyword(text):
    doc=nlp(text)
    keywords=[chunk.text for chunk in doc.noun_chunks if len(chunk.text)>1]
    return keywords

def extract_text_from_pdf(pdf_path):
    document=fitz.open(pdf_path)
    text=""
    for page_num in range(len(document)):
        page= document.load_page(page_num)
        text += page.get_text()
    return text 


def match_keywords(existing_keywords, new_keywords):
    common_keywords = set(existing_keywords).intersection(new_keywords)
    if not existing_keywords:
        return False, common_keywords  # No existing keywords to match with

    match_percentage = len(common_keywords) / len(existing_keywords) * 100
    return match_percentage >= 50, common_keywords