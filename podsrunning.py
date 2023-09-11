from kubernetes import client, config, watch
import time

def is_pod_completed(pod_name, namespace='default'):
    config.load_kube_config()  # Assumes you have a kubeconfig file set up
    v1 = client.CoreV1Api()

    try:
        pod = v1.read_namespaced_pod(pod_name, namespace)
        if pod.status.phase in ["Succeeded", "Failed"]:
            return True
        return False
    except client.ApiException as e:
        print(f"Error retrieving Pod status: {e}")
        return False

def create_pod(pod_definition, namespace='default'):
    config.load_kube_config()
    v1 = client.CoreV1Api()

    try:
        created_pod = v1.create_namespaced_pod(namespace, pod_definition)
        return created_pod.metadata.name
    except client.ApiException as e:
        print(f"Error creating Pod: {e}")
        return None

if __name__ == "__main__":
    pod_definitions = []
    #use label to find pods
    '''
    from kubernetes import client, config

def list_pods_with_label(label_selector, namespace='default'):
    config.load_kube_config()
    v1 = client.CoreV1Api()
    
    try:
        pods = v1.list_namespaced_pod(namespace, label_selector=label_selector)
        return [pod.metadata.name for pod in pods.items]
    except client.ApiException as e:
        print(f"Error retrieving Pods: {e}")
        return []

    '''

    for pod_def in pod_definitions:
        pod_name = create_pod(pod_def)
        if pod_name:
            print(f"Waiting for {pod_name} ")
            while not is_pod_completed(pod_name):
                time.sleep(10)  
            print(f"{pod_name} completed!")
