from __future__ import annotations
import logging
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from typing import Any, Dict, List, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.graph import ExecutionContext
from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from underthesea import word_tokenize
logger = logging.getLogger(__name__)
@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=False
)
class UndertheseaTokenizer(Tokenizer):
    provides = [TOKENS_NAMES[attribute] for attribute in MESSAGE_ATTRIBUTES]

    # @classmethod
    # def create(
    #         cls,
    #         config: Dict[Text, Any],
    #         model_storage: ModelStorage,
    #         resource: Resource,
    #         execution_context: ExecutionContext,
    # ) -> UndertheseaTokenizer:
    #     return cls(config)
    def __init__(self, component_config: Dict[Text, Any] = None) -> None:
        super().__init__(component_config)
        self.intent_tokenization_flag = component_config.get("intent_tokenization_flag", False)
        self.intent_split_symbol = component_config.get("intent_split_symbol", "_")

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        words = word_tokenize(text)
        tokens = self._convert_words_to_tokens(words, text)

        if self.intent_tokenization_flag:
            tokens = self._split_intent(tokens)

        return tokens

    def _split_intent(self, tokens: List[Token]) -> List[Token]:
        split_tokens = []
        for token in tokens:
            if self.intent_split_symbol in token.text:
                split_tokens.extend([
                    Token(text, token.start + i)
                    for i, text in enumerate(token.text.split(self.intent_split_symbol))
                ])
            else:
                split_tokens.append(token)
        return split_tokens

