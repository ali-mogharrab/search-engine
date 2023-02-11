from pathlib import Path
from typing import Union

from src.nlp.text_process import (ConvertCase, RemovePunc, RemoveSpace,
                                  TextPipeline)


class Search:
    def __init__(self, document_path: Union[str, Path], stop_words_path: Union[str, Path] = 'data/stop_words.txt'):
        #crawl data
        self.data = self.crawl(document_path)

        # load text processor
        self.pipe = TextPipeline(ConvertCase, RemovePunc, RemoveSpace)

        # load stop words
        self.stop_words = self.load_stop_words(stop_words_path)

    def crawl(self, document_path: Union[str, Path]) -> dict:
        """
        Crawl data from documents.

        :param document_path: Path to documents.
        :return: Data crawled.
        """
        data = {}
        for doc_path in Path(document_path).iterdir():
            if doc_path.suffix == '.txt':
                with open(doc_path) as f:
                    data[doc_path] = f.read()

        return data

    def load_stop_words(self, stop_words_path: Union[str, Path]) -> set:
        """
        Load stop words from file.

        :param stop_words_path: Path to stop words.
        :return: Set of stop words.
        """
        with open(stop_words_path) as f:
            stop_words = f.read()

        stop_words = stop_words.split('\n')
        # Process stop words
        stop_words = set(map(self.pipe.transform, stop_words))

        return stop_words


if __name__ == '__main__':
    searcher = Search('data/documents')
