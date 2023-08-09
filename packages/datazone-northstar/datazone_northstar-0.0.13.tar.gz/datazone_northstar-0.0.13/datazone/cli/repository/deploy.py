import os
import uuid
from typing import Optional

import git
from rich import print

from datazone.core.common.config import ConfigReader
from datazone.models.config import Config
from datazone.service_callers.crud import CrudServiceCaller
from datazone.service_callers.git import GitServiceCaller
from datazone.service_callers.job import JobServiceCaller
from datazone.service_callers.repository import RepositoryServiceCaller
from datazone.utils.helpers import is_git_repo


def fetch_git_repo(repo_name: str, commit_message: Optional[str] = None) -> None:
    """
    Fetch git repository from the repository service.
    It uses the default server and default organisation. It creates a session with the given repository name.
    Also, it uses GitPython to fetch the repository and perform git operations.
    Args:
        repo_name (str): name of the repository
        commit_message (str): commit message
    """
    commit_message = commit_message or str(uuid.uuid4())

    server = RepositoryServiceCaller.get_default_server()
    organisation_name = server.get("default_organisation")

    if not organisation_name:
        print("[bold red]Default organisation does not exist![/bold red]")
        return

    session = RepositoryServiceCaller.create_session(
        server_id=server["_id"],
        organisation_name=organisation_name,
        repository_name=repo_name,
    )
    token = session.get("token")

    git_url = f"{GitServiceCaller.get_service_url()}/{token}"

    if not is_git_repo():
        repo = git.Repo.init()
        print("[green]Repository has initialized[/green]")

        origin = repo.create_remote("origin", git_url)
    else:
        repo = git.Repo()
        origin = repo.remotes.origin

    origin.fetch()
    repo.git.checkout("master")

    repo.index.add("*")
    repo.index.commit(commit_message)
    origin.push("master")
    print("[green]Files have pushed to the repository.[/green]:rocket:")


def deploy(file: Optional[str] = None, commit_message: Optional[str] = None) -> None:
    """
    Deploy project to the repository.
    Args:
        file: path to the custom config file
        commit_message: commit message
    """
    config_file = ConfigReader(file)

    if not config_file.is_config_file_exist():
        print("[bold red]Config file does not exist![/bold red]")
        return

    config: Config = config_file.read_config_file()
    project = CrudServiceCaller(service_name="job", entity_name="project").get_entity_with_id(
        entity_id=str(config.project_id),
    )
    for pipeline in config.pipelines:
        pipeline_file = pipeline.path
        if not os.path.exists(pipeline_file):
            print(f"[bold red]Pipeline file {pipeline_file} does not exist![/bold red]")
            return

    print("[bold green]Deploying...[/bold green]")

    repository_name = project.get("repository_name")
    fetch_git_repo(repository_name, commit_message)

    JobServiceCaller.inspect_project(project_id=str(config.project_id))
