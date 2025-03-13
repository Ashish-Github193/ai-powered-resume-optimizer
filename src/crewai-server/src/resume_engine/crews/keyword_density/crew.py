from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_engine.tools.k_density import KeywordDensityCalculatorTool


@CrewBase
class ResumeOptimizationForKeywordDensity:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    keyword_density_calculator = KeywordDensityCalculatorTool()  # type: ignore

    @agent
    def keyword_density_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["keyword_density_optimizer"],  # type: ignore
            tools=[self.keyword_density_calculator],
            verbose=True,
        )

    @task
    def keyword_density_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["keyword_density_optimization"],  # type: ignore
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ResumeOptimization crew"""
        return Crew(
            agents=self.agents,  # type: ignore
            tasks=self.tasks,  # type: ignore
            process=Process.sequential,
            verbose=True,
        )
