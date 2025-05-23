from crewai.flow import Flow, start
from pydantic import BaseModel

from resume_engine.crews.for_ats_compliance.crew import \
    ResumeOptimizationForATSCompliance


class ResumeOptimizationState(BaseModel):
    resume_contents: str = ""
    job_posting_contents: str = ""


class ResumeOptimizationForATSFlow(Flow[ResumeOptimizationState]):
    """ResumeOptimizationForATSFlow flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_content" in inputs:
            self.state.resume_contents = inputs["resume_content"]

    @start()
    async def optimize_resume_for_ats_compliance(self) -> None:
        """Optimize resume for ATS compliance"""
        crew = ResumeOptimizationForATSCompliance().crew()
        result = await crew.kickoff_async(
            inputs={
                "resume_contents": self.state.resume_contents,
                "job_posting_contents": self.state.job_posting_contents,
            }
        )
        self.state.resume_contents = result.raw
