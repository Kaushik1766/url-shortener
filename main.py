import os
import sys
import warnings

from dotenv import load_dotenv
from github import Github

from services.url_shortener import URLShortener

load_dotenv()
warnings.filterwarnings('ignore')

def main():
    try:
        access_token = os.getenv('GITHUB_ACESS_TOKEN')
        repo = os.getenv('URL_REPO')

        if access_token is None or repo is None:
            raise RuntimeError('acesss token or repo not defined in env')

        git = Github(access_token)
        repo = git.get_repo(str(repo))

        shortener = URLShortener(repo)

        command = sys.argv[1]
        input = sys.argv[2]

        if command == '-s':
            print(shortener.shorten(input)[:7])
        elif command=='-g':
            print(shortener.get_url(input))

    except RuntimeError:
        print('error occured')
        raise

if __name__ == "__main__":
    main()
