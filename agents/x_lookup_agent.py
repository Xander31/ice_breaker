import os
from ctypes import HRESULT

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from tools.toolss import get_profile_url_tavily

def lookup_x_username (name:str) -> str:
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    template = """
    Given the name {name_of_person}, I want you to find the link of his/her X (previously know as Twitter) profile page, and extract from it his/her username.
    Your final answer must only contain the person's username, a unique username.
    """

    prompt_template = PromptTemplate(input_variables=["name_of_person"], template= template)

    x_username_search_tool = Tool(
        name="Crawl Google for X (Twitter) profile page",
        func=get_profile_url_tavily,
        description="Useful when you need to the the X(Twitter) profile page URL"
    )

    toos_for_agent = [
        x_username_search_tool
    ]

    react_prompt = hub.pull("hwchase17/react")

    agent = create_react_agent(llm=llm, tools=toos_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=toos_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    x_username = result["output"]

    return x_username

if __name__ == "__main__":
    load_dotenv()
    x_username = lookup_x_username(name="Donald Trump")
    print(f"X username found: {x_username}")