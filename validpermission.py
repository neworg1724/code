import requests
import pandas as pd

# GitHub credentials
github_token = "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"
github_organization = "neworg1724"


# GitHub API URLs
repositories_url = f"https://api.github.com/orgs/{github_organization}/repos"
teams_url = f"https://api.github.com/orgs/{github_organization}/teams"

# Authenticate with GitHub using a token
github_headers = {"Authorization": f"Bearer {github_token}"}

# Fetch repositories
repositories_response = requests.get(repositories_url, headers=github_headers)
repositories_data = repositories_response.json()

# Fetch teams
teams_response = requests.get(teams_url, headers=github_headers)
teams_data = teams_response.json()

# Mapping of GitHub permission values to custom permission names
permission_mapping = {
    "admin": "Admin",
    "push": "Write",
    "pull": "Read",
    "maintain": "Maintain",
    "triage": "Triage"
}

# Prepare data for the repository, team, members, and permissions
data = []
for repo in repositories_data:
    team_response = requests.get(repo["teams_url"], headers=github_headers)
    team_data = team_response.json()
    if team_data:
        team_name = team_data[0]["name"]
        members_url = f"https://api.github.com/teams/{team_data[0]['id']}/members"
        members_response = requests.get(members_url, headers=github_headers)
        members_data = members_response.json()
        member_logins = ", ".join([member["login"] for member in members_data])
        permission = team_data[0]["permission"]
        custom_permission = permission_mapping.get(permission, "")
        data.append({
            "Repository": repo["name"],
            "Team": team_name,
            "Members": member_logins,
            "Permission": custom_permission
        })

# Create a pandas DataFrame from the data
df = pd.DataFrame(data)

# Save data to Excel sheet
df.to_excel("github_data.xlsx", index=False)
