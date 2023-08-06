import logging
import os
import requests
import subprocess
import tempfile
from urllib.parse import urlparse


# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(filename)s %(lineno)d> %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def apply(yaml, namespace=None):
    cmd = f"kubectl apply -f {yaml}"

    if namespace:
        cmd += f" -n {namespace}"

    logging.info(f"Applying {yaml}")
    subprocess.run(cmd, shell=True, check=True)


def pipe_bash(url):
    ua = requests.get(url, stream=True)
    ua.raise_for_status()

    basename = os.path.basename(urlparse(url).path)
    fd, filename = tempfile.mkstemp(prefix=f"{basename}-", dir="/tmp", suffix=".sh")

    with open(fd, 'wb') as out_file:
        out_file.write(ua.content)
    logging.debug(f"Downloaded {url}")

    subprocess.run(f"bash {filename}", shell=True, check=True, capture_output=False)


    os.remove(filename)


class Kind:
    def __init__(self):
        pass

    @staticmethod
    def create(version='1.26.3', config=None):
        cmd = f"kind create cluster --image=kindest/node:v{version}"

        if config:
            cmd += f" --config='{config}'"

        logging.info(f"Creating a kind cluster with version {version}")
        subprocess.run(cmd, shell=True, check=True)
        subprocess.run('kubectl cluster-info --context kind-kind', shell=True, check=True)

    @staticmethod
    def delete(cluster='kind'):
        logging.info(f"Deleting the kind cluster")
        subprocess.run(f"kind delete cluster --name {cluster}", shell=True, check=True)


