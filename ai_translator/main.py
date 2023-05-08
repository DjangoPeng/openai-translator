import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import Environment, ArgumentParser, ConfigLoader, LOG
from model import Model
from translator import PDFTranslator

if __name__ == "__main__":
    environment = Environment()

    args = None
    if not environment.is_jupyter():
        argument_parser = ArgumentParser()
        args = argument_parser.parse_arguments()
        config_loader = ConfigLoader(args.config)
    else:
        config_loader = ConfigLoader('config.yaml')

    config = config_loader.load_config()
    file_path = args.book if hasattr(args, 'book') and args.book else config['book']
    model_url = args.model_url if hasattr(args, 'model_url') and args.model_url else config['model_url']
    timeout = args.timeout if hasattr(args, 'timeout') and args.timeout else config['timeout']

    model = Model(model_url=model_url, timeout=timeout)

    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法
    translator = PDFTranslator(model)
    translator.translate_pdf(file_path)

    LOG.info("翻译完成！")
