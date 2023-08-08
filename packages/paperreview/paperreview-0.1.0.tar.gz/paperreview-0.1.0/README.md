# paperreview

[![codecov](https://codecov.io/gh/AdityaNG/PaperReview/branch/main/graph/badge.svg?token=PaperReview_token_here)](https://codecov.io/gh/AdityaNG/PaperReview)
[![CI](https://github.com/AdityaNG/PaperReview/actions/workflows/main.yml/badge.svg)](https://github.com/AdityaNG/PaperReview/actions/workflows/main.yml)

A python module to help read and summarize research papers.

## Install it from PyPI

```bash
pip install paperreview
```

## Usage

```py
from paperreview.constants import Q_SUMMARY
from paperreview.helper import (
    extract_text_from_pdf,
    ask_paper_text
)

text = extract_text_from_pdf(pdf_path)
question = Q_SUMMARY
answer = ask_paper_text(text, question)
```

```bash
$ python3 -m paperreview https://arxiv.org/pdf/1706.03762.pdf
#or
$ paperreview https://arxiv.org/pdf/1706.03762.pdf
```

## Development

Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
