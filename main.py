import pdfplumber
from PyPDF2 import PdfReader
import argparse
import requests
import simplejson

parser = argparse.ArgumentParser(description='Translate English PDF book to Chinese.')
parser.add_argument('--book', type=str, help='PDF file to translate.')
parser.add_argument('--model_url', type=str, default='http://127.0.0.1:8000', help='The URL of the translation model API.')
parser.add_argument('--timeout', type=int, default=10, help='Timeout for the API request in seconds.')

args = parser.parse_args()

# 解析 PDF 文件
book = args.book
with pdfplumber.open(book) as pdf:
    book_contents = []
    for page in pdf.pages:
        text = page.extract_text()
        book_contents.append(text)
        # print(text)

translated_contents = [] * len(book_contents)
# 中英文翻译...

headers = {
    'Content-Type': 'application/json;charset=utf-8'
}

for i, text in enumerate(book_contents):
    prompt = f"翻译为中文：{text}"
    data = {
        "prompt": prompt,
        "history": []
    }
    response = requests.post(args.model_url, json=data, timeout=args.timeout)

    try:
        # response = requests.post(args.model_url, json=data, timeout=args.timeout)
        print(f"response={response}")
        response_dict = response.json()
        print(f"response_dict={response_dict}")
        translation = response_dict["completions"][0]["text"]
        print(f"translation={translation}")
        translated_contents[i] = translation
    except simplejson.errors.JSONDecodeError:
        print("Error: response is not valid JSON format.")
        response_dict = {}


print(translated_contents)

# 合并翻译结果，写入新的 TXT 文件
with open(f"{book[:-4]}_analyzed.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(translated_contents))
