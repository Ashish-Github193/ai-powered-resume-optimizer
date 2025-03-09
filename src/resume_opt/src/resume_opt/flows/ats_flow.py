from crewai.flow import Flow, start
from loguru import logger

from resume_opt.crews.for_ats_compliance.crew import \
    ResumeOptimizationForATSCompliance
from resume_opt.models import ResumeOptimizationState


class ResumeOptimizationForATSFlow(Flow[ResumeOptimizationState]):
    """ResumeOptimizationForATSFlow flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_content" in inputs:
            self.state.resume_contents = inputs["resume_content"]

        self.check_for_ats = False
        if inputs and "choices" in inputs:
            self.check_for_ats = inputs["choices"]["check_for_ats"] or False

    @start()
    def optimize_resume_for_ats_compliance(self) -> None:
        """Optimize resume for ATS compliance"""
        if not self.check_for_ats:
            logger.info("Skipping ATS compliance check")
            return

        result = (
            ResumeOptimizationForATSCompliance()
            .crew()
            .kickoff(
                inputs={
                    "resume_contents": self.state.resume_contents,
                    "job_posting_contents": self.state.job_posting_contents,
                }
            )
        )
        self.state.resume_contents = result.raw
