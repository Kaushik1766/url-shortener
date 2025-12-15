import os
import sys
import warnings
import json

from dotenv import load_dotenv
from github import Github

from services.url_shortener import URLShortener

load_dotenv()
warnings.filterwarnings("ignore")


access_token = os.getenv("GITHUB_ACESS_TOKEN")
repo = os.getenv("URL_REPO")

if access_token is None or repo is None:
    raise RuntimeError("acesss token or repo not defined in env")

git = Github(access_token)
repo = git.get_repo(str(repo))

shortener = URLShortener(repo)


def main():
    try:
        access_token = os.getenv("GITHUB_ACESS_TOKEN")
        repo = os.getenv("URL_REPO")

        if access_token is None or repo is None:
            raise RuntimeError("acesss token or repo not defined in env")

        git = Github(access_token)
        repo = git.get_repo(str(repo))

        shortener = URLShortener(repo)

        command = sys.argv[1]
        input = sys.argv[2]

        if command == "-s":
            print(shortener.shorten(input)[:7])
        elif command == "-g":
            print(shortener.get_url(input))

    except RuntimeError:
        print("error occured")
        raise


if __name__ == "__main__":
    main()


def encode(event, context):
    try:
        body = event["body"]
        data = json.loads(body)

        s_url = shortener.shorten(data["url"])

        return {"statusCode": 200, "body": json.dumps({"shortenedUrl": s_url})}

    except KeyError as e:
        print(f"KeyError: {e}")
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid input"})}


def decode(event, context):
    try:
        path_params = event["pathParameters"]
        short_url = path_params["url"]

        url = shortener.get_url(short_url)

        return {"statusCode": 200, "body": json.dumps({"url": url})}

    except KeyError as e:
        print(f"KeyError: {e}")
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid input"})}
