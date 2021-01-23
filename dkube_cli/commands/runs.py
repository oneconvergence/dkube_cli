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
def list(obj):
    data = obj["api"].list_runs(obj["type"], obj["username"])

    jobs = [["name", "last_updated", "status"]]
    for row in data[0]["jobs"]:
        p = JobModel(**row)
        jobs.append(
            [
                p.name,
                p.parameters["generated"]["timestamps"]["start"],
                p.parameters["generated"]["status"]["state"],
            ]
        )

    print(tabulate(jobs, headers="firstrow", showindex="always"))


@run.command()
@click.pass_obj
@click.argument("name")
def get(obj, name):
    data = obj["api"].get_run(obj["type"], obj["username"], name)
    pprint(data, sort_dicts=True)
