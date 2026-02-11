import os
os.chdir('..')

from langchain_core.tools import tool
from datetime import timedelta as td
from datetime import datetime as dt
from utils.logger import log
import requests
import os

date_dash = (dt.now() - td(2)).strftime('%Y-%m-%d')
date = (dt.now() - td(2)).strftime('%d%m%Y')

@tool
def download_hf_papers():
  if os.path.exists(f"papers/{date}"):
    log(f"Papers already downloaded for date - {date}")
    return
  log(f"Downloading papers for date - {date_dash}")
  res = requests.get(f"https://huggingface.co/api/daily_papers?date={date_dash}",
      headers={
        "Authorization": os.getenv("HF_TOKEN")
      },
      params={
        "sort": "publishedAt"
      }
  )
  log(f"Response Status Code: {res.status_code}")
  res = res.json()
  rank = 1
  paper_names = {}
  if not res:
    log("No papers found for the given date.")
    return paper_names
  for paper in res[:3]: # Download top 3 papers
    log(f"Processing paper: {paper['paper']['title']}")
    id = paper['paper']['id']
    paper_names[f"{rank}_{id}.pdf"] = paper['paper']['title']
    url = f"https://arxiv.org/pdf/{id}"
    response = requests.get(url)
    print(f"Downloading {paper['paper']['title']} from {url}")
    if not os.path.exists(f"papers/{date}"):
      os.makedirs(f"papers/{date}")
    with open(f"papers/{date}/{rank}_{id}.pdf", 'wb') as file:
      file.write(response.content)
      rank += 1
      log(f"Saved paper: {paper['paper']['title']} as papers/{date}/{rank}_{id}.pdf")
  return paper_names

download_hf_papers()