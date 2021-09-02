# common utility functions

import subprocess
import time
from inspect import getframeinfo, stack
from pathlib import Path

import yaml
from logzero import logger


def kubectl(args, print_output=True, print_error=True):
    """Run kubectl command."""
    caller = getframeinfo(stack()[1][0])
    caller_module = Path(caller.filename).stem
    c = f"[{caller_module}:{caller.lineno}] "
    command = ["kubectl"]
    command.extend(args)
    logger.debug(" ".join(command))
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if print_output:
        if process.stdout != b"":
            logger.info(c + process.stdout.decode("ascii"))
        if process.stderr != b"":
            logger.error(c + process.stderr.decode("ascii"))
    return process


def wait_for_k8s_resource(
    type, name, namespace="istio-system", instances=1, timeout=600
):
    """Wait for a k8s resource to be ready"""

    while True and timeout > 0:
        timeout -= 1
        process = kubectl(
            ["get", type, "-n", namespace, name, "-o", "yaml"],
            print_output=False,
        )
        if process.returncode != 0:
            time.sleep(1)
            print("|", end="", flush=True)
            continue
        result = yaml.safe_load(process.stdout)

        if (
            "readyReplicas" in result["status"]
            and result["status"]["readyReplicas"] == instances
        ):
            break
        time.sleep(1)
        print(".", end="", flush=True)
    return 0 if timeout > 0 else 1
