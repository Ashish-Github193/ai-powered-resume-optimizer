from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_engine.tools.k_density import KeywordDensityCalculatorTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ResumeOptimizationForKeywordDensity:
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    keyword_density_calculator = KeywordDensityCalculatorTool()  # type: ignore

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
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
