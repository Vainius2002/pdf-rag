from app.services.chunker import chunker

def test_empty_string_returns_empty_list():
    assert chunker("") == []
    
def test_short_text_returns_one_chunk():
    text = "Hello world"
    chunks = chunker(text)
    assert len(chunks) == 1
    assert chunks[0] == "Hello world"


def test_long_text_splits_into_correct_number_of_chunks():
    text = "a" * 1200                # 1200 chars
    chunks = chunker(text, chunk_size=500)
    assert len(chunks) == 3           # 500 + 500 + 200
    assert chunks[0] == "a" * 500
    assert chunks[1] == "a" * 500
    assert chunks[2] == "a" * 200


def test_default_chunk_size_is_500():
    text = "a" * 600
    chunks = chunker(text)            # no chunk_size arg = uses default
    assert len(chunks[0]) == 500