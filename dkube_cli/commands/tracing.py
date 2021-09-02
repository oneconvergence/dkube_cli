import os
import tempfile
import time
import webbrowser

import click
import requests
from logzero import logger
from ruamel import yaml

from dkube_cli.utils import kubectl, wait_for_k8s_resource

yaml_file = "https://raw.githubusercontent.com/istio/istio/release-1.10/samples/addons/jaeger.yaml"


def update_cm(sampling):
    process = kubectl(
        ["get", "cm", "-n", "istio-system", "istio", "-o", "yaml"],
        print_output=False,
    )
    if process.returncode != 0:
        logger.error(process.stderr.decode("ascii"))
        return
    cm = yaml.safe_load(process.stdout.decode("ascii"))
    mesh = yaml.safe_load(cm["data"]["mesh"])
    if sampling != 0:
        tracing = {
            "sampling": sampling,
            "zipkin": {"address": "zipkin.istio-system:9411"},
        }
        mesh["defaultConfig"]["tracing"] = tracing
        mesh["enableTracing"] = True
    else:
        mesh["defaultConfig"]["tracing"] = {}
        mesh["enableTracing"] = False

    cm["data"]["mesh"] = yaml.dump(mesh, indent=2)
    template = {
        "apiVersion": "v1",
        "data": cm["data"],
        "kind": "ConfigMap",
        "metadata": {"name": "istio", "namespace": "istio-system"},
    }
    yaml.scalarstring.walk_tree(template)
    with tempfile.NamedTemporaryFile(mode="w") as tmp:
        yaml.round_trip_dump(
            template,
            tmp,
            default_style=None,
            default_flow_style=False,
            indent=2,
            block_seq_indent=2,
            line_break=0,
            explicit_start=True,
        )
        tmp.flush()
        process = kubectl(["replace", "cm", "-n", "istio-system", "-f", tmp.name])

        if process.returncode != 0:
            raise click.Abort()


@click.group()
@click.pass_obj
def tracing(obj):
    """tracing commands"""
    pass


@tracing.command()
@click.option("-s", "--sampling-rate", default=100)
def install(sampling_rate):
    kubectl(["apply", "-f", yaml_file])
    wait_for_k8s_resource("deployment", "jaeger")
    update_cm(sampling_rate)
    kubectl(["delete", "pod", "-n", "istio-system", "-l", "app=istiod"])


@tracing.command()
def ui():
    os.system("kubectl port-forward -n istio-system svc/tracing 16686:80 &>/dev/null &")
    while True:
        try:
            time.sleep(1)
            print(".", end="")
            r = requests.get("http://localhost:16686")
            if r.status_code == 200:
                break
        except Exception:
            pass
    webbrowser.open("http://localhost:16686")


@tracing.command()
@click.argument("namespace")
def enable(namespace):
    patch = '{"metadata":{"labels":{"istio-injection":"enabled"}}}'
    kubectl(["patch", "ns", namespace, "-p", patch])


@tracing.command()
@click.argument("namespace")
def disable(namespace):
    patch = '{"metadata":{"labels":{"istio-injection":"disabled"}}}'
    kubectl(["patch", "ns", namespace, "-p", patch])


@tracing.command()
def uninstall():
    kubectl(["delete", "-f", yaml_file])
    update_cm(0)
    kubectl(["delete", "pod", "-n", "istio-system", "-l", "app=istiod"])
