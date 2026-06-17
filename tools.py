from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets. """
    results = tavily.search(query=query,max_results=5)
    return results
print(web_search.invoke("what are the recent news of war?"))
  
  
  

def scrape_url(url: str) -> str:
    import requests
    try:
        from bs4 import BeautifulSoup
        r = requests.get(url, timeout=10)
        return BeautifulSoup(r.text, 'html.parser').get_text()
    except:
        return 'Could not scrape URL'
