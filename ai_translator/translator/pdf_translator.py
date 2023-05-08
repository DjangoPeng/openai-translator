import sys
import requests
from typing import Optional
from book import Book, Page, Content, ContentType, TableContent
from model import Model
from translator.exceptions import TranslatorException
from translator.pdf_parser import PDFParser
from translator.writer import Writer
from translator.prompt_maker import PromptMaker
from utils import LOG

class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model
        self.pdf_parser = PDFParser()
        self.writer = Writer()
        self.prompt_maker = PromptMaker()

    def handle_translation_response(self, response):
        try:
            response.raise_for_status()
            response_dict = response.json()
            translation = response_dict["response"]
            return translation, True
        except Exception as e:
            exception_handler = TranslatorException(e)
            error_message = exception_handler.handle_exception()
            LOG.error(f"[翻译失败]{error_message}")
            return "", False

    def translate_content(self, content, target_language):
        prompt = self.prompt_maker.translate_prompt(content, target_language)
        payload = {
            "prompt": prompt,
            "history": []
        }
        response = requests.post(self.model.model_url, json=payload, timeout=self.model.timeout)
        translation, status = self.handle_translation_response(response)
        content.set_translation(translation, status)

    def translate_pdf(self, pdf_file_path: str, target_language: str = '中文', output_file_path: str = None, pages: Optional[int] = None):
        self.book = self.pdf_parser.parse_pdf(pdf_file_path, pages)

        for page in self.book.pages:
            for content in page.contents:
                self.translate_content(content, target_language)

        self.writer.save_translated_book(self.book, output_file_path)
