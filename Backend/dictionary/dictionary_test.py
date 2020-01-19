from .document import Document


def test_create_document():
    doc = Document(["ab", "ac", "ab"])
    assert doc.terms["ab"] == 2
    assert doc.terms["ac"] == 1

