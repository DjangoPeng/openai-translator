import os
import sys
import pdfplumber
import requests
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from book import Book, Page, Content, ContentType, TableContent
from model import Model
from translator.exceptions import TranslatorException, PageOutOfRangeException


class PDFTranslator:
    def __init__(self, model: Model):
        self.model = model

    def parse_pdf(self, pdf_file_path: str, pages: Optional[int] = None) -> Book:
        self.book = Book()
        self.pdf_file_path = pdf_file_path
        with pdfplumber.open(pdf_file_path) as pdf:
            if pages is not None and pages > len(pdf.pages):
                raise PageOutOfRangeException(len(pdf.pages), pages)

            if pages is None:
                pages_to_parse = pdf.pages
            else:
                pages_to_parse = pdf.pages[:pages]

            for pdf_page in pages_to_parse:
                page = Page()

                # Handling text
                text = pdf_page.extract_text()
                print(f"[text] {text}")
                if text:
                    content = Content(content_type=ContentType.TEXT, original=text)
                    page.add_content(content)

                # Handling tables
                tables = pdf_page.extract_tables()
                print(f"[tables] {tables}")
                for table_data in tables:
                    table = TableContent(table_data)
                    page.add_content(table)
                    print(f"[table] {table}")

                # Handling images
                images = pdf_page.images
                for img in images:
                    image_content = Content(content_type=ContentType.IMAGE, original=img)
                    page.add_content(image_content)

                self.book.add_page(page)


    def handle_translation_response(self, response):
        try:
            response.raise_for_status()
            response_dict = response.json()
            translation = response_dict["response"]
            return translation, True
        except Exception as e:
            exception_handler = TranslatorException(e)
            error_message = exception_handler.handle_exception()
            print(error_message, file=sys.stderr)
            return "[翻译失败]", False

    def save_translated_book(self, output_file_path: str = None):
        if output_file_path is None:
            output_file_path = self.pdf_file_path.replace('.pdf', f'_translated.pdf')

        # Register Chinese font
        font_path = "../fonts/simsun.ttc"  # 请将此路径替换为您的字体文件路径
        pdfmetrics.registerFont(TTFont("SimSun", font_path))

        # Create a new ParagraphStyle with the SimSun font
        simsun_style = ParagraphStyle('SimSun', fontName='SimSun', fontSize=12, leading=14)

        # Create a PDF document
        doc = SimpleDocTemplate(output_file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Iterate over the pages and contents
        for page in self.book.pages:
            for content in page.contents:
                if content.content_type == ContentType.TEXT:
                    # Add translated text to the PDF
                    text = content.translation
                    para = Paragraph(text, simsun_style)
                    story.append(para)
                    # print(para)

                elif content.content_type == ContentType.TABLE:
                    # Add table to the PDF
                    table = content.translation
                    table_style = TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),  # 更改表头字体为 "SimSun"
                        ('FONTSIZE', (0, 0), (-1, 0), 14),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),  # 更改表格中的字体为 "SimSun"
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ])
                    pdf_table = Table(table)
                    pdf_table.setStyle(table_style)
                    story.append(pdf_table)

                elif content.content_type == ContentType.IMAGE:
                    # Add image to the PDF
                    image_data = content.translation
                    image = Image(image_data)
                    story.append(image)

            # Add a page break after each page except the last one
            if page != self.book.pages[-1]:
                story.append(PageBreak())

        # Save the translated book as a new PDF file
        doc.build(story)


    def translate_pdf(self, pdf_file_path: str, target_language: str = '中文', output_file_path: str = None, pages: Optional[int] = None):
        self.parse_pdf(pdf_file_path, pages)
        for page in self.book.pages:
            for content in page.contents:
                if content.content_type == ContentType.TEXT:
                    prompt = f"翻译为{target_language}：{content.original}"
                    payload = {
                        "prompt": prompt,
                        "history": []
                    }
                    response = requests.post(self.model.model_url, json=payload, timeout=self.model.timeout)
                    translation, status = self.handle_translation_response(response)
                    content.set_translation(translation, status)
                if content.content_type == ContentType.TABLE:
                    prompt = f"翻译为{target_language}，以表格形式返回：\n{content.original}"
                    payload = {
                        "prompt": prompt,
                        "history": []
                    }
                    print(f"prompt\n{prompt}")
                    response = requests.post(self.model.model_url, json=payload, timeout=self.model.timeout)
                    translation, status = self.handle_translation_response(response)
                    print(type(translation))
                    print(translation)
                    content.set_translation(translation, status)
                elif content.content_type == ContentType.IMAGE:
                    # 对于图片，我们不执行翻译操作
                    content.set_translation(content.original, True)
        self.save_translated_book()


    # def calculate_success_rate(self):
    #     total_contents = 0
    #     successful_translations = 0
    #     for page in self.book.pages:
    #         for content in page.contents:
    #             total_contents += 1
    #             if content.translation_status == 1:
    #                 successful_translations += 1
    #     self.success_rate = successful_translations / total_contents if total_contents > 0 else 0

