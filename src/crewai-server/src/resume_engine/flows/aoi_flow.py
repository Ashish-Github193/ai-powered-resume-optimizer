from crewai.flow import Flow, listen, start

from resume_engine.crews.area_for_improve.crew import FindAreasForImprovement
from resume_engine.crews.area_for_improve.models import (Resume,
                                                         ResumeAnalysisResult)


class ResumeAOIFlowStates(ResumeAnalysisResult):
    resume_contents: str = ""
    resume: Resume = Resume()


class ResumeAOIFlow(Flow[ResumeAOIFlowStates]):  # type: ignore
    """ResumeAOIFlow flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_contents" in inputs:
            self.state.resume_contents = inputs["resume_contents"]

    @start()
    async def start_breakdown_crew(self) -> None:
        """Starts the breakdown crew"""
        self.breakdown_crew = FindAreasForImprovement().breakdown_crew()
        result = await self.breakdown_crew.kickoff_async(
            inputs={"resume_contents": self.state.resume_contents}
        )
        if not (resume := result.pydantic):
            raise ValueError("Error in breakdown crew")
        self.state.resume = resume  # type: ignore

    @listen(start_breakdown_crew)
    async def start_resume_experience_crew(self) -> None:
        """Starts the resume experience crew"""
        self.resume_experience_crew = (
            FindAreasForImprovement().resume_experience_crew()
        )
        result = await self.resume_experience_crew.kickoff_async(
            inputs={"contents": self.state.resume.model_dump()["experience"]}
        )
        if not (score := result.pydantic):
            raise ValueError("Error in resume experience crew")
        self.state.sections_feedback.append(score)  # type: ignore

    @listen(start_breakdown_crew)
    async def start_resume_education_crew(self) -> None:
        """Starts the resume education crew"""
        self.resume_education_crew = (
            FindAreasForImprovement().resume_education_crew()
        )
        result = await self.resume_education_crew.kickoff_async(
            inputs={"contents": self.state.resume.model_dump()["education"]}
        )
        if not (score := result.pydantic):
            raise ValueError("Error in resume education crew")
        self.state.sections_feedback.append(score)  # type: ignore

    @listen(start_breakdown_crew)
    async def start_resume_skills_crew(self) -> None:
        """Starts the resume skills crew"""
        self.resume_skills_crew = (
            FindAreasForImprovement().resume_skills_crew()
        )
        result = await self.resume_skills_crew.kickoff_async(
            inputs={"contents": self.state.resume.model_dump()["skills"]}
        )
        if not (score := result.pydantic):
            raise ValueError("Error in resume skills crew")
        self.state.sections_feedback.append(score)  # type: ignore

    @listen(start_breakdown_crew)
    async def start_resume_project_crew(self) -> None:
        """Starts the resume project crew"""
        self.resume_project_crew = (
            FindAreasForImprovement().resume_project_crew()
        )
        result = await self.resume_project_crew.kickoff_async(
            inputs={"contents": self.state.resume.model_dump()["projects"]}
        )
        if not (score := result.pydantic):
            raise ValueError("Error in resume project crew")
        self.state.sections_feedback.append(score)  # type: ignore


# async def kickoff(inputs: dict[str, str]) -> ResumeAnalysisResult:
#    """Kickoff the resume analysis flow"""
#    return await ResumeAOIFlow(inputs=inputs).kickoff_async()
#
#
# if __name__ == "__main__":
#    base_path = "resume_opt/inputs/"
#    resume_content = read_file(base_path + "rresume.md")
#    inputs = {"resume_contents": resume_content}
#    result = asyncio.run(kickoff(inputs))
#    print(result)
