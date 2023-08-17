import logging
import os

import urllib3
from kube_client.client import KubernetesClient

urllib3.disable_warnings()
logging.basicConfig(level=logging.INFO)

def main() -> None:
    env = os.getenv('ENVIRONMENT')
    client = KubernetesClient(env=env)
    while True:
        client.handle_deployment_netpol(namespace='k8s-netpol-controller')


if __name__ == "__main__":
    main()
