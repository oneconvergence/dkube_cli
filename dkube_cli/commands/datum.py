from pprint import pprint

import click
from dkube.sdk.internal.dkube_api import DatumModel
from tabulate import tabulate


def list_datums(data):
    repos = [["name", "source", "url", "last_updated", "status", "reason"]]
    for row in data[0]["datums"]:
        p = DatumModel(**row["datum"])
        repos.append(
            [
                p.name,
                p.source,
                p.url,
                p.generated["updated_time"]["end"],
                p.generated["status"]["state"],
                p.generated["status"]["reason"],
            ]
        )

    print(tabulate(repos, headers="firstrow", showindex="always"))


@click.group()
def code():
    """Code commands"""
    pass


@click.group()
def dataset():
    """Dataset commands"""
    pass


@click.group()
def model():
    """Model commands"""
    pass


@code.command("list")
@click.pass_obj
def list_code(obj):
    list_datums(obj["api"].list_code(obj["username"]))


@code.command("get")
@click.pass_obj
@click.argument("name")
def get_code(obj, name):
    data = obj["api"].get_code(obj["username"], name)
    pprint(data, sort_dicts=True)


@dataset.command("list")
@click.pass_obj
def list_datasets(obj):
    list_datums(obj["api"].list_datasets(obj["username"]))


@dataset.command("get")
@click.pass_obj
@click.argument("name")
def get_dataset(obj, name):
    data = obj["api"].get_dataset(obj["username"], name)
    pprint(data, sort_dicts=True)


@model.command("list")
@click.pass_obj
def list_models(obj):
    list_datums(obj["api"].list_models(obj["username"]))


@model.command("get")
@click.pass_obj
@click.argument("name")
def get_model(obj, name):
    data = obj["api"].get_model(obj["username"], name)
    pprint(data, sort_dicts=True)
