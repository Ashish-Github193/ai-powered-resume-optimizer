from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from resume_opt.crews.area_for_imrpove.models import (Resume, ResumeScore,
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
    def resume_quality_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config["resume_quality_evaluator"],  # type: ignore
            verbose=True,
            llm="o3-mini",
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
    def overall_score_evaluation(self) -> Task:
        return Task(
            config=self.tasks_config["overall_score_evaluation"],  # type: ignore
            output_pydantic=ResumeScore,
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

    @task
    def resume_summary_evaluation(self) -> Task:
        return Task(
            config=self.tasks_config["resume_summary_evaluation"],  # type: ignore
            output_pydantic=ResumeScore,
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
    def overall_score_crew(self) -> Crew:
        """Creates the resume overall score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.overall_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def consistency_score_crew(self) -> Crew:
        """Creates the resume consistency score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.consistency_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def formatting_score_crew(self) -> Crew:
        """Creates the resume formatting score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.formatting_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def grammar_score_crew(self) -> Crew:
        """Creates the resume grammar score crew"""
        return Crew(
            agents=[self.resume_quality_evaluator()],
            tasks=[self.grammar_score_evaluation()],
            process=Process.sequential,
            verbose=True,
        )

    @crew
    def resume_summary_crew(self) -> Crew:
        """Creates the resume summary crew"""
        return Crew(
            agents=[self.summary_experience_assessor()],
            tasks=[self.resume_summary_evaluation()],
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
