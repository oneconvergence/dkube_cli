"""Console script for dkube_cli."""
import sys
from configparser import ConfigParser
from pathlib import Path

import click
from dkube.sdk import DkubeApi

from dkube_cli.commands.datum import code, dataset, model
from dkube_cli.commands.projects import project
from dkube_cli.commands.runs import run

config = ConfigParser()
config.read(str(Path.home() / ".dkube.ini"))


@click.group()
@click.pass_context
def main(ctx):
    """Console script for dkube_cli."""
    ctx.obj = None
    if "default" in config.sections():
        name = config.get("default", "name")
        if name in config.sections():
            url = config.get(name, "url")
            token = config.get(name, "token")
            api = DkubeApi(URL=url, token=token)
            username = config.get(name, "username")
            ctx.obj = {"api": api, "username": username}


@main.command()
@click.pass_obj
def configure(obj):
    """Configure DKube CLI"""

    name = click.prompt("Name for dkube instance:", default="dkube")
    url_default = "https://127.0.0.1:32222"
    token_default = ""

    if name in config.sections():
        url_default = config.get(name, "url")
        token_default = config.get(name, "token")

    url = click.prompt("DKube URL", default=url_default)
    token = click.prompt("Auth Token", default=token_default)

    api = DkubeApi(url, token)
    data = api.validate_token()

    if name not in config.sections():
        config.add_section(name)

    config.set(name, "url", url)
    config.set(name, "token", token)
    config.set(name, "username", data["username"])
    config.set(name, "role", data["role"])

    if "default" not in config.sections():
        config.add_section("default")
    config.set("default", "name", name)

    with open(str(Path.home() / ".dkube.ini"), "w") as f:
        config.write(f)


main.add_command(project)
main.add_command(code)
main.add_command(dataset)
main.add_command(model)
main.add_command(run)

if __name__ == "__main__":
    sys.exit(main(""))  # pragma: no cover
