import asyncio

import litellm
from crewai.flow import Flow, start
from pydantic import BaseModel

from resume_engine.crews.keyword_density.crew import \
    ResumeOptimizationForKeywordDensity
from resume_engine.utils import read_file

litellm._turn_on_debug()  # type: ignore


class ResumeOptimizationState(BaseModel):
    resume_contents: str = ""
    job_posting_contents: str = ""


class ResumeOptimizationForKeywordDensityFlow(Flow[ResumeOptimizationState]):
    """ResumeOptimizationForKeywordDensityFlow flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_content" in inputs:
            self.state.resume_contents = inputs["resume_content"]

    @start()
    async def optimize_resume_for_keyword_density(self) -> None:
        """Optimize resume for keyword density"""
        crew = ResumeOptimizationForKeywordDensity().crew()
        result = await crew.kickoff_async(
            inputs={"resume_contents": self.state.resume_contents}
        )
        self.state.resume_contents = result.raw


async def kickoff(inputs: dict[str, str]) -> ResumeOptimizationState:
    """Kickoff the resume optimization flow"""
    return await ResumeOptimizationForKeywordDensityFlow(
        inputs=inputs
    ).kickoff_async()


if __name__ == "__main__":
    base_path = "resume_engine/inputs/"
    resume_content = read_file(base_path + "rresume.md")
    inputs = {"resume_contents": resume_content}
    result = asyncio.run(kickoff(inputs))
    print(result)
