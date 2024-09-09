import requests
from github import Github
import os

# Set up your GitHub Token
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
g = Github(GITHUB_TOKEN)

def fetch_repositories(username):
    user = g.get_user(username)
    repos = user.get_repos()
    return repos

def analyze_repository(repo):
    complexity_score = 0
    loc = 0
    # Fetch repo files, analyze code complexity, LOC, etc.
    # You can use static analysis tools like PyLint, Cyclomatic complexity tools
    # and other code analysis methods.
    
    return complexity_score

def main():
    username = input("Enter the GitHub username: ")
    repos = fetch_repositories(username)
    
    for repo in repos:
        print(f"Analyzing repository: {repo.name}")
        complexity_score = analyze_repository(repo)
        print(f"Repository {repo.name} has a complexity score of {complexity_score}")

if __name__ == "__main__":
    main()