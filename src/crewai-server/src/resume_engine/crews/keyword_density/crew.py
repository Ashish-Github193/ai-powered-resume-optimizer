from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_engine.crews.keyword_density.models import ResumeBreakdownResult
from resume_engine.tools.k_density import KeywordDensityCalculatorTool


@CrewBase
class ResumeOptimizationForKeywordDensity:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    keyword_density_calculator = KeywordDensityCalculatorTool()  # type: ignore

    @agent
    def resume_section_divider(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_section_divider"],  # type: ignore
            verbose=True,
        )

    @agent
    def header_and_summary_keyword_density_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["header_and_summary_keyword_density_optimizer"],  # type: ignore
            tools=[self.keyword_density_calculator],
            verbose=True,
        )

    @agent
    def skill_section_keyword_density_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["skill_section_keyword_density_optimizer"],  # type: ignore
            tools=[self.keyword_density_calculator],
            verbose=True,
        )

    @agent
    def work_experience_keyword_density_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["work_experience_keyword_density_optimizer"],  # type: ignore
            tools=[self.keyword_density_calculator],
            verbose=True,
        )

    @agent
    def education_certifications_keyword_density_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["education_certifications_keyword_density_optimizer"],  # type: ignore
            tools=[self.keyword_density_calculator],
            verbose=True,
        )

    @agent
    def additional_sections_keyword_density_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config["additional_sections_keyword_density_optimizer"],  # type: ignore
            tools=[self.keyword_density_calculator],
            verbose=True,
        )

    @agent
    def resume_updater_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_updater_agent"],  # type: ignore
            verbose=True,
        )

    @task
    def divide_resume_into_sections(self) -> Task:
        return Task(
            config=self.tasks_config["divide_resume_into_sections"],  # type: ignore
            output_pydantic=ResumeBreakdownResult,
        )

    @task
    def header_and_summary_keyword_density_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["header_and_summary_keyword_density_optimization"],  # type: ignore
        )

    @task
    def skill_section_keyword_density_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["skill_section_keyword_density_optimization"],  # type: ignore
        )

    @task
    def work_experience_keyword_density_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["work_experience_keyword_density_optimization"],  # type: ignore
        )

    @task
    def education_certifications_keyword_density_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["education_certifications_keyword_density_optimization"],  # type: ignore
        )

    @task
    def additional_sections_keyword_density_optimization(self) -> Task:
        return Task(
            config=self.tasks_config["additional_sections_keyword_density_optimization"],  # type: ignore
        )

    @task
    def resume_updatation(self) -> Task:
        return Task(
            config=self.tasks_config["resume_updatation"],  # type: ignore
        )

    @crew
    def section_divider_crew(self) -> Crew:
        """Creates the section divider crew"""
        return Crew(
            agents=[self.resume_section_divider()],  # type: ignore
            tasks=[self.divide_resume_into_sections()],  # type: ignore
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def header_and_summary_keyword_density_optimizer_crew(self) -> Crew:
        """Creates the header and summary keyword density optimizer crew"""
        return Crew(
            agents=[self.header_and_summary_keyword_density_optimizer()],
            tasks=[self.header_and_summary_keyword_density_optimization()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def skill_section_keyword_density_optimizer_crew(self) -> Crew:
        """Creates the skill section keyword density optimizer crew"""
        return Crew(
            agents=[self.skill_section_keyword_density_optimizer()],
            tasks=[self.skill_section_keyword_density_optimization()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def work_experience_keyword_density_optimizer_crew(self) -> Crew:
        """Creates the work experience keyword density optimizer crew"""
        return Crew(
            agents=[self.work_experience_keyword_density_optimizer()],
            tasks=[self.work_experience_keyword_density_optimization()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def education_certifications_keyword_density_optimizer_crew(self) -> Crew:
        """Creates the education and certifications keyword density optimizer crew"""
        return Crew(
            agents=[self.education_certifications_keyword_density_optimizer()],
            tasks=[
                self.education_certifications_keyword_density_optimization()
            ],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def additional_sections_keyword_density_optimizer_crew(self) -> Crew:
        """Creates the additional sections keyword density optimizer crew"""
        return Crew(
            agents=[self.additional_sections_keyword_density_optimizer()],
            tasks=[self.additional_sections_keyword_density_optimization()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def resume_updater_crew(self) -> Crew:
        """Creates the resume updater crew"""
        return Crew(
            agents=[self.resume_updater_agent()],
            tasks=[self.resume_updatation()],
            process=Process.sequential,
            verbose=True,
        )
