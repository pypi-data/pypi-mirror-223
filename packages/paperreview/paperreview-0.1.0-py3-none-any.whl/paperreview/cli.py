"""CLI interface for paperreview project.
"""
import argparse
import os

from tqdm import tqdm

from .constants import Q_LIST
from .helper import (
    ask_paper_text,
    download_pdf_from_url,
    extract_text_from_pdf,
)


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Summarize a PDF using GPT-4."
    )
    parser.add_argument(
        "pdf_file", type=str, help="Path or URL to the PDF file"
    )
    args = parser.parse_args()

    pdf_path = args.pdf_file
    # if URL, download PDF file
    if pdf_path.startswith("http"):
        print("Downloading PDF file...")
        pdf_path = download_pdf_from_url(pdf_path)

    text = extract_text_from_pdf(pdf_path)

    output_path = os.path.splitext(pdf_path)[0] + ".txt"

    with open(output_path, "w") as f:
        for i, question in tqdm(
            enumerate(Q_LIST), desc="Asking questions", total=len(Q_LIST)
        ):
            print(f"Q{i+1}. {question}")
            answer = ask_paper_text(text, question)
            print(answer)
            print("=" * 50)

            f.write(
                f"Question: {question}\nAnswer:\n{answer}\n"
                + ("=" * 50)
                + "\n"
            )


if __name__ == "__main__":  # pragma: no cover
    main()
