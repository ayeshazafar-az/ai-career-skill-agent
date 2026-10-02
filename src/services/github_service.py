import requests
import re

def extract_github_username(url):
    """
    Extracts the GitHub username from a standard profile URL.
    """
    url = url.strip().rstrip('/')
    if 'github.com/' in url:
        # get the part after github.com/
        parts = url.split('github.com/')[-1].split('/')
        if parts:
            return parts[0]
    return None

def fetch_github_portfolio_context(url):
    """
    Hits the GitHub public API to pull the 5 most recently updated repositories
    and formats them into an AI-readable context block.
    """
    if not url:
        return ""
        
    username = extract_github_username(url)
    if not username:
        return ""
        
    try:
        # Using public API. (Rate limited to 60/hr without token, sufficient for demo)
        response = requests.get(f"https://api.github.com/users/{username}/repos?sort=updated&per_page=5", timeout=5)
        if response.status_code == 200:
            repos = response.json()
            if not repos:
                return f"GitHub Context: User {username} found, but no public repositories."
                
            portfolio = f"\n\n=== LIVE GITHUB PORTFOLIO EVIDENCE FOR '{username}' ===\n"
            portfolio += "The following are the candidate's active code repositories, providing definitive proof of technical application:\n\n"
            for repo in repos:
                name = repo.get('name', 'Unknown')
                desc = repo.get('description', '')
                if not desc: desc = 'No description provided.'
                lang = repo.get('language', 'Unknown')
                portfolio += f"• Repository: {name}\n  Description: {desc}\n  Primary Tech Stack: {lang}\n\n"
            return portfolio
        else:
            return ""
    except Exception as e:
        return ""
