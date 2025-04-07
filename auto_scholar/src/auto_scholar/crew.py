from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import WebsiteSearchTool
from tools.custom_tool import addToVectorDB, getFromVectorDB, summarizeText

websearch = WebsiteSearchTool()
summarier = summarizeText()
add = addToVectorDB()
get = getFromVectorDB()

@CrewBase
class AutoScholar():
    """AutoScholar crew"""
    tasks_config = 'config/tasks.yaml'
    agents_config = 'config/agents.yaml'

    # Agents -----------------------------------------------------------------------------------------------------------------------------------
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[websearch, summarier, add],
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            tools=[get],
            verbose=True
        )
    
    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=True
        )

    # Tasks -----------------------------------------------------------------------------------------------------------------------------------
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
        )
    
    @task
    def pdf_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_task'],
            output_file='report.md'
        )

    # Crew -----------------------------------------------------------------------------------------------------------------------------------
    @crew
    def crew(self) -> Crew:
        
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
