import requests


class UserDoesNotExistError(Exception):
    pass


def get_github_user(username):
    response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
    if response.status_code == 404:
        raise UserDoesNotExistError("The user does not exist.")
    response.raise_for_status()
    return response.json()


def get_repos(link):
    response = requests.get(link, timeout=10)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    user_name = input("Enter a username: ")

    try:
        user_data = get_github_user(user_name)
        name = user_data["name"] or user_name
        public_repos_count = user_data["public_repos"]
        followers_count = user_data["followers"]
        year_of_creation = user_data["created_at"].split("-")[0]
        print(f"Name: {name}")
        print(f"Number of Public Repositories: {public_repos_count}")
        print(f"Number of followers: {followers_count}")
        print(f"Year when account was created: {year_of_creation}")
        repos = get_repos(user_data["repos_url"])
        repos = sorted(repos, key=lambda repo: repo["stargazers_count"], reverse=True)
        for rank, repo in enumerate(repos[0:3], start=1):
            print(f"{rank}. {repo['name']} - Stars: {repo['stargazers_count']}")

    except UserDoesNotExistError as e:
        print(e)
    except requests.exceptions.Timeout:
        print("Request timed out.")
    except requests.exceptions.ConnectionError:
        print("Couldn't connect to the internet.")
    except requests.exceptions.HTTPError as e:
        print(f"Github returned an error: {e}")
