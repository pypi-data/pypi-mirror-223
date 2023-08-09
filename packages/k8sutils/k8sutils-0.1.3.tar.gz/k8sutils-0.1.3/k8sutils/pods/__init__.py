import json
import logging
import subprocess

def get(namespace=None):
    """Get all pods in the cluster"""
    cmd = "kubectl get pods -o json"
    if namespace:
        cmd += f" -n {namespace}"

    result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
    pods = json.loads(result.stdout)
    return pods

def delete(pod_name, namespace=None):
    """Delete a specific pod by name"""
    cmd = f"kubectl delete pod {pod_name}"
    if namespace:
        cmd += f" -n {namespace}"

    try:
        logging.info(f"Deleting pod {pod_name}")
        subprocess.run(cmd, shell=True, check=True)
        logging.info(f"Pod {pod_name} deleted successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to delete pod {pod_name}: {str(e)}")
        return False

    return True