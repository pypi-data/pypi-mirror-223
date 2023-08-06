import logging
import subprocess


def label(namespace, key, value):
    logging.info(f"Labeling namespace {namespace} with {key}={value}")
    subprocess.run(f"kubectl label namespace {namespace} {key}={value}", shell=True, check=True)


def create(namespace):
    logging.info(f"Creating namespace {namespace}")
    subprocess.run(f"kubectl create namespace {namespace}", shell=True, check=True)
