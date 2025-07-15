from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

@CrewBase
class Workers():
    """Workers crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def product_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['product_manager'], # type: ignore[index]
            verbose=True
        )

    @agent
    def frontend_engineer_1(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer_1'], verbose=True
        )

    @agent
    def frontend_engineer_2(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer_2'], verbose=True
        )

    @agent
    def frontend_engineer_3(self) -> Agent:
        return Agent(
            config=self.agents_config['frontend_engineer_3'], verbose=True
        )

    @agent
    def backend_engineer_1(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer_1'], verbose=True
        )

    @agent
    def backend_engineer_2(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer_2'], verbose=True
        )

    @agent
    def backend_engineer_3(self) -> Agent:
        return Agent(
            config=self.agents_config['backend_engineer_3'], verbose=True
        )

    @agent
    def test_maker(self) -> Agent:
        return Agent(
            config=self.agents_config['test_maker'], # type: ignore[index]
            verbose=True
        )

    @agent
    def code_security_reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_security_reviewer'], # type: ignore[index]
            verbose=True
        )

    @task
    def product_definition_task(self) -> Task:
        return Task(
            description=self.tasks_config['product_definition_task']['description'],
            expected_output=self.tasks_config['product_definition_task']['expected_output'],
            agent=self.product_manager(),
            output_file='code/product_spec.md'
        )

    @task
    def frontend_planning_task(self) -> Task:
        return Task(
            description=self.tasks_config['frontend_planning_task']['description'],
            expected_output=self.tasks_config['frontend_planning_task']['expected_output'],
            agent=self.frontend_engineer_1()
        )

    @task
    def frontend_implementation_task_2(self) -> Task:
        return Task(
            description=self.tasks_config['frontend_implementation_task_2']['description'],
            expected_output=self.tasks_config['frontend_implementation_task_2']['expected_output'],
            agent=self.frontend_engineer_2()
        )

    @task
    def frontend_implementation_task_3(self) -> Task:
        return Task(
            description=self.tasks_config['frontend_implementation_task_3']['description'],
            expected_output=self.tasks_config['frontend_implementation_task_3']['expected_output'],
            agent=self.frontend_engineer_3(),
            output_file='code/frontend_code.html'
        )

    @task
    def backend_planning_task(self) -> Task:
        return Task(
            description=self.tasks_config['backend_planning_task']['description'],
            expected_output=self.tasks_config['backend_planning_task']['expected_output'],
            agent=self.backend_engineer_1()
        )

    @task
    def backend_implementation_task_2(self) -> Task:
        return Task(
            description=self.tasks_config['backend_implementation_task_2']['description'],
            expected_output=self.tasks_config['backend_implementation_task_2']['expected_output'],
            agent=self.backend_engineer_2()
        )

    @task
    def backend_implementation_task_3(self) -> Task:
        return Task(
            description=self.tasks_config['backend_implementation_task_3']['description'],
            expected_output=self.tasks_config['backend_implementation_task_3']['expected_output'],
            agent=self.backend_engineer_3(),
            output_file='code/backend_code.py'
        )

    @task
    def testing_task(self) -> Task:
        return Task(
            description=self.tasks_config['testing_task']['description'],
            expected_output=self.tasks_config['testing_task']['expected_output'],
            agent=self.test_maker(),
            output_file='code/test_plan.md'
        )

    @task
    def security_review_task(self) -> Task:
        return Task(
            description=self.tasks_config['security_review_task']['description'],
            expected_output=self.tasks_config['security_review_task']['expected_output'],
            agent=self.code_security_reviewer(),
            output_file='code/security_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Workers crew"""
        return Crew(
            agents=self.agents,
            tasks=[
                self.product_definition_task(),
                self.frontend_planning_task(),
                self.frontend_implementation_task_2(),
                self.frontend_implementation_task_3(),
                self.backend_planning_task(),
                self.backend_implementation_task_2(),
                self.backend_implementation_task_3(),
                self.testing_task(),
                self.security_review_task()
            ],
            process=Process.sequential,
            verbose=True,
        )
