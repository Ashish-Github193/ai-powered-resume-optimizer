from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ResumeOptimizationForJobPostings:
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def job_posting_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["job_posting_analyzer"],  # type: ignore
            verbose=True,
        )

    @agent
    def resume_content_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_content_matcher"],  # type: ignore
            verbose=True,
        )

    @task
    def job_posting_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["job_posting_analysis"],  # type: ignore
            agent=self.job_posting_analyzer(),
        )

    @task
    def resume_content_match(self) -> Task:
        return Task(
            config=self.tasks_config["resume_content_match"],  # type: ignore
            agent=self.resume_content_matcher(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # Automatically collected by CrewBase
            tasks=self.tasks,  # Automatically collected by CrewBase
            process=Process.sequential,
            verbose=True,
        )
