import logging
import os
from typing import Optional

import requests
import subprocess
import tempfile
from urllib.parse import urlparse
import yaml
from dotty_dict import Dotty



# Configure the logger
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(filename)s %(lineno)d> %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def apply(yaml: str, namespace: Optional[int] = None) -> int:
    """Apply a yaml file to the cluster.
    The file can be local or remote.

    :param yaml: The yaml file to apply
    :param namespace: The namespace to apply the yaml to
    :return: The exit code of the kubectl command
    """
    cmd = f"kubectl apply -f {yaml}"

    if namespace:
        cmd += f" -n {namespace}"

    logging.info(f"Applying {yaml}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to apply {yaml}: {str(e)}")
        return e.returncode  # Return the non-zero exit status

def delete(yaml: str, namespace: Optional[int] = None) -> int:
    """Delete resources defined in a yaml file from the cluster.
    The file can be local or remote.

    :param yaml: The yaml file that defines the resources to delete
    :param namespace: The namespace to delete the resources from
    :return: The exit code of the kubectl command
    """
    cmd = f"kubectl delete -f {yaml}"

    if namespace:
        cmd += f" -n {namespace}"

    logging.info(f"Deleting resources from {yaml}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to delete resources from {yaml}: {str(e)}")
        return e.returncode  # Return the non-zero exit status


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


class Yaml:
    def __init__(self, path):
        with open(path, 'r') as file:
            self.data = Dotty(yaml.safe_load(file))

    def set(self, key, value):
        keys = key.split(".")
        item = self.data
        for i in range(len(keys)):
            part = keys[i]
            if "[" in part and "]" in part:
                sub_key, index_str = part.split("[")
                index = int(index_str[:-1])  # Convert the index to an integer
                if sub_key:
                    item = item[sub_key]
                if i == len(keys) - 1:
                    item[index] = value
                else:
                    item = item[index]
            else:
                if i == len(keys) - 1:
                    item[part] = value
                else:
                    item = item[part]



    def save(self, path):
        with open(path, 'w') as file:
            yaml.safe_dump(self.data.to_dict(), file)
