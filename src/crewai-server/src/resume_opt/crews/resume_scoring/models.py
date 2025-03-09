from typing import List, Optional

from pydantic import BaseModel, Field, computed_field, field_validator


class ResumeScore(BaseModel):
    score: float = Field(
        -1, description="Score of a section of resume between 0 and 1"
    )
    positive_factors: List[str] = []
    negative_factors: List[str] = []

    @field_validator("score")
    @classmethod
    def check_score_range(cls, v):
        if v != -1 and (v < 0 or v > 1):
            raise ValueError("Score must be between 0 and 1 or -1 for unset")
        return v


class ResumeScoringResult(BaseModel):
    grammar_score: Optional[ResumeScore] = ResumeScore(score=-1)
    formatting_score: Optional[ResumeScore] = ResumeScore(score=-1)
    consistency_score: Optional[ResumeScore] = ResumeScore(score=-1)

    @computed_field(return_type=Optional[ResumeScore])
    @property
    def overall_score(self) -> Optional[ResumeScore]:
        scores = [
            s.score
            for s in [
                self.grammar_score,
                self.formatting_score,
                self.consistency_score,
            ]
            if s is not None and s.score != -1
        ]
        if not scores:
            return None  # No valid scores available

        avg_score = sum(scores) / len(scores)
        return ResumeScore(score=avg_score)
