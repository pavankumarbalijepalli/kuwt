from datetime import timedelta as td
from datetime import datetime as dt
from utils.logger import log
import pypdf
import requests
import os

date_dash = (dt.now() - td(2)).strftime("%Y-%m-%d")
date = (dt.now() - td(2)).strftime("%d%m%Y")


def download_hf_papers():

    log(f"Downloading papers for date - {date_dash}")
    res = requests.get(
        f"https://huggingface.co/api/daily_papers?date={date_dash}",
        headers={"Authorization": os.getenv("HF_TOKEN")},
        params={"sort": "publishedAt"},
    )
    log(f"Response Status Code: {res.status_code}")
    res = res.json()
    rank = 1
    paper_names = {}
    if not res:
        log("No papers found for the given date.")
        return paper_names
    for paper in res[:3]:  # Download top 3 papers
        log(f"Processing paper: {paper['paper']['title']}")
        id = paper["paper"]["id"]
        paper_names[f"{rank}_{id}.pdf"] = paper["paper"]["title"]
        url = f"https://arxiv.org/pdf/{id}"
        response = requests.get(url)
        print(f"Downloading {paper['paper']['title']} from {url}")
        if not os.path.exists(f"assets/input/papers/{date}"):
            os.makedirs(f"assets/input/papers/{date}")
        with open(f"assets/input/papers/{date}/{rank}_{id}.pdf", "wb") as file:
            file.write(response.content)
            rank += 1
            log(
                f"Saved paper: {paper['paper']['title']} as assets/input/papers/{date}/{rank}_{id}.pdf"
            )
    return paper_names


def get_papers():
    """
    This tool fetches the papers downloaded for a specific date and extracts their content. It returns a dictionary where the keys are the paper filenames and the values are the extracted content of the papers. If the papers for the given date have not been downloaded yet, it will return an empty dictionary.

    Returns:
      paper_names: dict - A dictionary where the keys are the paper filenames and the values are the extracted content
    """
    paper_names = {}
    if not os.path.exists(f"assets/input/papers/{date}"):
        paper_names = download_hf_papers()
    else:
        for filename in os.listdir(f"assets/input/papers/{date}"):
            if filename.endswith(".pdf"):
                paper_names[filename] = ""
    log(f"Papers downloaded for date -  {date}")
    for filename in os.listdir(f"assets/input/papers/{date}"):
        if not filename.endswith(".pdf"):
            continue
        reader = pypdf.PdfReader(f"assets/input/papers/{date}/{filename}")
        content = ""
        log(f"Paper {filename} with {len(reader.pages)} pages is getting ready...")
        for page in reader.pages:
            content += page.extract_text() + "\n"
        paper_names[filename] += content
        log(f"Paper {filename} pre-processed!")
    return paper_names
