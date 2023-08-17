import concurrent.futures
import logging
import os
# import time # uncomment it and line 50 if you want to see how threads work with events

from kubernetes import client, config, watch
from kubernetes.client import (Configuration, V1LabelSelector, V1NetworkPolicy,
                               V1NetworkPolicySpec, V1ObjectMeta)
from kubernetes.client.exceptions import ApiException


class KubernetesClient:
    def __init__(self, env: str) -> None:
        self.configuration = Configuration()
        self.configuration.assert_hostname = False
        self.configuration.verify_ssl = False

        if env == 'local':
            config.load_kube_config(config_file=f'{os.getenv("HOME")}/.kube/config', client_configuration=self.configuration)
        else:
            config.load_incluster_config(client_configuration=self.configuration)

        self.api_client = client.ApiClient(configuration=self.configuration)
        self.apps_v1_client = client.AppsV1Api(api_client=self.api_client)
        self.networking_v1_api = client.NetworkingV1Api(api_client=self.api_client)

    def handle_deployment_netpol(self, namespace: str) -> None:
        w = watch.Watch()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for event in w.stream(self.apps_v1_client.list_namespaced_deployment, namespace=namespace):
                executor.submit(self.handle_event, event, namespace)
            

    def handle_event(self, event, namespace) -> None:
        event_type = event.get('type', None)
        event_obj = event.get('object', None)
        event_obj_name = event_obj.metadata.name

        if event_obj:
            event_obj_kind = event_obj.kind
        if event_type == 'ADDED' and event_obj_kind == 'Deployment':
            try:
                netpol = self.networking_v1_api.read_namespaced_network_policy(name=event_obj_name, namespace=namespace)
                if netpol:
                    logging.info(f'deployment: {event_obj_name} namespace: {namespace} has netpol: {netpol.metadata.name}')
            except ApiException as e:
                if e.status == 404:
                    logging.info(f'deployment: {event_obj_name} namespace: {namespace} has not netpol')
                    netpol = construct_default_netpol(event_obj_name)
                    self.networking_v1_api.create_namespaced_network_policy(body=netpol, namespace=namespace)
                    # time.sleep(10)
                    logging.info(f'netpol is created: namespace: {event_obj.metadata.namespace} name: {netpol.metadata.name}')
                else:
                    logging.info(e)


def construct_default_netpol(name: str) -> V1NetworkPolicy:
    policy_types=['Ingress', 'Egress']
    pod_selector=V1LabelSelector(match_labels={'app': name})
    spec=V1NetworkPolicySpec(pod_selector=pod_selector, policy_types=policy_types)
    metadata=V1ObjectMeta(name=name)
    
    return V1NetworkPolicy(
        spec=spec,
        api_version="networking.k8s.io/v1",
        kind="NetworkPolicy",
        metadata=metadata
    )
