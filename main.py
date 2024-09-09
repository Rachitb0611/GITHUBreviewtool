import requests
from github import Github
import pandas as pd
import os

# username = input("Link: ")

# GitHub API Token
GITHUB_TOKEN = "your_github_token_here"

# Initialize PyGithub
g = Github(GITHUB_TOKEN)

def get_repositories(username):
    """Fetches public repositories for a given GitHub user"""
    user = g.get_user(username)
    return user.get_repos()

def count_lines_of_code(content):
    """Counts lines of code in the file content"""
    return len(content.split('\n'))

def calculate_folder_depth(path):
    """Calculates the depth of the folder structure"""
    return path.count('/')

def analyze_repository(repo):
    """Analyzes the complexity of a given repository"""
    complexity_score = 0
    total_lines_of_code = 0
    max_folder_depth = 0
    num_code_files = 0
    languages = repo.get_languages()
    
    contents = repo.get_contents("")
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == 'dir':
            contents.extend(repo.get_contents(file_content.path))
        else:
            if file_content.name.endswith(('.py', '.js', '.java', '.cpp')):
                # Download file and analyze
                content = requests.get(file_content.download_url).text
                total_lines_of_code += count_lines_of_code(content)
                num_code_files += 1
                max_folder_depth = max(max_folder_depth, calculate_folder_depth(file_content.path))
    
    # Example scoring algorithm
    complexity_score = total_lines_of_code * 0.4 + max_folder_depth * 0.3 + num_code_files * 0.3
    
    return complexity_score, languages

def generate_report(username):
    """Generates a report of all repositories and their complexity"""
    repos = get_repositories(username)
    repo_analysis = []

    for repo in repos:
        complexity_score, languages = analyze_repository(repo)
        repo_analysis.append({
            "name": repo.name,
            "complexity_score": complexity_score,
            "languages": languages,
            "stars": repo.stargazers_count,
            "forks": repo.forks_count,
            "watchers": repo.watchers_count
        })
    
    # Sort repositories by complexity score
    repo_analysis.sort(key=lambda x: x['complexity_score'], reverse=True)
    
    # Display the most complex repository
    most_complex_repo = repo_analysis[0]
    print(f"Most complex repository: {most_complex_repo['name']}")
    print(f"Complexity Score: {most_complex_repo['complexity_score']}")
    print(f"Languages Used: {most_complex_repo['languages']}")
    
    # Convert to DataFrame and save as CSV
    df = pd.DataFrame(repo_analysis)
    df.to_csv(f"{username}_repo_analysis.csv", index=False)
    
    return repo_analysis

# Example usage
if __name__ == "__main__":
    username = "github_username_here"
    generate_report('https://github.com/attreyabhatt')
