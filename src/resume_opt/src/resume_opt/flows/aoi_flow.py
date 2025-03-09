from crewai.crew import asyncio
from crewai.flow import Flow, listen, start

from resume_opt.crews.area_for_imrpove.crew import FindAreasForImprovement
from resume_opt.crews.area_for_imrpove.models import (Resume,
                                                      ResumeAnalysisResult)


class ResumeAOIFlowStates(ResumeAnalysisResult):
    resume_contents: str = ""
    resume: Resume = Resume()


class ResumeAOIFlow(Flow[ResumeAOIFlowStates]):  # type: ignore
    """ResumeAOIFlow flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_content" in inputs:
            self.state.resume_contents = inputs["resume_content"]

    @start()
    async def start_breakdown_crew(self) -> None:
        """Starts the breakdown crew"""
        self.breakdown_crew = FindAreasForImprovement().breakdown_crew()
        result = await self.breakdown_crew.kickoff_async()
        if not (resume := result.pydantic):
            raise ValueError("Error in breakdown crew")
        self.state.resume = resume

    @start()
    async def start_overall_score_crew(self) -> None:
        """Starts the overall score crew"""
        self.overall_score_crew = (
            FindAreasForImprovement().overall_score_crew()
        )
        result = await self.overall_score_crew.kickoff_async()
        if not (r := result.pydantic):
            raise ValueError("Error in overall score crew")
        self.state.overall_score = r.score

    @start()
    async def start_consistency_score_crew(self) -> None:
        """Starts the consistency score crew"""
        self.consistency_score_crew = (
            FindAreasForImprovement().consistency_score_crew()
        )
        result = await self.consistency_score_crew.kickoff_async()
        if not (r := result.pydantic):
            raise ValueError("Error in consistency score crew")
        self.state.consistency_score = r.score

    @start()
    async def start_formatting_score_crew(self) -> None:
        """Starts the formatting score crew"""
        self.formatting_score_crew = (
            FindAreasForImprovement().formatting_score_crew()
        )
        result = await self.formatting_score_crew.kickoff_async()
        if not (r := result.pydantic):
            raise ValueError("Error in formatting score crew")
        self.state.formatting_score = r.score

    @start()
    async def start_grammar_score_crew(self) -> None:
        """Starts the grammar score crew"""
        self.grammar_score_crew = (
            FindAreasForImprovement().grammar_score_crew()
        )
        result = await self.grammar_score_crew.kickoff_async()
        if not (r := result.pydantic):
            raise ValueError("Error in grammar score crew")
        self.state.grammar_score = r.score

    @listen(start_breakdown_crew)
    async def start_resume_summary_crew(self) -> None:
        """Starts the resume summary crew"""
        self.resume_summary_crew = (
            FindAreasForImprovement().resume_summary_crew()
        )
        result = await self.resume_summary_crew.kickoff_async()
        if not (score := result.pydantic):
            raise ValueError("Error in resume summary crew")
        self.state.sections_feedback.append(score)

    @listen(start_breakdown_crew)
    async def start_resume_experience_crew(self) -> None:
        """Starts the resume experience crew"""
        self.resume_experience_crew = (
            FindAreasForImprovement().resume_experience_crew()
        )
        result = await self.resume_experience_crew.kickoff_async()
        if not (score := result.pydantic):
            raise ValueError("Error in resume experience crew")
        self.state.sections_feedback.append(score)

    @listen(start_breakdown_crew)
    async def start_resume_education_crew(self) -> None:
        """Starts the resume education crew"""
        self.resume_education_crew = (
            FindAreasForImprovement().resume_education_crew()
        )
        result = await self.resume_education_crew.kickoff_async()
        if not (score := result.pydantic):
            raise ValueError("Error in resume education crew")
        self.state.sections_feedback.append(score)

    @listen(start_breakdown_crew)
    async def start_resume_skills_crew(self) -> None:
        """Starts the resume skills crew"""
        self.resume_skills_crew = (
            FindAreasForImprovement().resume_skills_crew()
        )
        result = await self.resume_skills_crew.kickoff_async()
        if not (score := result.pydantic):
            raise ValueError("Error in resume skills crew")
        self.state.sections_feedback.append(score)

    @listen(start_breakdown_crew)
    async def start_resume_project_crew(self) -> None:
        """Starts the resume project crew"""
        self.resume_project_crew = (
            FindAreasForImprovement().resume_project_crew()
        )
        result = await self.resume_project_crew.kickoff_async()
        if not (score := result.pydantic):
            raise ValueError("Error in resume project crew")
        self.state.sections_feedback.append(score)


async def kickoff(inputs: dict[str, str]) -> ResumeAnalysisResult:
    """Kickoff the resume analysis flow"""
    return await ResumeAOIFlow(inputs=inputs).kickoff_async()


def read_file(file_path: str) -> str:
    """Read a file and return its contents as a string"""
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    base_path = "resume_opt/inputs/"
    resume_content = read_file(base_path + "resume.md")
    inputs = {"resume_content": resume_content}
    result = asyncio.run(kickoff(inputs))
    print(result)
