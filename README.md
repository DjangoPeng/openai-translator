# AI Translator

A versatile AI translation tool powered by LLMs.

## Introduction

`AI Translator` is an AI-powered translation tool designed to translate English PDF books to Chinese. The project aims to provide a unified translation experience for users, allowing them to leverage the power of large language models (LLMs) without being aware of the underlying models. Currently, it supports ChatGLM and OpenAI GPT models.

The tool is built in Python and has a flexible, modular, and object-oriented design, making it easy to extend and adapt to different translation models and use cases.

## Getting Started

### Environment Setup

1. Clone the repository
2. Install the required dependencies by running `pip install -r requirements.txt`
3. Configure the `config.yaml` file with the desired model settings and API keys.

### Usage

You can run the translator with either the `config.yaml` file or by using command-line arguments.

Using `config.yaml`:

1. Update the `config.yaml` file with your desired settings, including model type, API keys, input PDF file, and output format.
2. Run `python main.py` to start the translation process.

Using command-line arguments:

1. Run `python main.py --model_type <model_type> --book <input_pdf> --file_format <output_format>`. You can also use additional flags for model-specific settings such as `--model_url`, `--api_key`, or `--timeout`.

## TODO List

- [ ] Add support for other languages and translation directions.
- [ ] Improve translation quality by using custom-trained translation models.
- [ ] Implement a graphical user interface (GUI) for easier use.
- [ ] Add support for batch processing of multiple PDF files.
- [ ] Improve error handling and fault tolerance.
- [ ] Create a web service or API to enable usage in web applications.
- [ ] Integrate with popular e-book formats like EPUB and MOBI.
- [ ] Add support for preserving the original layout and formatting of the source PDF.
- [ ] Extend support for other open-source large language models.

