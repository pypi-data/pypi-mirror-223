from prettytable import PrettyTable
from termcolor import colored
import k8sutils.deployments as _deployments

def table(highlight=None, namespace=None):
    """Print all deployments in the cluster. Optionally highlight a deployment by name."""
    deployments = _deployments.get(namespace=namespace)
    table = PrettyTable(["Name", "Ready", "Up-to-date", "Available", "Age"])

    for deployment in deployments['items']:
        name = deployment['metadata']['name']
        ready = f"{deployment['status']['availableReplicas']}/{deployment['status']['replicas']}"
        up_to_date = deployment['status']['updatedReplicas']
        available = deployment['status']['availableReplicas']
        age = deployment['metadata']['creationTimestamp'] # TODO: format this into a more human-readable form

        table.add_row([name, ready, up_to_date, available, age])

    for line in str(table).split("\n"):
        if highlight and highlight in line:
            print(colored(line, 'green'))
        else:
            print(line)
