import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.toolss import get_profile_irl_tavily

def lookup(name:str) -> str:
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    template="""
    Given the full name {name_of_person}, I want you to get the link of his/her LinkedIn profile page.
    Your answer should only contain the URL. (Example: https://www.linkedin.com/in/alvaro-espinoza-h/ )
    """

    prompt_template = PromptTemplate(input_variables=["name_of_person"], template=template)

    linkedin_url_search_tool = Tool(
        name="Crawl Google for LinkedIn profile page",
        func=get_profile_irl_tavily,
        description="Useful when you need to get the LinedIn profile page URL.",
    )

    tools_for_agent = [
        linkedin_url_search_tool
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]

    return linkedin_profile_url

if __name__ == "__main__":
    load_dotenv()
    linkedin_url = lookup(name="Alessandra Espinoza Holguin")
    print(f"URL found: {linkedin_url}")