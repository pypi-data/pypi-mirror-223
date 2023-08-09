import json
import subprocess


def get():
    """Get all CRDs in the cluster"""
    json_text = subprocess.run("kubectl get crds -o json", shell=True, check=True, capture_output=True, text=True)
    crds = json.loads(json_text.stdout)
    return crds



