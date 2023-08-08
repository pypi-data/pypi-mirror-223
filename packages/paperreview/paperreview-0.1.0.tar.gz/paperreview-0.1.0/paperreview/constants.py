import os
from typing import Optional


def str_default(value: Optional[str], default: str) -> str:
    if not value:
        return default

    return str(value)


OPENAI_API_KEY = str_default(os.getenv("OPENAI_API_KEY"), "")

if OPENAI_API_KEY == "":
    # warn user that OPENAI_API_KEY is not set
    print("OPENAI_API_KEY is not set")

Q_SUMMARY = """Summarize the paper’s claimed primary contributions: \
In 10-15 sentences, describe the key ideas, results, findings, and \
significance as claimed by the paper’s authors"""

Q_STRENGTHS = """What do you see as the main strengths of this work? \
Consider, among others, the significance of critical ideas, \
validation, writing quality, and data contribution. Explain \
clearly why these aspects of the paper are valuable."""

Q_WEAKNESSES = """What do you see as the main weaknesses of this work? \
Clearly explain why these are weak aspects of the paper, e.g., \
why a specific prior work has already demonstrated the key contributions, \
why the experiments are insufficient to validate the claims, etc."""

Q_REPRODUCIBILITY = """Reproducibility: Could the work be reproduced \
by a talented graduate student from the information in the paper?"""

Q_REFERENCES = """References: List the primary references of this paper"""

Q_LIST = [
    Q_SUMMARY,
    Q_STRENGTHS,
    Q_WEAKNESSES,
    Q_REPRODUCIBILITY,
    Q_REFERENCES,
]
