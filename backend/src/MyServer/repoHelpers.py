import git


def stageChanges(repoFolderPath: str) -> bool:
    try:
        repo = git.Repo(repoFolderPath)
        repo.git.add(repoFolderPath)
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    except OSError:
        return False
    

def removeFromRepo(userFolder: str, targetPath: str) -> bool:
    """Probably unnessesery for later"""
    try:
        repo = git.Repo(userFolder)
        repo.index.remove([targetPath])
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False
    

def commitAndPush(userFolder: str, message: str) -> bool:
    try:
        repo = git.Repo(userFolder)
        repo.index.commit(message)
        repo.remote().push()
        return True
    except git.InvalidGitRepositoryError:
        return False
    except git.NoSuchPathError:
        return False