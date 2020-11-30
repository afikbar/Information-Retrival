from collections import defaultdict

from bs4 import BeautifulSoup
from bs4.element import Tag


class BidirectionalMap:
    """
    Biderctional Map between index IDs and DOCNOs.
    """

    def __init__(self) -> None:
        self._docnos = []
        self._docno_to_id = {}

    def add(self, docno: str) -> int:
        self._docnos.append(docno)
        i = len(self._docnos)
        self._docno_to_id[docno] = i  # 1-based.
        return i

    def get_docno(self, i: int) -> str:
        """
        Get DOCNO by index ID
        """
        return self._docnos[i - 1]  # 1-based

    def get_id(self, docno: str) -> int:
        """
        Get Index ID by DOCNO
        """
        return self._docno_to_id[docno]

    def __len__(self) -> int:
        return len(self._docnos)


class InvertedIndex:
    """
    Inverted Index class.
    """

    def __init__(self) -> None:
        self.index = defaultdict(list)
        self._id_docno_map = BidirectionalMap()

    def __repr__(self) -> str:
        return str(self.index)

    def __getitem__(self, item) -> list:
        return self.index[item]

    @property
    def document_count(self) -> int:
        return len(self._id_docno_map)

    @staticmethod
    def _element_to_dict(ele: Tag) -> dict:
        res = {
            'docno': ele.find('docno').text.strip(),
            'text': ' '.join([t.text.strip() for t in ele.find_all('text')])
        }
        return res

    def _index_document(self, ele: Tag) -> None:
        """
        Process a given document and update the index.
        """
        doc = self._element_to_dict(ele)
        doc_id = self._id_docno_map.add(doc['docno'])

        for word in set(doc['text'].split()):
            self.index[word].append(doc_id)

    def parse_file(self, path) -> None:
        """
        Read file in TRECTEXT format and index its documents.
        """
        with open(path, 'r') as f:
            xml_str = f"<ROOT> {' '.join(map(str.rstrip, f))} </ROOT>"

        for doc in BeautifulSoup(xml_str, 'lxml').find_all('doc'):
            self._index_document(doc)

    def get_docno(self, doc_id: int) -> str:
        """
        Given a document inner ID, returns its original DOCNO.
        """
        return self._id_docno_map.get_docno(doc_id)

    def finalize(self, dump_path=None) -> None:
        """
        Sorts index by Document Frequency, and save it.
        """
        self.index = {k: v for k, v in
                      sorted(self.index.items(), key=lambda kv: len(kv[1]), reverse=True)}
        if dump_path:
            self._dump(dump_path)

    def _dump(self, file_path) -> None:
        with open(file_path, 'w') as f:
            f.write('\n'.join(map(str, self.index.items())))


if __name__ == "__main__":
    pass
