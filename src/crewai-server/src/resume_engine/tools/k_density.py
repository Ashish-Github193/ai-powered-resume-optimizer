from collections import Counter
from typing import Type

import nltk
from crewai.tools import BaseTool
from loguru import logger
from nltk.tokenize import word_tokenize
from pydantic import BaseModel

nltk.download("punkt_tab")


class KeywordDensityInput(BaseModel):
    text: str


class KeywordDensityCalculatorTool(BaseTool):
    name: str = "Keyword Density Calculator"
    description: str = "Calculates the density of keywords in a given text"
    args_schema: Type[BaseModel] = KeywordDensityInput

    def _run(self, text: str) -> dict[str, float]:
        if not text:
            logger.debug("No text provided, returning empty dictionary")
            return {}

        words = word_tokenize(text.lower())
        words = [word for word in words if word.isalnum()]
        total_words = len(words)

        word_counts = Counter(words)
        density = {
            word: (count / total_words) * 100
            for word, count in word_counts.items()
        }
        return density
