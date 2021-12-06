from pprint import pprint

import click
from dkube.sdk.internal.dkube_api import JobModel
from tabulate import tabulate


@click.group()
@click.argument("run_type")
@click.pass_obj
def run(obj, run_type):
    """Runs commands"""
    if run_type in "training":
        run_type = "training"
    elif run_type in "preprocessing":
        run_type = "preprocessing"
    elif run_type in "inference" or run_type in "serving":
        run_type = "inference"

    obj["type"] = run_type


@run.command()
@click.pass_obj
@click.option("-a", "--shared", is_flag=True, default=False)
def list(obj, shared):
    data = obj["api"].list_runs(obj["type"], obj["username"], shared=shared)

    jobs = [["owner", "name", "tags", "description", "gpu", "last_updated", "status"]]
    for entry in data:
        for row in entry["jobs"]:
            p = JobModel(**row)
            if p.parameters[obj["type"]] is None:
                continue
            jobs.append(
                [
                    entry["owner"],
                    p.name,
                    p.parameters[obj["type"]]["tags"],
                    p.description,
                    p.parameters[obj["type"]]["ngpus"],
                    p.parameters["generated"]["timestamps"]["start"],
                    p.parameters["generated"]["status"]["state"],
                ]
            )

    print(tabulate(jobs, headers="firstrow", showindex="always"))


@run.command()
@click.pass_obj
@click.argument("name")
def delete(obj, name):
    jobs = [name]
    if name == "all":
        jobs = []
        data = obj["api"].list_runs(obj["type"], obj["username"], shared=False)
        for entry in data:
            for row in entry["jobs"]:
                if row["parameters"][obj["type"]] is None:
                    continue
                jobs.append(row["name"])

    if (len(jobs)) == 0:
        print("No runs found")
        return

    print(f"deleting {len(jobs)} runs ", " ".join(jobs))

    obj["api"]._api.jobs_list_delete_by_class(
        obj["username"], obj["type"], {"jobs": jobs}
    )


@run.command()
@click.pass_obj
@click.argument("name")
def get(obj, name):
    data = obj["api"].get_run(obj["type"], obj["username"], name)
    pprint(data, sort_dicts=True)
