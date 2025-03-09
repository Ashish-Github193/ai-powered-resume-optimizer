from crewai.flow import Flow, listen, start
from loguru import logger

from resume_engine.crews.for_ats_compliance.crew import \
    ResumeOptimizationForATSCompliance
from resume_engine.crews.for_job_posting.crew import \
    ResumeOptimizationForJobPostings
from resume_engine.models import ResumeOptimizationState


class ResumeOptimizationFlow(Flow[ResumeOptimizationState]):
    """ResumeOptimization flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_content" in inputs:
            self.state.resume_contents = inputs["resume_content"]
        if inputs and "job_posting" in inputs:
            self.state.job_posting_contents = inputs["job_posting"]

        self.check_for_ats = False
        if inputs and "choices" in inputs:
            self.check_for_ats = inputs["choices"]["check_for_ats"] or False

    @start()
    async def optimize_resume_for_job_posting(self) -> None:
        """Optimize resume for job posting"""
        crew = ResumeOptimizationForJobPostings().crew()
        result = await crew.kickoff_async(
            inputs={
                "resume_contents": self.state.resume_contents,
                "job_posting_contents": self.state.job_posting_contents,
            }
        )
        self.state.resume_contents = result.raw

    @listen(optimize_resume_for_job_posting)
    async def optimize_resume_for_ats_compliance(self) -> None:
        """Optimize resume for ATS compliance"""
        if not self.check_for_ats:
            logger.info("Skipping ATS compliance check")
            return

        crew = ResumeOptimizationForATSCompliance().crew()
        result = await crew.kickoff_async(
            inputs={
                "resume_contents": self.state.resume_contents,
                "job_posting_contents": self.state.job_posting_contents,
            }
        )
        self.state.resume_contents = result.raw
