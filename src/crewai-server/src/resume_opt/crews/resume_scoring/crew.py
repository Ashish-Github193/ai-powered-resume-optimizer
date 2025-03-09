from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_opt.crews.resume_scoring.models import ResumeScore


@CrewBase
class ResumeScoring:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def resume_quality_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_quality_evaluator"],  # type: ignore
            verbose=True,
            llm="o3-mini",
        )

    @task
    def consistency_score_evaluation(self) -> Task:
        return Task(
            config=self.tasks_config["consistency_score_evaluation"],  # type: ignore
            output_pydantic=ResumeScore,
        )

    @task
    def formatting_score_evaluation(self) -> Task:
        return Task(
            config=self.tasks_config["formatting_score_evaluation"],  # type: ignore
            output_pydantic=ResumeScore,
        )

    @task
    def grammar_score_evaluation(self) -> Task:
        return Task(
            config=self.tasks_config["grammar_score_evaluation"],  # type: ignore
            output_pydantic=ResumeScore,
        )

    @crew
    def consistency_score_crew(self) -> Crew:
        """Creates the consistency score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.consistency_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def formatting_score_crew(self) -> Crew:
        """Creates the formatting score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.formatting_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def grammar_score_crew(self) -> Crew:
        """Creates the grammar score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.grammar_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )
