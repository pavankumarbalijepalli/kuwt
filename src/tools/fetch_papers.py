from datetime import timedelta as td
from datetime import datetime as dt
from utils.logger import log
import requests
from pypdf import PdfReader
import io
import os

from dotenv import load_dotenv
load_dotenv('../../.env')

date_dash = (dt.now() - td(2)).strftime("%Y-%m-%d")
date = (dt.now() - td(2)).strftime("%d%m%Y")

DEFAULT_HTTP_TIMEOUT_S = 45

def get_papers():
    log(f"Downloading papers for date - {date_dash}")
    try:
        res = requests.get(
            f"https://huggingface.co/api/daily_papers?date={date_dash}",
            headers={"Authorization": os.getenv("HF_TOKEN")},
            params={"sort": "publishedAt"},
            timeout=DEFAULT_HTTP_TIMEOUT_S,
        )
        log(f"Response Status Code: {res.status_code}")
        res.raise_for_status()
        res = res.json()
    except Exception as e:
        log(f"Failed to fetch Hugging Face daily papers: {e}")
        return {}
    paper_names = {}
    if not res:
        log("No papers found for the given date.")
        return paper_names
    for paper in res[:3]:  # Download top 3 papers
        # log(f"Processing paper: {paper['paper']['title']}")
        id = paper["paper"]["id"]
        url = f"https://arxiv.org/pdf/{id}"
        print(f"Loading {paper['paper']['title']} from {url}")
        try:
            response = requests.get(url, timeout=DEFAULT_HTTP_TIMEOUT_S)
            response.raise_for_status()
            bytes = io.BytesIO(response.content)
            reader = PdfReader(bytes)
            paper_names[paper["paper"]["title"]] = ""
            for page in reader.pages:
                paper_names[paper["paper"]["title"]] += page.extract_text() or ""
        except Exception as e:
            log(f"Failed to download/parse paper PDF {id}: {e}")
    return paper_names
