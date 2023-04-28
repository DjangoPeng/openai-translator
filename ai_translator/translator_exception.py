class TranslatorException:
    def __init__(self, e):
        self.exception = e

    def handle_exception(self):
        if isinstance(self.exception, requests.exceptions.RequestException):
            return f"请求异常：{self.exception}"
        elif isinstance(self.exception, requests.exceptions.Timeout):
            return f"请求超时：{self.exception}"
        elif isinstance(self.exception, simplejson.errors.JSONDecodeError):
            return "Error: response is not valid JSON format."
        else:
            return f"发生了未知错误：{self.exception}"
        
        
class PageOutOfRangeException(Exception):
    def __init__(self, book_pages, requested_pages):
        self.book_pages = book_pages
        self.requested_pages = requested_pages
        super().__init__(f"Page out of range: Book has {book_pages} pages, but {requested_pages} pages were requested.")
