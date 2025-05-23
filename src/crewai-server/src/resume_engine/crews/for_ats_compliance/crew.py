from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class ResumeOptimizationForATSCompliance:
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def ats_compliance_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["ats_compliance_checker"], verbose=True
        )

    @agent
    def resume_content_matcher(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_content_matcher"], verbose=True
        )

    @task
    def ats_compliance_check(self) -> Task:
        return Task(
            config=self.tasks_config["ats_compliance_check"],
        )

    @task
    def resume_content_match(self) -> Task:
        return Task(
            config=self.tasks_config["resume_content_match"],
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
