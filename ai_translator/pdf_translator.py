import pdfplumber
from PyPDF2 import PdfReader
import requests
import os
import sys

class PDFTranslator:
    def __init__(self, model):
        self.model = model
        self.book_contents = []
        self.translated_contents = []
        self.translate_status = []
        self.success_rate = 0
        self.headers = {
            'Content-Type': 'application/json;charset=utf-8'
        }

    def parse_pdf(self, book, pages=None):
        with pdfplumber.open(book) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for page in pages_to_parse:
                text = page.extract_text()
                self.book_contents.append(text)


    def handle_translation_response(self, response):
        try:
            response.raise_for_status()
            response_dict = response.json()
            translation = response_dict["response"]
            self.translated_contents.append(translation)
            self.translate_status.append(1)
        except Exception as e:
            exception_handler = TranslatorException(e)
            error_message = exception_handler.handle_exception()
            print(error_message, file=sys.stderr)
            self.translated_contents.append("[翻译失败]")
            self.translate_status.append(0)

    def translate_contents(self, book):
        successful_requests = 0
        total_requests = len(self.book_contents)

        with open(f"{book[:-4]}_analyzed.txt", "w", encoding="utf-8") as f:
            for i, text in enumerate(self.book_contents):
                prompt = f"翻译为中文：{text}"
                data = {
                    "prompt": prompt,
                    "history": []
                }
                response = requests.post(self.model.model_url, json=data, timeout=self.model.timeout)
                self.handle_translation_response(response)
                f.write(self.translated_contents[-1])

    def calculate_success_rate(self):
        successful_requests = sum(self.translate_status)
        total_requests = len(self.translate_status)
        self.success_rate = successful_requests / total_requests * 100
    
    def translate_pdf(self, book, pages=None):
        self.parse_pdf(book, pages)
        self.translate_contents(book)
        self.calculate_success_rate()