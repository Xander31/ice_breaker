#List of tools used for the agents
from langchain_community.tools.tavily_search import TavilySearchResults

def get_profile_url_tavily(name:str) -> str:
    search = TavilySearchResults()
    res = search.run(f"{name}")
    return res  #Note no parsing is done. The LLM will pick the URL part for us.
