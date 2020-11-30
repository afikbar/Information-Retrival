from InvertedIndex import InvertedIndex


def _difference_sorted(base: list, exclude: list) -> list:
    """
    Accept two sorted list and returns their symmetric difference.
    """
    res = []
    i = j = 0
    while i < len(base) and j < len(exclude):
        if base[i] == exclude[j]:
            i += 1
        elif base[i] < exclude[j]:
            res.append(base[i])
            i += 1
        elif base[i] > exclude[j]:
            j += 1

    res += base[i:]
    return res


def _intersect_sorted(l1: list, l2: list) -> list:
    """
    Accepts two sorted lists and return their sorted intersection.
    """
    res = []
    i = j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            res.append(l1[i])
            j += 1
            i += 1
        elif l1[i] > l2[j]:
            j += 1
        else:
            i += 1

    return res


def _union_sorted(l1: list, l2: list) -> list:
    """
    Accepts two sorted list and returns their sorted union.
    """
    res = []
    i = j = 0
    while i < len(l1) and j < len(l2):
        if l1[i] == l2[j]:
            res.append(l1[i])
            j += 1
            i += 1
        elif l1[i] > l2[j]:
            res.append(l2[j])
            j += 1
        else:
            res.append(l1[i])
            i += 1

    res += l1[i:]
    res += l2[j:]
    return res


def _rpn_eval(index: InvertedIndex, query: str) -> list:
    """
    Evaluates Reverse Polish Notation boolean query
    """
    docs_seqs = []

    for token in query.split():
        if token == 'OR':
            seq2 = docs_seqs.pop()
            seq1 = docs_seqs.pop()
            docs_seqs.append(_union_sorted(seq1, seq2))
        elif token == 'AND':
            seq2 = docs_seqs.pop()
            seq1 = docs_seqs.pop()
            docs_seqs.append(_intersect_sorted(seq1, seq2))
        elif token == 'NOT':
            exclude = docs_seqs.pop()
            base = docs_seqs.pop() if docs_seqs else list(range(1, index.document_count + 1))
            docs_seqs.append(_difference_sorted(base, exclude))

        else:
            docs_seqs.append(index[token.lower()])

    assert len(docs_seqs) == 1
    return docs_seqs[0]


def BooleanRetrieval(index: InvertedIndex, query: str) -> str:
    """
    Parse RPN boolean query and return matching DOCNOs from given index.
    """
    doc_ids = _rpn_eval(index, query)
    return ' '.join(map(index.get_docno, doc_ids))


if __name__ == "__main__":
    pass
