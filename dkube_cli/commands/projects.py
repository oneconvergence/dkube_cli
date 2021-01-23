import pprint

import click
from dkube.sdk.internal.dkube_api import ProjectModel
from tabulate import tabulate


@click.group()
def project():
    """Project commands"""
    pass


@project.command()
@click.pass_obj
def list(obj):
    data = obj["api"].list_projects()
    projects = [["name", "description", "leaderboard", "last_updated", "status"]]
    for row in data:
        p = ProjectModel(**row)
        projects.append(
            [
                p.id,
                p.name,
                p.description,
                p.leaderboard,
                p.last_updated,
                p.status["state"],
            ]
        )

    print(tabulate(projects, headers="firstrow", showindex="always"))


@project.command()
@click.pass_obj
@click.argument("project_id")
def get(obj, project_id):
    data = obj["api"].get_project(project_id)
    pprint.pprint(data, sort_dicts=True)
