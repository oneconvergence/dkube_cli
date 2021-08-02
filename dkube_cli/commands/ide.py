from pprint import pprint

import click
from dkube.sdk.internal.dkube_api import JobModel
from tabulate import tabulate


@click.group()
@click.pass_obj
def ide(obj):
    """IDE commands"""
    pass


@ide.command()
@click.pass_obj
@click.option("-a", "--shared", is_flag=True, default=False)
def list(obj, shared):

    data = obj["api"].list_ides(obj["username"], shared=shared)
    jobs = [["owner", "name", "gpu", "last_updated", "status"]]
    for entry in data:
        for row in entry["jobs"]:
            p = JobModel(**row)
            jobs.append(
                [
                    entry["owner"],
                    p.name,
                    p.parameters["notebook"]["ngpus"],
                    p.parameters["generated"]["timestamps"]["start"],
                    p.parameters["generated"]["status"]["state"],
                ]
            )

    print(tabulate(jobs, headers="firstrow", showindex="always"))


@ide.command()
@click.pass_obj
@click.argument("name")
def delete(obj, name):
    notebooks = [name]
    if name == "all":
        notebooks = []
        data = obj["api"].list_runs(obj["type"], obj["username"], shared=False)
        for entry in data:
            for row in entry["jobs"]:
                if row["parameters"][obj["type"]] is None:
                    continue
                notebooks.append(row["name"])

    if (len(notebooks)) == 0:
        print("No IDEs found")
        return

    print(f"deleting {len(notebooks)} notebook ", " ".join(notebooks))

    obj["api"]._api.jobs_list_delete_by_class(
        obj["username"], "notebook", {"jobs": notebooks}
    )


@ide.command()
@click.pass_obj
@click.argument("name")
def get(obj, name):
    data = obj["api"].get_ide(obj["username"], name)
    pprint(data, sort_dicts=True)
