from crewai.flow import Flow, listen, start
from pydantic import BaseModel

from resume_opt.crews.for_ats_compliance.crew import \
    ResumeOptimizationForATSCompliance
from resume_opt.crews.for_job_posting.crew import \
    ResumeOptimizationForJobPostings


def read_file(path: str) -> str:
    with open(path, "r") as f:
        return f.read()


class ResumeOptimizationState(BaseModel):
    resume_contents: str = ""
    job_posting_contents: str = ""


class ResumeOptimizationFlow(Flow[ResumeOptimizationState]):
    """ResumeOptimization flow"""

    def __init__(self, inputs=None):
        super().__init__()
        if inputs and "resume_content" in inputs:
            self.state.resume_contents = inputs["resume_content"]
        if inputs and "job_posting" in inputs:
            self.state.job_posting_contents = inputs["job_posting"]

    @start()
    def optimize_resume_for_job_posting(self) -> None:
        """Optimize resume for job posting"""
        result = (
            ResumeOptimizationForJobPostings()
            .crew()
            .kickoff(
                inputs={
                    "resume_contents": self.state.resume_contents,
                    "job_posting_contents": self.state.job_posting_contents,
                }
            )
        )
        self.state.resume_contents = result.raw

    @listen(optimize_resume_for_job_posting)
    def optimize_resume_for_ats_compliance(self) -> None:
        """Optimize resume for ATS compliance"""
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


# Example usage
def kickoff(inputs=None):
    flow = ResumeOptimizationFlow(inputs=inputs)
    flow.kickoff()
