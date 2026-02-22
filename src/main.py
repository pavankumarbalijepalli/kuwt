from agents.researchers import Researchers
from agents.enthusiasts import Enthusiasts
from agents.teachers import Teachers
from utils.email_handler import send_email
from utils.logger import log
import markdown
import json
import os

class AgentOrchestrator:
    def __init__(self):
        self.researchers = Researchers()
        self.enthusiasts = Enthusiasts()
        self.teachers = Teachers()
        # self.date = dt.now().strftime("%Y%m%d")
        self.date = '20260221'
        log(f"Initialized Agent Orchestrator for date: {self.date}")
    
    def run(self):
        if os.path.exists(f'assets/output/{self.date}'):
            log(f"Output for date {self.date} already exists. Skipping agent execution.")
            return
        log("Starting Agent Orchestrator...")
        log("Running Researchers Agent...")
        self.researchers.run()
        log("Running Enthusiasts Agent...")
        self.enthusiasts.run()
        log("Running Teachers Agent...")
        self.teachers.run()
        log("All agents have completed their tasks.")
    
    def prepare_researcher(self):
        log("Preparing content from Researchers Agent output...")
        _json = json.load(open(f'assets/output/{self.date}/researchers.json'))
        # Prepare Markdown formatted string
        papers_content = {}
        for paper in _json:
            papers_content[paper] = {}
            for key, value in _json[paper].items():
                if key == 'linkedin_post':
                    linkedin = _json[paper][key]
                    linkedin_content = ""
                    for title, content in linkedin.items():
                        if isinstance(content, dict):
                            linkedin_content += f"{content['content']}\n\n"
                    papers_content[paper]['linkedin'] = linkedin_content
                elif key == 'instagram_post':
                    instagram = _json[paper][key]
                    instagram_content = ""
                    for title, content in instagram.items():
                        if isinstance(content, dict):
                            instagram_content += f"## {title.upper()}\n{content['content']}\n\n"
                    papers_content[paper]['instagram'] = instagram_content
                elif key == 'medium_post':
                    medium = _json[paper][key]
                    medium_content = ""
                    for title, content in medium.items():
                        if isinstance(content, dict):
                            medium_content += f"## {title.upper()}\n{content['content']}\n\n"
                    papers_content[paper]['medium'] = medium_content
                elif key == 'youtube_post':
                    youtube = _json[paper][key]
                    youtube_content = ""
                    for title, content in youtube.items():
                        if isinstance(content, dict):
                            youtube_content += f"## {title.upper()}\n{content['content']}\n\n"
                    papers_content[paper]['youtube'] = youtube_content
        log("Prepared content from Researchers Agent output.")
        return papers_content
    
    def prepare_enthusiast(self):
        log("Preparing content from Enthusiasts Agent output...")
        _json = json.load(open(f'assets/output/{self.date}/enthusiasts.json'))
        news = _json['news']['news']
        repos = _json['repos']

        news_content = {}
        for post, content in news.items():
            news_content[post] = ''
            for title, value in content.items():
                news_content[post] += f"## {title.upper()}\n{value}\n\n"
                
        repos_content = {}
        for repo, content in repos.items():
            repos_content[repo] = {}
            for title, value in content.items():
                repos_content[repo][title] = ''
                for sub_title, sub_value in value.items():
                    repos_content[repo][title] += f"## {sub_title.upper()}\n{sub_value}\n\n"
        log("Prepared content from Enthusiasts Agent output.")
        return news_content, repos_content
    
    def prepare_teacher(self):
        log("Preparing content from Teachers Agent output...")
        _json = json.load(open(f'assets/output/{self.date}/teachers.json'))
        fundamentals_content = {}
        for key, value in _json.items():
            fundamentals_content[key] = ''
            for title, content in value.items():
                if title == 'walkthrough_code':
                    fundamentals_content[key] += f"## {title.upper()}\n```python\n{content}\n```\n\n"
                elif title == "hashtags":
                    fundamentals_content[key] += f"## {title.upper()}\n```{content}```\n\n"
                else:
                    fundamentals_content[key] += f"## {title.upper()}\n{content}\n\n"
        log("Prepared content from Teachers Agent output.")
        return fundamentals_content

    def prepare_body(self):
        log("Preparing email body content...")
        paper_content = self.prepare_researcher()
        news_content, repos_content = self.prepare_enthusiast()
        fundamentals_content = self.prepare_teacher()

        # Today's Linkedin Posts
        all_linkedin_posts = "# RESEARCHER\n\n"
        all_instagram_posts = "# RESEARCHER\n\n"
        all_medium_posts = "# RESEARCHER\n\n"
        all_youtube_posts = "# RESEARCHER\n\n"

        log("Aggregating researcher content for email body...")
        for paper in paper_content:
            for key in paper_content[paper]:
                if key == 'linkedin':
                    all_linkedin_posts += paper_content[paper][key]
                    all_linkedin_posts += "<hr>"
                elif key == 'instagram':
                    all_instagram_posts += paper_content[paper][key]
                    all_instagram_posts += "<hr>"
                elif key == 'medium':
                    all_medium_posts += paper_content[paper][key]
                    all_medium_posts += "<hr>"
                elif key == 'youtube':
                    all_youtube_posts += paper_content[paper][key]
                    all_youtube_posts += "<hr>"

        # Today's News
        all_linkedin_posts += "\n\n# ENTHUSIAST\n\n"
        all_instagram_posts += "\n\n# ENTHUSIAST\n\n"
        all_medium_posts += "\n\n# ENTHUSIAST\n\n"
        all_youtube_posts += "\n\n# ENTHUSIAST\n\n"

        log("Aggregating enthusiast content for email body...")
        for post in news_content:
            if post == 'linkedin_post':
                all_linkedin_posts += news_content[post]
                all_linkedin_posts += "<hr>"
            elif post == 'instagram_post':
                all_instagram_posts += news_content[post]
                all_instagram_posts += "<hr>"
            elif post == 'youtube_video':
                all_youtube_posts += news_content[post]
                all_youtube_posts += "<hr>"

        for repo in repos_content:
            for post in repos_content[repo]:
                if post == 'linkedin_post':
                    all_linkedin_posts += repos_content[repo][post]
                    all_linkedin_posts += "<hr>"
                elif post == 'instagram_post':
                    all_instagram_posts += repos_content[repo][post]
                    all_instagram_posts += "<hr>"
                elif post == 'youtube_video':
                    all_youtube_posts += repos_content[repo][post]
                    all_youtube_posts += "<hr>"
                    
        all_linkedin_posts += "\n\n# TEACHER\n\n"
        all_instagram_posts += "\n\n# TEACHER\n\n"
        all_medium_posts += "\n\n# TEACHER\n\n"
        all_youtube_posts += "\n\n# TEACHER\n\n"

        log("Aggregating teacher content for email body...")
        for key in fundamentals_content:
            if key == 'linkedin_post':
                all_linkedin_posts += fundamentals_content[key]
                all_linkedin_posts += "<hr>"
            elif key == 'instagram_post':
                all_instagram_posts += fundamentals_content[key]
                all_instagram_posts += "<hr>"
            elif key == 'medium_post':
                all_medium_posts += fundamentals_content[key]
                all_medium_posts += "<hr>"
            elif key == 'youtube_post':
                all_youtube_posts += fundamentals_content[key]
                all_youtube_posts += "<hr>"
        return all_linkedin_posts, all_instagram_posts, all_medium_posts, all_youtube_posts
    
    def send_email(self):
        linkedin_post, instagram_post, medium_post, youtube_post = self.prepare_body()
        log("Sending email for Linkedin content...")
        send_email(full_post=markdown.markdown(linkedin_post), post_type="Linkedin Posts")
        log("Sending email for Instagram content...")
        send_email(full_post=markdown.markdown(instagram_post), post_type="Instagram Posts")
        log("Sending email for Medium content...")
        send_email(full_post=markdown.markdown(medium_post), post_type="Medium Posts")
        log("Sending email for Youtube content...")
        send_email(full_post=markdown.markdown(youtube_post), post_type="Youtube Posts")
        
        
if __name__ == "__main__":
    orchestrator = AgentOrchestrator()
    orchestrator.run()
    orchestrator.send_email()
