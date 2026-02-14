from tavily import TavilyClient
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import os

def fetch_news():
    """
    Fetch recent news articles related to AI advancements using the Tavily API.
    Returns:
        A dictionary of news articles with relevant details.
    """
    client = TavilyClient(os.getenv("TAVILY_API"))
    response = client.search(
        query="latest AI breakthroughs, agentic AI developments, enterprise AI adoption, robotics AI, AI infrastructure trends, regulation updates 2026",
        topic="news",
        search_depth="advanced",
        max_results=10,
        time_range="week",
        include_usage=True,
    )
    titles = [
        "News Title: " + article["title"].strip() for article in response["results"]
    ]
    contents = [article["content"].strip() for article in response["results"]]
    lengths = [len(content) for content in contents]
    news = pd.DataFrame({"name": titles, "description": contents, "length": lengths})
    return news


def fetch_tools():
    """
    Fetch recent AI tools from "There's an AI for That" website.
    Returns:
        A DataFrame of AI tools with relevant details.
    """
    data = requests.get(
        "https://theresanaiforthat.com", headers={"User-Agent": "Mozilla/5.0"}
    )
    soup = BeautifulSoup(data.text, "html.parser")
    names = soup.find_all(class_="tasks")[0].find_all(class_="ai_link_wrap")

    tools = pd.DataFrame()

    titles = [
        "Tool Name: " + name.find_all("span")[0].text for name in names
    ]
    urls = [name.find_all("a")[0]["href"] for name in names]
    trends = [
        int(trend.find_all("span")[-1].text.replace(",", ""))
        for trend in soup.find_all(class_="tasks")[0].find_all(class_="stats_views")
    ]
    times = [
        trend.find(class_="relative").text.replace("Released ", "")
        for trend in soup.find_all(class_="tasks")[0].find_all(class_="released")
    ]

    tools = pd.DataFrame({"name": titles, "url": urls, "trend": trends, "time": times})
    tools = tools.sort_values(by="trend", ascending=False)
    tools["time"] = tools["time"].apply(
        lambda x: x.split(" ")[0] if "Releases" not in x else "NA"
    )
    tools = tools[tools["time"] != "NA"]

    def convert_to_seconds(time_str):
        if "d" in time_str:
            return int(time_str[:-1]) * 24 * 3600
        elif "h" in time_str:
            return int(time_str[:-1]) * 3600
        elif "m" in time_str:
            return int(time_str[:-1]) * 60
        else:
            return int(time_str[:-1])

    tools["seconds"] = tools["time"].apply(convert_to_seconds)
    tools = tools[tools["seconds"] < 86400]
    tools = tools[tools["trend"] > 150]

    for url in tools["url"]:
        data = requests.get(
            f"https://theresanaiforthat.com{url}", headers={"User-Agent": "Mozilla/5.0"}
        )
        soup = BeautifulSoup(data.text, "html.parser")
        content = soup.find(class_="ai_description").text.strip().replace("\n", " ")
        tools.loc[tools["url"] == url, "description"] = content
        tools.loc[tools["url"] == url, "length"] = len(content)

    return tools


def fetch_repos():
    """
    Fetch trending GitHub repositories.
    Returns:
        A DataFrame of trending GitHub repositories with relevant details.
    """
    url = "https://github.com/trending?since=daily"
    data = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(data.text, "html.parser")
    repo_links = soup.find_all(class_="Box-row")
    repos = pd.DataFrame(
        {
            "name": [
                "Repo Name: "
                + repo_link.find(class_="Link").text.replace("\n", "").replace(" ", "")
                for repo_link in repo_links
            ]
        }
    )
   
    for repo_link in repos["name"]:
        repo_url = f"https://www.github.com/{repo_link.replace('Repo Name: ', '')}"
        repo_data = requests.get(repo_url, headers={"User-Agent": "Mozilla/5.0"})
        repo_soup = BeautifulSoup(repo_data.text, "html.parser")
        content = repo_soup.find("article").text.strip()
        repos.loc[repos["name"] == repo_link, "description"] = content
    repos["length"] = repos["description"].apply(lambda x: len(x) if x else 0)
    return repos

def run_fetch_tools_and_news():
    covered = json.load(open("assets/input/covered.json", "r"))
    
    news = fetch_news()[["name", "description"]]
    for item in covered["news"]:
        news = news.drop(news[news["name"].str.contains(item)].index)
    covered["news"].extend(news["name"].apply(lambda x: x.replace("News Title: ", "").strip()).tolist())
    
    repos = fetch_repos()[["name", "description"]]
    for item in covered["repos"]:
        repos = repos.drop(repos[repos["name"].str.contains(item)].index)
    covered["repos"].extend(repos["name"].apply(lambda x: x.replace("Repo Name: ", "").strip()).tolist())
    
    tools = fetch_tools()[["name", "description"]]
    for item in covered["tools"]:
        tools = tools.drop(tools[tools["name"].str.contains(item)].index)
    covered["tools"].extend(tools["name"].apply(lambda x: x.replace("Tool Name: ", "").strip()).tolist())
    
    json.dump(covered, open("assets/input/covered.json", "w"), indent=4)
    return news, repos, tools