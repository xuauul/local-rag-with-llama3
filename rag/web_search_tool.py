import os
from langchain_community.tools.tavily_search import TavilySearchResults

from utils import load_config

config = load_config()
os.environ["TAVILY_API_KEY"] = config["TAVILY_API_KEY"]

def load_web_search_tool():
    web_search_tool = TavilySearchResults(k=3)
    return web_search_tool