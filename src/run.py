from pathlib import Path
from typing import Union

from src.nlp.text_process import (ConvertCase, RemovePunc, RemoveSpace,
                                  TextPipeline)


class Search:
    def __init__(self, documents_path: Union[str, Path], stop_words_path: Union[str, Path] = 'data/stop_words.txt'):
        """
        Search Engine to search in documents.

        :param documents_path: Path to documents
        :param stop_words_path: Path to stop words
        """
        # crawl data
        self.data = self.crawl(documents_path)

        # load text processor
        self.pipe = TextPipeline(ConvertCase, RemovePunc, RemoveSpace)

        # load stop words
        self.stop_words = self.load_stop_words(stop_words_path)

        # index data
        self.index = self.index_data()

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

    def index_data(self) -> dict:
        """
        Index data.

        return a dict which keys are words of data dict
        and values are a dict of doc_paths with frequency
        of the word in doc_path

        :return: Index of data.
        """
        index = {}
        for doc_path, doc_content in self.data.items():
            for word in doc_content.split():
                word = self.pipe.transform(word)

                if not word or word in self.stop_words:
                    continue

                # update words value dict
                if word in index:
                    index[word][doc_path] = index[word].get(doc_path, 0) + 1

                # set words value to a dict for the first time
                else:
                    index[word] = {doc_path: 1}

        return index


if __name__ == '__main__':
    searcher = Search('data/documents')
