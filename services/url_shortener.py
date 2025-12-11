from github.Repository import Repository


class URLShortener:
    def __init__(self, repo) -> None:
        if not isinstance(repo, Repository):
            raise TypeError('invalid github instance provided')
        self.repo = repo

    def shorten(self, url : str) -> str:
        ref = self.repo.get_git_ref("heads/url")
        latest_commit = self.repo.get_git_commit(ref.object.sha)

        new_commit = self.repo.create_git_commit(
            message=url,
            tree=latest_commit.tree,
            parents=[latest_commit]
        )

        return new_commit.sha

    def get_url(self, shortened_url : str) -> str:
        commit = self.repo.get_git_commit(shortened_url)

        return commit.message
