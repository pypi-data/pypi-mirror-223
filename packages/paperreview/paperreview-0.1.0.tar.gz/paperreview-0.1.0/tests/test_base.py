import os
from paperreview.helper import (
    extract_text_from_pdf,
    download_pdf_from_url,
    ChunkIterator,
)

from paperreview.constants import str_default

ATTENTION_PAPER = "https://arxiv.org/pdf/1706.03762.pdf"
# ATTENTION_PAPER = "https://openreview.net/pdf?id=q4pQkTlImdk"


def test_main():
    from paperreview.cli import main

    del main


def test_str_default():
    assert str_default("1", "2") == "1"
    assert str_default(None, "2") == "2"


def test_extract_text_from_pdf():
    pdf_file = download_pdf_from_url(ATTENTION_PAPER)
    text = extract_text_from_pdf(pdf_file)
    assert "Attention Is All You Need" in text


# Expensive to run, so commented out
# def test_ask_paper_text():
#     text = "This is a test text."
#     question = "What is the test text?"
#     # assuming that GPT-4 returns the following text for this question:
#     # "The test text is: This is a test text."
# assert (
#     ask_paper_text(text, question) == "The test text is: This is a test text."
# )


def test_download_pdf_from_url():
    pdf_file = download_pdf_from_url(ATTENTION_PAPER)
    assert os.path.exists(pdf_file)


def test_chunk_iterator():
    text = "This is a test text."
    chunk_iterator = ChunkIterator(text, 2, "gpt-3.5-turbo")

    # Check that the ChunkIterator instance has the correct length
    assert len(chunk_iterator) == 6

    # Check that the ChunkIterator instance yields the correct chunks
    chunks = list(chunk_iterator)
    # assert chunks == ['This', ' is', ' a ', 'tes', 't text.']
    assert "".join(chunks) == text


def test_integration():
    # Download the PDF
    pdf_file = download_pdf_from_url(ATTENTION_PAPER)

    # Extract the text
    text = extract_text_from_pdf(pdf_file)
    assert "Attention Is All You Need" in text

    # Divide the text into chunks
    chunk_iterator = ChunkIterator(text, 3000, "gpt-3.5-turbo")
    chunks = list(chunk_iterator)
    assert len(chunks) > 0

    # This test doesn't include a call to ask_paper_text due to the cost
