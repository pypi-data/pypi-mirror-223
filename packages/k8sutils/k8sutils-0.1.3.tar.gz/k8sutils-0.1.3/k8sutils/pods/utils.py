from prettytable import PrettyTable
from termcolor import colored
import k8sutils.pods as _pods

def table(highlight=None, namespace=None):
    """Print all pods in the cluster. Optionally highlight a pod by name."""
    pods = _pods.get(namespace=namespace)
    table = PrettyTable(["NAME", "READY", "STATUS", "RESTARTS", "AGE"])

    for pod in pods['items']:
        name = pod['metadata']['name']
        ready = f"{pod['status']['containerStatuses'][0]['ready']}/{len(pod['spec']['containers'])}"
        status = pod['status']['phase']
        restarts = pod['status']['containerStatuses'][0]['restartCount']
        age = pod['metadata']['creationTimestamp'] # TODO: format this into a more human-readable form

        table.add_row([name, ready, status, restarts, age])

    for line in str(table).split("\n"):
        if highlight and highlight in line:
            print(colored(line, 'green'))
        else:
            print(line)
