from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.custom_tool import SummarizeTool, AddToVectorDBTool, QueryVectorDBTool, WebSearchTool
from langchain_community.llms import HuggingFaceHub

# Initialize tools
websearch = WebSearchTool()
summarizer = SummarizeTool()
vector_adder = AddToVectorDBTool()
vector_querier = QueryVectorDBTool()

@CrewBase
class AutoScholar():
    """AutoScholar crew"""
    tasks_config = 'config/tasks.yaml'
    agents_config = 'config/agents.yaml'

    # Agents -------------------------------------------------------------------
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[websearch, summarizer, vector_adder],
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            tools=[vector_querier],
            verbose=True
        )
    
    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config['editor'],
            verbose=True
        )

    # Tasks -------------------------------------------------------------------
    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher()
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.analyst()
        )
    
    @task
    def pdf_task(self) -> Task:
        return Task(
            config=self.tasks_config['pdf_task'],
            output_file='report.md',
            agent=self.editor()
        )

    # Crew -------------------------------------------------------------------
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            llm=HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.1",
            model_kwargs={"temperature": 0.7, "max_length": 3000}
            )
        )