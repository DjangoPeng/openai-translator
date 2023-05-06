from .page import Page

class Book:
    def __init__(self):
        self.pages = []

    def add_page(self, page: Page):
        self.pages.append(page)