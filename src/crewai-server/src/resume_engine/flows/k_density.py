from crewai.flow import Flow, and_, listen, start
from pydantic import BaseModel

from resume_engine.crews.keyword_density.crew import \
    ResumeOptimizationForKeywordDensity
from resume_engine.crews.keyword_density.models import ResumeBreakdownResult


class KeywordDensityFlowInputState(BaseModel):
    resume: str = ""
    resume_result: str = ""
    header_and_summary_result: str = ""
    skills_result: str = ""
    work_experience_result: str = ""
    education_and_certifications_result: str = ""
    additional_sections_result: str = ""
    breakdown_result: ResumeBreakdownResult = ResumeBreakdownResult()


class KeywordDensityFlow(Flow[KeywordDensityFlowInputState]):

    crewbase = ResumeOptimizationForKeywordDensity()

    @start()
    async def start_breakdown_crew(self) -> None:
        """Start the breakdown crew"""
        crew = ResumeOptimizationForKeywordDensity().section_divider_crew()
        result = await crew.kickoff_async(inputs={"resume": self.state.resume})
        if not (result := result.pydantic):
            raise ValueError("Error in breakdown crew")
        self.state.breakdown_result = result  # type: ignore

    @listen(start_breakdown_crew)
    async def start_header_and_summary_optimization_crew(self) -> None:
        """Start the header and summary optimization crew"""
        crew = (
            self.crewbase.header_and_summary_keyword_density_optimizer_crew()
        )
        result = await crew.kickoff_async(
            inputs={"resume": self.state.breakdown_result.header_and_summary}
        )
        self.state.header_and_summary_result = result.raw

    @listen(start_breakdown_crew)
    async def start_skills_optimization_crew(self) -> None:
        """Start the skills optimization crew"""
        crew = self.crewbase.skill_section_keyword_density_optimizer_crew()
        result = await crew.kickoff_async(
            inputs={"resume": self.state.breakdown_result.skills_section}
        )
        self.state.skills_result = result.raw

    @listen(start_breakdown_crew)
    async def start_work_experience_optimization_crew(self) -> None:
        """Start the work experience optimization crew"""
        crew = self.crewbase.work_experience_keyword_density_optimizer_crew()
        result = await crew.kickoff_async(
            inputs={"resume": self.state.breakdown_result.work_experience}
        )
        self.state.work_experience_result = result.raw

    @listen(start_breakdown_crew)
    async def start_education_and_certifications_optimization_crew(
        self,
    ) -> None:
        """Start the education and certifications optimization crew"""
        crew = (
            self.crewbase.education_certifications_keyword_density_optimizer_crew()
        )
        result = await crew.kickoff_async(
            inputs={
                "resume": self.state.breakdown_result.education_and_certifications
            }
        )
        self.state.education_and_certifications_result = result.raw

    @listen(start_breakdown_crew)
    async def start_additional_sections_optimization_crew(self) -> None:
        """Start the additional sections optimization crew"""
        crew = (
            self.crewbase.additional_sections_keyword_density_optimizer_crew()
        )
        result = await crew.kickoff_async(
            inputs={"resume": self.state.breakdown_result.additional_sections}
        )
        self.state.additional_sections_result = result.raw

    @listen(
        and_(
            start_header_and_summary_optimization_crew,
            start_skills_optimization_crew,
            start_work_experience_optimization_crew,
            start_education_and_certifications_optimization_crew,
            start_additional_sections_optimization_crew,
        )
    )
    async def start_resume_updater_crew(self) -> None:
        """Start the resume updater crew"""
        crew = self.crewbase.resume_updater_crew()
        result = await crew.kickoff_async(
            inputs={
                "resume": self.state.breakdown_result.header_and_summary,
                "resume_optimized_content": self.state.header_and_summary_result,
            }
        )
        self.state.resume_result = result.raw


# async def kickoff(inputs: dict) -> dict[str, str]:
#    """Kickoff the keyword density flow"""
#    flow = KeywordDensityFlow()
#    await flow.kickoff_async(inputs=inputs)
#    return {"resume": flow.state.resume_result}
#
#
# if __name__ == "__main__":
#    base_path = "resume_engine/inputs/"
#    resume_content = read_file(base_path + "rresume.md")
#    inputs = {"resume": resume_content}
#    result = asyncio.run(kickoff(inputs))
#    print(result)
