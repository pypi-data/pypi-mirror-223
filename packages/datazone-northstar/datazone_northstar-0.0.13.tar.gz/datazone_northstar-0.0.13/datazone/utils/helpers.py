import git


def is_git_repo():
    try:
        _ = git.Repo()
    except git.exc.InvalidGitRepositoryError:
        return False
    else:
        return True
