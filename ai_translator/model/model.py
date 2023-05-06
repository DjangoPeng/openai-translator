from enum import Enum, auto

class ModelType(Enum):
    ChatGLM = auto()
    GPT_3 = auto()
    GPT_3_5 = auto()

class Model:
    def __init__(self, model_url, timeout, model_type=ModelType.ChatGLM):
        self.model_url = model_url
        self.timeout = timeout
        self.model_type = model_type
