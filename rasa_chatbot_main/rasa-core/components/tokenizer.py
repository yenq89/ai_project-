from underthesea import word_tokenize
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.constants import TEXT
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import GraphComponent
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from typing import Any, Dict, Optional

@DefaultV1Recipe.register(
    [GraphComponent], is_trainable=False  # Đăng ký component trong pipeline của Rasa
)
class UndertheseaTokenizer(Tokenizer):
    @classmethod
    def create(
        cls,
        config: Dict[str, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: Any,
    ) -> "UndertheseaTokenizer":
        return cls(config)

# class UndertheseaTokenizer(Tokenizer):
#     def __init__(self, component_config=None):
#         super().__init__(component_config)

    # def tokenize(self, message, **kwargs):
    #     # Sử dụng underthesea để tách từ
    #     tokens = word_tokenize(message.text)
    #     # Trả về danh sách các token (dưới dạng chuỗi)
    #     return tokens

    def tokenize(self, message: Message, attribute: str = TEXT):
        text = message.get(attribute)
        tokens = word_tokenize(text)
        return self._convert_words_to_tokens(tokens, text)