import string
from abc import ABC, abstractmethod


class TextProcessor(ABC):
    @abstractmethod
    def transform(self, text: str):
        pass


class ConvertCase(TextProcessor):
    def __init__(self, casing: str='lower'):
        self.casing = casing

    def transform(self, text: str) -> str:
        if self.casing == 'lower':
            return text.lower()
        elif self.casing == 'upper':
            return text.upper()
        elif self.casing == 'title':
            return text.title()
        else:
            raise TypeError(f'{self.casing} casing is not supported by {self.__class__.__name__}')


class RemovePunc(TextProcessor):
    def transform(self, text: str) -> str:
        return ''.join(map(lambda char: ' ' if char in string.punctuation else char, text))


class RemoveSpace(TextProcessor):
    def transform(self, text: str) -> str:
        return ' '.join(text.split())


class TextPipeline:
    def __init__(self, *args):
        self.transformers = args

    def transform(self, text: str) -> str:
        for tf_class in self.transformers:
            tf_ob = tf_class()
            text = tf_ob.transform(text)
        return text

    def __str__(self):
        transformers = ' -> '.join([tf_class.__name__ for tf_class in self.transformers])
        return f'Pipeline: [{transformers}]'
