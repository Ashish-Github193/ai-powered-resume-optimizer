from crewai.flow import Flow, start

from resume_engine.crews.resume_scoring.crew import ResumeScoring
from resume_engine.crews.resume_scoring.models import ResumeScoringResult


class ResumeScoringFlowStates(ResumeScoringResult):
    resume_contents: str = ""


class ResumeScoringFlow(Flow[ResumeScoringFlowStates]):  # type: ignore
    """ResumeAOIFlow flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_contents" in inputs:
            self.state.resume_contents = inputs["resume_contents"]

    @start()
    async def start_consistency_score_crew(self) -> None:
        """Starts the consistency score crew"""
        self.consistency_score_crew = ResumeScoring().consistency_score_crew()
        result = await self.consistency_score_crew.kickoff_async(
            inputs={"resume_contents": self.state.resume_contents}
        )
        if not (result := result.pydantic):
            raise ValueError("Error in consistency score crew")
        self.state.consistency_score = result  # type: ignore

    @start()
    async def start_formatting_score_crew(self) -> None:
        """Starts the formatting score crew"""
        self.formatting_score_crew = ResumeScoring().formatting_score_crew()
        result = await self.formatting_score_crew.kickoff_async(
            inputs={"resume_contents": self.state.resume_contents}
        )
        if not (result := result.pydantic):
            raise ValueError("Error in formatting score crew")
        self.state.formatting_score = result  # type: ignore

    @start()
    async def start_grammar_score_crew(self) -> None:
        """Starts the grammar score crew"""
        self.grammar_score_crew = ResumeScoring().grammar_score_crew()
        result = await self.grammar_score_crew.kickoff_async(
            inputs={"resume_contents": self.state.resume_contents}
        )
        if not (result := result.pydantic):
            raise ValueError("Error in grammar score crew")
        self.state.grammar_score = result  # type: ignore


async def kickoff(inputs: dict[str, str]) -> ResumeScoringResult:
    """Kickoff the resume analysis flow"""
    return await ResumeScoringFlow(inputs=inputs).kickoff_async()


# if __name__ == "__main__":
#    base_path = "resume_opt/inputs/"
#    resume_content = read_file(base_path + "rresume.md")
#    inputs = {"resume_contents": resume_content}
#    result = asyncio.run(kickoff(inputs))
#    print(result)
