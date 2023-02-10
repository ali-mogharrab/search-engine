from pathlib import Path
from typing import Union

from src.nlp.text_process import (ConvertCase, RemovePunc, RemoveSpace,
                                  TextPipeline)


class Search:
    def __init__(self, document_path: Union[str, Path]):
        #crawl data
        self.data = self.crawl(document_path)

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


if __name__ == '__main__':
    searcher = Search('data/documents')
