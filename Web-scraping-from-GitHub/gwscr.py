import requests
from pprint import pprint

def get_trending_repositories(language, num_repositories):
    repositories = []
    page = 1

    while len(repositories) < num_repositories:
        url = f"https://github.com/search?q={language}&type=repositories&s=stars&o=desc&p={page}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            page_repositories = data['payload']['results']
            repositories.extend(page_repositories)
            page += 1
        else:
            print("Error!")
            return []
    return repositories[:num_repositories]



language = input('Enter language: ')
num_repositories = int(input('Number of repositories: '))


repositories = get_trending_repositories(language ,num_repositories)
if repositories:
    output = f"trending_{language}_repositories.txt"
    with open(output, mode="w", encoding="utf-8") as file:
        file.write(f"Top {num_repositories} {language} repositories on GitHub:\n")
        file.write(50 * "*")
        file.write(f"\n")
        for i, repo in enumerate(repositories, start=1):
            file.write(f"#{i} {repo['hl_name']} - {repo['hl_trunc_description']}\n"
                       f"URL: https://github.com/{repo['repo']['repository']['owner_login']}"
                       f"/{repo['repo']['repository']['name']}\n")
            file.write(50 * "-")
            file.write(f"\n")
        print(f"Results saved to '{output}")
else:
    print("No repositories found!")