
class Model:
    def __init__(self, model_url: str, timeout: int = 600):
        self.model_url = model_url
        self.timeout = timeout

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
