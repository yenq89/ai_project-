from rasa.nlu.tokenizers.tokenizer import Tokenizer
from underthesea import word_tokenize

class UnderTheseaTokenizer(Tokenizer):
    def __init__(self, component_config=None):
        super().__init__(component_config)

    def tokenize(self, message, **kwargs):
        # Sử dụng underthesea để phân tách từ
        tokens = word_tokenize(message.text)
        # Trả về danh sách các token (dưới dạng chuỗi)
        return tokens
