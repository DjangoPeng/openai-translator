import openai
import requests
import simplejson

from model import Model

class OpenAIModel(Model):
    def __init__(self, model: str, api_key: str):
        self.model = model
        openai.api_key = api_key

    def make_request(self, prompt):
        try:
            if self.model == "gpt-3.5-turbo":
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                translation = response.choices[0].message['content'].strip()
            else:
                response = openai.Completion.create(
                    model=self.model,
                    prompt=prompt,
                    max_tokens=150,
                    temperature=0
                )
                translation = response.choices[0].text.strip()

            return translation, True
        except requests.exceptions.RequestException as e:
            raise Exception(f"请求异常：{e}")
        except requests.exceptions.Timeout as e:
            raise Exception(f"请求超时：{e}")
        except simplejson.errors.JSONDecodeError as e:
            raise Exception("Error: response is not valid JSON format.")
        except Exception as e:
            raise Exception(f"发生了未知错误：{e}")
        return "", False
