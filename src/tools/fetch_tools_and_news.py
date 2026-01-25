from langchain_core.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
import requests
import pandas as pd
import os

@tool
def fetch_news():
    """
    Fetch recent news articles related to AI advancements using the Tavily API.
    Returns:
        A dictionary of news articles with relevant details.
    """
    client = TavilyClient(os.getenv("TAVILY_API"))
    response = client.search(
        query="ai advancements",
        topic="news",
        search_depth="advanced",
        max_results=10,
        time_range="week",
        include_usage=True
    )
    return {article['title']: article['content'] for article in response['results']}

def fetch_tools():
    
    # Scrape TIAFT website for trending AI tools
    data = requests.get("https://theresanaiforthat.com",
                        headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(data.text, 'html.parser')
    names = soup.find_all(class_='tasks')[0].find_all(class_="ai_link_wrap")
    tools = pd.DataFrame()
    titles = [name.find_all('span')[0].text for name in names]
    urls = [name.find_all('a')[0]['href'] for name in names]
    trends = [int(trend.find_all('span')[-1].text.replace(',', '')) for trend in soup.find_all(class_='tasks')[0].find_all(class_="stats_views")]
    times = [trend.find(class_="relative").text for trend in soup.find_all(class_='tasks')[0].find_all(class_="released")]
    times = [int(time.split(' ')[0][:-1]) if 'h' in time else int(time.split(' ')[0][:-1])*24 for time in times]
    tools = pd.DataFrame({'name': titles, 'url': urls, 'trend': trends, 'time': times})
    tools = tools[tools['time'] < 24]
    tools = tools.sort_values(by='trend', ascending=False).head(5)
    return tools

def fetch_repos():
    url = "https://github.com/trending?since=daily"
    data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(data.text, 'html.parser')
    repo_links = soup.find_all(class_='Box-row')
    repos = [repo_link.find(class_='Link').text.replace('\n', '').replace(' ','') for repo_link in repo_links]
    return repos

tools = fetch_tools()
tools