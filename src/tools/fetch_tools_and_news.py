# import os
# os.chdir("..")

from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime as dt
import json
from utils.logger import log

def fetch_news():
    """
    Fetch recent news articles related to AI advancements using the smol.ai news.
    Returns:
        A string containing the formatted news content.
    """
    log("Fetching news from smol.ai...")
    data = requests.get(
        "https://news.smol.ai/issues", headers={"User-Agent": "Mozilla/5.0"}
    )
    soup = BeautifulSoup(data.text, "html.parser")
    year_month = dt.now().strftime("%Y-%B")
    latest_url = soup.find_all("div", id=f"{year_month}")[0].find_all("ul")[0].find_all("li")[0].find_all("a")[0]['href']
    
    title = soup.find_all("div", id=f"{year_month}")[0].find_all("ul")[0].find_all("li")[0].find_all('div', class_="font-semibold")[0].text.strip()
    latest_data = requests.get(
        f"https://news.smol.ai{latest_url}", headers={"User-Agent": "Mozilla/5.0"}
    )
    soup = BeautifulSoup(latest_data.text, "html.parser")
    content = soup.find_all("main", id="main-content")[0].text
    
    summary = content.split('AI Reddit Recap')[0].split('AI Twitter Recap')[0].strip()
    twitter_recap = content.split('AI Reddit Recap')[0].split('AI Twitter Recap')[-1].strip()
    reddit_recap = content.split('AI Reddit Recap')[-1].split('Less Technical AI Subreddit Recap')[0].strip()
    log(f"Fetched news article: {title}")
    return {"latest_url": latest_url, "content": f"Title: {title}, Main Headlines: {summary}, Twitter Recap: {twitter_recap}, Reddit Recap: {reddit_recap}"}

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
        time_str = time_str.strip()
        if "y" in time_str:
            return int(time_str[:-1]) * 365 * 24 * 3600
        elif "mo" in time_str:
            return int(time_str[:-2]) * 30 * 24 * 3600
        elif "d" in time_str:
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
    log("Fetching trending repositories from GitHub...")
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
    log("Fetched Top 3 trending repositories from GitHub.")
    return repos

def fetch_news_repos():
    covered = json.load(open("assets/input/covered.json", "r"))
    
    news = fetch_news()
    if news['latest_url'] in covered["news"]:
        news = {"latest_url": news['latest_url'], "content": "No new news articles to fetch"}
    covered["news"].extend([news["latest_url"]])
    
    repos = fetch_repos()[["name", "description"]].head(3)
    for item in covered["repos"]:
        repos = repos.drop(repos[repos["name"].str.contains(item)].index)
    covered["repos"].extend(repos["name"].apply(lambda x: x.replace("Repo Name: ", "").strip()).tolist())
    repos = {row['name']: row['description'] for _, row in repos.iterrows()}
    
    # tools = fetch_tools()[["name", "description"]]
    # for item in covered["tools"]:
    #     tools = tools.drop(tools[tools["name"].str.contains(item)].index)
    # covered["tools"].extend(tools["name"].apply(lambda x: x.replace("Tool Name: ", "").strip()).tolist())
    
    json.dump(covered, open("assets/input/covered.json", "w"), indent=4)
    return news, repos