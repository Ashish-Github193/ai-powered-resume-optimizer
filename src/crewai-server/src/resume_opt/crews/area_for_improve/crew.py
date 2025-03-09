from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_opt.crews.area_for_improve.models import (Resume,
                                                      ResumeSectionFeedback)


@CrewBase
class FindAreasForImprovement:

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def resume_structure_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_structure_analyst"],  # type: ignore
            verbose=True,
        )

    @agent
    def summary_experience_assessor(self) -> Agent:
        return Agent(
            config=self.agents_config["summary_experience_assessor"],  # type: ignore
            verbose=True,
            llm="o3-mini",
        )

    @agent
    def education_skills_verifier(self) -> Agent:
        return Agent(
            config=self.agents_config["education_skills_verifier"],  # type: ignore
            verbose=True,
            llm="o3-mini",
        )

    @agent
    def project_achievement_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config["project_achievement_reviewer"],  # type: ignore
            verbose=True,
            llm="o3-mini",
        )

    @task
    def resume_section_breakdown(self) -> Task:
        return Task(
            config=self.tasks_config["section_breakdown_task"],  # type: ignore
            output_pydantic=Resume,
        )

    @task
    def resume_experience_assessment(self) -> Task:
        return Task(
            config=self.tasks_config["resume_experience_assessment"],  # type: ignore
            output_pydantic=ResumeSectionFeedback,
        )

    @task
    def resume_education_check(self) -> Task:
        return Task(
            config=self.tasks_config["resume_education_check"],  # type: ignore
            output_pydantic=ResumeSectionFeedback,
        )

    @task
    def resume_skills_assessment(self) -> Task:
        return Task(
            config=self.tasks_config["resume_skills_assessment"],  # type: ignore
            output_pydantic=ResumeSectionFeedback,
        )

    @task
    def resume_project_reviewer(self) -> Task:
        return Task(
            config=self.tasks_config["resume_project_reviewer"],  # type: ignore
            output_pydantic=ResumeSectionFeedback,
        )

    @crew
    def breakdown_crew(self) -> Crew:
        """Creates the resume breakdown crew"""
        return Crew(
            agents=[self.resume_structure_analyst()],
            tasks=[self.resume_section_breakdown()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def resume_experience_crew(self) -> Crew:
        """Creates the resume experience crew"""
        return Crew(
            agents=[self.summary_experience_assessor()],
            tasks=[self.resume_experience_assessment()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def resume_education_crew(self) -> Crew:
        """Creates the resume education crew"""
        return Crew(
            agents=[self.education_skills_verifier()],
            tasks=[self.resume_education_check()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def resume_skills_crew(self) -> Crew:
        """Creates the resume skills crew"""
        return Crew(
            agents=[self.education_skills_verifier()],
            tasks=[self.resume_skills_assessment()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def resume_project_crew(self) -> Crew:
        """Creates the resume project crew"""
        return Crew(
            agents=[self.project_achievement_reviewer()],
            tasks=[self.resume_project_reviewer()],
            process=Process.sequential,
            verbose=True,
        )
